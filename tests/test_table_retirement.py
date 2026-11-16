import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from table_retirement import consolidated_run, historical_event_type, source_checkpoint
from stage_state import run_progress, run_progress_contexts
import hashlib
import json


class TableRetirementTests(unittest.TestCase):
    def test_source_cursor_proof_and_reader_context_survive_column_removal(self):
        source = {'Checkpoint (JSON)': '{"cursor":"next-page","end_verified":false,"proof_sha256":"proof-example"}',
                  'source_verification': 'Official feed verified', 'Manifest version': 'manifest-example',
                  'run_id': 'execution-example', 'snapshot_at': '2026-01-01', 'Archived at': '2026-01-02'}
        original = copy.deepcopy(source)
        result = source_checkpoint(source)
        self.assertEqual(source, original)
        self.assertEqual(result['cursor'], 'next-page')
        self.assertFalse(result['end_verified'])
        self.assertEqual(result['source_context']['verification'], 'Official feed verified')
        self.assertEqual(result['source_context']['legacy_run_key'], 'execution-example')
        self.assertEqual(source['Archived at'], '2026-01-02')
        self.assertEqual(source_checkpoint({'Checkpoint (JSON)': result}), result)

    def test_run_merges_pending_handoff_without_touching_accepted_input_pins(self):
        run = {'Checkpoint (JSON)': '{"cursor":"next-page"}', 'Pending checks (JSON)': '["role-example"]',
               'Handoff (JSON)': '{"next":"Review"}', 'Input versions (JSON)': 'immutable pins'}
        original = copy.deepcopy(run)
        result = consolidated_run(run)
        self.assertEqual(result['pending_checks'], ['role-example'])
        self.assertEqual(result['handoff']['next'], 'Review')
        self.assertEqual(run, original)
        with self.assertRaises(ValueError):
            consolidated_run({**run, 'Checkpoint (JSON)': '{"pending_checks":[]}'})

    def test_history_backfill_does_not_invent_business_event_actor_or_time(self):
        event = {'Operation': 'Update', 'Phase': 'Succeeded', 'Recorded at': 'old-recorded-time'}
        original = copy.deepcopy(event)
        self.assertEqual(historical_event_type(event), 'Update / Succeeded')
        self.assertEqual(event, original)
        self.assertEqual(historical_event_type({**event, 'Event type': 'Confirmation received'}), 'Confirmation received')
        with self.assertRaises(ValueError):
            historical_event_type({})

    def test_immutable_history_context_recovers_progress_after_retired_columns_are_gone(self):
        raw = '{"cursor":"old-page"}'
        run = {'id': 'run-example', 'Checkpoint (JSON)': raw, 'Input versions (JSON)': 'fixed accepted pins'}
        original = copy.deepcopy(run)
        data = {'schema': 'nextmove.run-progress.v1', 'original_run_id': 'run-example',
                'accepted_checkpoint_hashes': [hashlib.sha256(raw.encode()).hexdigest()],
                'checkpoint': {'cursor': 'old-page', 'pending_checks': ['role-example'], 'handoff': {'next': 'Review'}}}
        history = [{'id': 'history-example', 'Recorded at': '2026-01-01',
                    'Field changes (JSON)': json.dumps(data)}]
        contexts = run_progress_contexts(history)
        resolved = run_progress(run, progress_contexts=contexts)
        self.assertEqual(resolved['pending_checks'], ['role-example'])
        self.assertEqual(resolved['_progress_context_event'], 'history-example')
        self.assertEqual(run, original)
        with self.assertRaises(ValueError):
            run_progress({**run, 'Checkpoint (JSON)': '{"cursor":"unexpected-edit"}'}, progress_contexts=contexts)
        resumed = {**resolved, 'cursor': 'new-page'}
        self.assertEqual(run_progress({**run, 'Checkpoint (JSON)': json.dumps(resumed)}, progress_contexts=contexts)['cursor'], 'new-page')


if __name__ == '__main__':
    unittest.main()
