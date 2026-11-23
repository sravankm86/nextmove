import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lifecycle import STATUSES, END_STATES, LEGACY_READ_ONLY
from stage_state import application_write, run_progress, protected_history, merge_state

class LifecycleTests(unittest.TestCase):
    def test_six_active_states_and_ready_endpoint(self):
        self.assertEqual(STATUSES,['Inventoried','Need review','Queued','Ready','Not pursuing','Duplicate'])
        self.assertEqual(END_STATES,{'Ready','Not pursuing','Duplicate'})
        commands=json.loads((ROOT/'contracts/commands.json').read_text())
        self.assertEqual(commands['pipeline'],['Curate','Scan','Review','Prepare'])
        self.assertEqual(commands['endpoint'],'Ready')
        self.assertFalse({'Apply','Track'} & {c['command'] for c in commands['commands']})

    def test_historical_outcomes_and_attempts_cannot_be_reopened(self):
        histories=[{'Lifecycle status':s} for s in LEGACY_READ_ONLY]
        histories.append({'Lifecycle status':'Queued','Submission attempt key':'legacy'})
        for old in histories:
            self.assertTrue(protected_history(old))
            with self.assertRaises(ValueError):application_write({'Lifecycle status':'Queued'},existing_application=old)
            self.assertEqual(application_write({'Feedback':None},existing_application=old),{'Feedback':None})
        with self.assertRaises(ValueError):
            application_write({'Agent notes':'Reopening'},existing_application={'Lifecycle status':'Queued'},existing_state={'submission':{'attempt_key':'legacy'}})
        for old in ['Confirmed','Needs review','Offer','Submission uncertain',*LEGACY_READ_ONLY]:
            with self.assertRaises(ValueError):application_write({'Lifecycle status':old})
        for field in ['Submission run','Submission attempt key','Applied on','Confirmation reference']:
            with self.assertRaises(ValueError):application_write({field:'old'})

    def test_active_answer_links_are_permitted(self):
        self.assertEqual(application_write({'Application questions':['question-one']}), {'Application questions':['question-one']})

    def test_active_state_merge_preserves_opaque_legacy_history(self):
        old={'record_id':'role','stage_runs':{'submission':'old-run'},'submission':{'attempt_key':'legacy'}}
        merged=merge_state(old,record_id='role',job_key='employer:role',stage='scan',run_id='new',values={'observed':True})
        self.assertEqual(merged['submission'],old['submission'])
        with self.assertRaises(ValueError):merge_state(old,record_id='role',job_key='employer:role',stage='submission',run_id='new',values={})

    def test_run_progress_reads_checkpoint_only(self):
        run={'Input versions (JSON)':'immutable input pins','Checkpoint (JSON)':'{"cursor":42}'}
        self.assertEqual(run_progress(run),{'cursor':42})
        self.assertEqual(run_progress({'Checkpoint (JSON)':'not json'}),{'raw_checkpoint':'not json'})
        self.assertEqual(run_progress({}),{})

if __name__=='__main__':unittest.main()
