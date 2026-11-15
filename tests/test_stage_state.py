import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import stage_state as s

class StateTests(unittest.TestCase):
    def setUp(self):
        self.inputs={'goals':'goals-v1','master':'master-v1','policy':'review-v3','eligibility_policy':'scope-v3','instructions':'new-storage-release','jd_hash':'jd-v1'}
        self.run={'id':'run-example','Input versions (JSON)':json.dumps({'stage_inputs':{'review':{**self.inputs,'instructions':'original-review-release'}}})}
        self.app={'id':'role-example','Job key':'employer:role-123','Lifecycle status':'Queued','Role eligibility':'Eligible','Career fit':'High','Resume fit':'Medium','Review run':['run-example']}
        self.state={'record_id':'role-example','job_key':self.app['Job key'],'stage_runs':{'review':'run-example'},'review':{'decision':'approve','jd_hash':'jd-v1','current_description':True,'role_eligible':True,'career_requirements_pass':True}}
    def test_manual_queue_cannot_create_acceptance(self):
        self.assertFalse(s.review_ready(self.app,None,[self.run],self.inputs))
        changed=copy.deepcopy(self.state);changed['review']['decision']='Needs review'
        self.assertFalse(s.review_ready(self.app,changed,[self.run],self.inputs))
    def test_schema_only_release_preserves_policy_but_changed_inputs_block(self):
        self.assertTrue(s.review_ready(self.app,self.state,[self.run],self.inputs))
        for key in ['goals','master','policy','eligibility_policy','jd_hash']:
            self.assertFalse(s.review_ready(self.app,self.state,[self.run],{**self.inputs,key:'changed'}))
    def test_queue_needs_explicit_hard_requirement_checks_without_gate_column(self):
        for key in ['role_eligible','career_requirements_pass']:
            for value in [None,False,'Pass']:
                state=copy.deepcopy(self.state);state['review'][key]=value
                self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))
        for field in s.RETIRED_FIELDS:
            with self.assertRaises(ValueError):s.application_write({field:'old value'})
        with self.assertRaises(ValueError):s.application_write({'Application ID':'invented'})
    def test_later_complete_snapshot_supersedes_old_approval(self):
        history=[{'Recorded at':'2026-01-01','Field changes (JSON)':json.dumps(s.payload([self.state]))}]
        later=copy.deepcopy(self.state);later['review']['decision']='Not aligned'
        history.append({'Recorded at':'2026-01-02','Field changes (JSON)':json.dumps(s.payload([later]))})
        self.assertEqual(s.resolve(self.app,history)['review']['decision'],'Not aligned')
    def test_changed_pdf_bytes_and_unknown_verification_block(self):
        pdf=b'original verified pdf';digest=hashlib.sha256(pdf).hexdigest();app={**self.app,'Lifecycle status':'Ready','Resume link':'verified-file','Resume version':digest,'Resume verified at':'2026-01-01','Preparation run':['prep-example']}
        state=copy.deepcopy(self.state);state['stage_runs']['preparation']='prep-example';state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1'}
        self.assertTrue(s.resume_ready(app,state,[self.run],self.inputs,pdf))
        self.assertFalse(s.resume_ready(app,state,[self.run],self.inputs,b'edited pdf'))
        app['Resume verified at']=None;self.assertFalse(s.resume_ready(app,state,[self.run],self.inputs,pdf))
    def test_pending_attempt_survives_manual_status_reset(self):
        self.assertTrue(s.attempt_blocks_retry({**self.app,'Lifecycle status':'Ready','Submission attempt key':'attempt-example'},self.state))
        self.assertTrue(s.attempt_blocks_retry(self.app,{'submission':{'attempt_key':'attempt-example'}}))
    def test_legacy_columns_and_multiple_context_links_are_rejected(self):
        with self.assertRaises(ValueError):s.application_write({'Evidence versions (JSON)':'old plan'})
        with self.assertRaises(ValueError):s.application_write({'Company':['one','two']})
        self.assertEqual(len(s.CORE_FIELDS),28)
    def test_separate_harness_recovers_without_legacy_columns(self):
        h=[{'Recorded at':'2026-01-01','Field changes (JSON)':json.dumps(s.payload([self.state]))}]
        self.assertTrue(s.review_ready(self.app,s.resolve(self.app,h),[self.run],self.inputs))
    def test_new_candidate_requires_checked_identity_and_explicit_allow(self):
        candidate={'Job key':'employer:role-123','Role':'Product Manager','Company':['company-example'],'Lifecycle status':'Inventoried','Role eligibility':'Pending'}
        self.assertEqual(s.application_write(candidate,creating=True,existing_keys=set(),allowed_companies={'company-example'}),candidate)
        with self.assertRaises(ValueError):s.application_write(candidate,creating=True,existing_keys={'employer:role-123'},allowed_companies={'company-example'})
        with self.assertRaises(ValueError):s.application_write(candidate,creating=True,existing_keys=set(),allowed_companies=set())

if __name__=='__main__':unittest.main()
