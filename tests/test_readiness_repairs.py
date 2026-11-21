import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from stage_state import resolve,payload,application_write,company_history_ready
from review_eval import feedback_id,feedback_clear

class RecoveryAndFeedbackTests(unittest.TestCase):
    def test_legacy_field_change_map_does_not_crash_or_replace_acceptance(self):
        state={'record_id':'role-one','stage_runs':{'review':'run-one'},'review':{'decision':'approve'}}
        good={'Recorded at':'2026-01-01','Field changes (JSON)':json.dumps(payload([state]))}
        bad={'Recorded at':'2026-01-02','Field changes (JSON)':json.dumps({'schema':'nextmove.stage-state.v1','records':{'role-one':[{'field':'resume','after':'pdf'}]}})}
        original=copy.deepcopy([good,bad])
        self.assertEqual(resolve({'id':'role-one'},[good,bad]),state)
        self.assertIsNone(resolve({'id':'role-one'},[bad]))
        self.assertEqual([good,bad],original)
        for records in [None,'broken',[None,'role-one',{},3]]:
            event={'Field changes (JSON)':{'schema':'nextmove.stage-state.v2','records':records}}
            self.assertEqual(resolve({'id':'role-one'},[good,event]),state)

    def test_same_company_history_cannot_be_hidden_by_not_applicable(self):
        p={'company_consistency':'not_applicable'}
        self.assertFalse(company_history_ready(p))
        p['company_history']={'status':'complete','matches':0,'evidence':'Live records checked'}
        self.assertTrue(company_history_ready(p))
        p['company_history']['matches']=1
        self.assertFalse(company_history_ready(p))
        p['company_consistency']='pass'
        self.assertFalse(company_history_ready(p))
        p['company_history']['compared_versions']=['exact-prior-file']
        self.assertTrue(company_history_ready(p))
        p['company_history']['missing_details']=['Submitted date unknown']
        self.assertFalse(company_history_ready(p))

    def test_only_verified_feedback_is_acknowledged_and_manual_notes_survives(self):
        row={'Manual notes':'Referral from a colleague. Keep this.','Feedback':'The role requires a missing specialty.'}
        receipt={'feedback_id':feedback_id('Review','role',row['Feedback']),'case_id':'case','snapshot_ref':'file','history_id':'event','eval_verified':True,'snapshot_verified':True,'history_verified':True}
        delta=feedback_clear('Review','role',row['Feedback'],row,receipt)
        self.assertEqual(delta,{'Feedback':None})
        self.assertEqual({**row,**delta}['Manual notes'],row['Manual notes'])
        self.assertEqual(feedback_clear('Review','role',row['Feedback'],row,{**receipt,'snapshot_verified':False}),{})
        self.assertEqual(feedback_clear('Review','role',row['Feedback'],{**row,'Feedback':'Concurrent edit'},receipt),{})
        self.assertEqual(feedback_clear('Review','role',row['Feedback'],{'Manual notes':row['Feedback']},receipt),{})
        with self.assertRaises(ValueError):application_write({'Manual notes':None})

if __name__=='__main__':unittest.main()
