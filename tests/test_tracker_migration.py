import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import stage_state as s
from tracker_migration import migrate


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.app = {'id': 'role-example', 'Application': 'old label', 'Role eligibility': 'Eligible',
                    'Career gate': 'Pass', 'Lifecycle status': 'Queued', 'Career fit': 'High',
                    'Review run': ['run-example'], 'Manual notes': 'Keep my wording',
                    'Assessment summary': 'Strong fit', 'Blocker': 'Confirm salary',
                    'Decision category': 'missing_evidence', 'Sources': ['source-example']}
        self.state = {'record_id': 'role-example', 'stage_runs': {'review': 'run-example'},
                      'review': {'decision': 'approve', 'jd_hash': 'jd-example', 'current_description': True,
                                 'qualifications_pass': True, 'resume_exclusions_pass': True,
                                 'essential_fit_pass': True, 'non_compensation_requirements_pass': True},
                      'submission': {'attempt_key': 'attempt-example'}}
        self.run = {'id': 'run-example', 'Input versions (JSON)': {'stage_inputs': {'review': {
            'goals': 'goals-example', 'master': 'master-example', 'policy': 'review-example',
            'eligibility_policy': 'scope-example'}}}}

    def test_preserves_acceptance_notes_provenance_and_retry_guard(self):
        original = copy.deepcopy(self.app)
        state, notes, status = migrate(self.app, self.state, [self.run])
        self.assertEqual(self.app, original)
        self.assertEqual(status, 'Queued')
        self.assertEqual(notes, 'Strong fit\nNext: Confirm salary')
        self.assertEqual(state['source']['memberships'], ['source-example'])
        self.assertEqual(state['review']['reason_category'], 'missing_evidence')
        self.assertEqual(state['details']['tracker_migration_v7']['previous_fields']['Career gate'], 'Pass')
        self.assertTrue(s.attempt_blocks_retry(self.app, state))
        stripped = {k: v for k, v in self.app.items() if k not in s.RETIRED_FIELDS}
        current = {**s.stage_versions(state, 'review', [self.run]), 'jd_hash': 'jd-example'}
        self.assertTrue(s.review_ready(stripped, state, [self.run], current))

    def test_unknown_or_failed_career_check_never_inherits_approval_from_status(self):
        for value in [None, 'Pending', 'Fail']:
            state, _, status = migrate({**self.app, 'Career gate': value}, self.state, [self.run])
            self.assertIsNot(state['review']['career_requirements_pass'], True)
            self.assertEqual(status, 'Needs review')

    def test_historical_outcome_and_unknown_identity_are_preserved(self):
        state, _, status = migrate({**self.app, 'Lifecycle status': 'Applied', 'Job key': None,
                                   'Career gate': None}, self.state, [self.run])
        self.assertEqual(status, 'Applied')
        self.assertEqual(state['submission']['attempt_key'], 'attempt-example')


if __name__ == '__main__':
    unittest.main()
