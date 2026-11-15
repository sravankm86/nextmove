import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lifecycle import STATUSES, END_STATES, normalize
from stage_state import application_write, run_progress, attempt_blocks_retry

class LifecycleTests(unittest.TestCase):
    def test_seven_states_and_endpoint(self):
        self.assertEqual(len(STATUSES),7)
        self.assertEqual(END_STATES,{'Interviewing','Not pursuing','Rejected'})
        self.assertEqual(normalize('Confirmed'),'Applied')
        self.assertEqual(normalize('In process'),'Interviewing')
        self.assertEqual(normalize('Offer'),'Interviewing')
        self.assertIsNone(normalize('invented state'))
    def test_unknown_review_and_uncertain_attempt_never_create_success(self):
        self.assertEqual(normalize('Shortlisted'),'Inventoried')
        self.assertEqual(normalize('Shortlisted',review_approved=True),'Queued')
        self.assertEqual(normalize('Submission uncertain'),'Inventoried')
        self.assertEqual(normalize('Submission uncertain',last_verified_stage='Ready'),'Ready')
        self.assertTrue(attempt_blocks_retry({'Lifecycle status':'Ready'},{'submission':{'attempt_key':'attempt-example'}}))
        for legacy in ['Confirmed','Needs review','Offer','Submission uncertain']:
            with self.assertRaises(ValueError):application_write({'Lifecycle status':legacy})
    def test_legacy_run_progress_is_read_without_losing_frozen_inputs(self):
        run={'Input versions (JSON)':'immutable input pins','Checkpoint (JSON)':'{"cursor":42}',
             'Pending checks (JSON)':'["role-example"]','Handoff (JSON)':'{"next":"Review"}',
             'Mode':'prepare','Next command':'Review'}
        result=run_progress(run)
        self.assertEqual(result['cursor'],42)
        self.assertEqual(result['pending_checks'],['role-example'])
        self.assertEqual(result['handoff'],{'next':'Review'})
        self.assertEqual(run['Input versions (JSON)'],'immutable input pins')
        self.assertNotIn('pending_checks',__import__('json').loads(run['Checkpoint (JSON)']))
        run['Checkpoint (JSON)']='{"pending_checks":[]}'
        self.assertEqual(run_progress(run)['pending_checks'],[])

if __name__=='__main__':unittest.main()
