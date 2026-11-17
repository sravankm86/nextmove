import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lifecycle import STATUSES, END_STATES
from stage_state import application_write, run_progress, attempt_blocks_retry

class LifecycleTests(unittest.TestCase):
    def test_nine_states_and_endpoint(self):
        self.assertEqual(len(STATUSES),9)
        self.assertEqual(END_STATES,{'Interviewing','Not pursuing','Rejected','Duplicate'})
        self.assertEqual(application_write({'Lifecycle status':'Need review'}),{'Lifecycle status':'Need review'})
    def test_uncertain_attempt_blocks_and_legacy_labels_are_rejected(self):
        self.assertTrue(attempt_blocks_retry({'Lifecycle status':'Ready'},{'submission':{'attempt_key':'attempt-example'}}))
        for legacy in ['Confirmed','Needs review','Offer','Submission uncertain']:
            with self.assertRaises(ValueError):application_write({'Lifecycle status':legacy})
    def test_run_progress_reads_checkpoint_only(self):
        run={'Input versions (JSON)':'immutable input pins','Checkpoint (JSON)':'{"cursor":42}'}
        self.assertEqual(run_progress(run),{'cursor':42})
        self.assertEqual(run_progress({'Checkpoint (JSON)':'not json'}),{'raw_checkpoint':'not json'})
        self.assertEqual(run_progress({}),{})

if __name__=='__main__':unittest.main()
