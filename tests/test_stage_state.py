import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import stage_state as s

class StateTests(unittest.TestCase):
    def setUp(self):
        self.inputs={'goals':'goals-v1','master':'master-v1','policy':'review-v3','eligibility_policy':'scope-v3','instructions':'new-storage-release','jd_hash':'jd-v1'}
        self.run={'id':'run-example','Input versions (JSON)':json.dumps({'stage_inputs':{'review':{**self.inputs,'instructions':'original-review-release'}}})}
        self.app={'id':'role-example','Job key':'employer:role-123','Lifecycle status':'Queued','Role eligibility':'Eligible','Career fit':'High','Resume fit':'Medium','Review run':['run-example']}
        self.state={'record_id':'role-example','job_key':self.app['Job key'],'stage_runs':{'review':'run-example'},'review':{'decision':'approve','jd_hash':'jd-v1','current_description':True,'role_eligible':True,'career_requirements_pass':True,'base_salary_pass':True,'qualifications_pass':True,'resume_exclusions_pass':True,'essential_fit_pass':True,'non_compensation_requirements_pass':True}}
    def test_manual_queue_cannot_create_acceptance(self):
        self.assertFalse(s.review_ready(self.app,None,[self.run],self.inputs))
        changed=copy.deepcopy(self.state);changed['review']['decision']='Needs review'
        self.assertFalse(s.review_ready(self.app,changed,[self.run],self.inputs))
    def test_general_pm_exception_needs_its_own_preference_and_scope_evidence(self):
        state=copy.deepcopy(self.state);r=state['review'];r['qualification_method']='general_senior_pm'
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))
        r.update(general_role_verified=True,general_preference_applied=True,seniority_pass=True,
                 general_preference_evidence={'source_revision':'goals-v1','preference':'General senior PM roles accepted'})
        self.assertTrue(s.review_ready(self.app,state,[self.run],self.inputs))
        r['general_role_verified']=False
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))
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

    def test_provisional_salary_can_prepare_but_cannot_apply(self):
        state=copy.deepcopy(self.state)
        state['review'].update(decision='approve_provisional',career_requirements_pass=None,
                               base_salary_pass=None,deferred_checks=['base_salary'])
        self.assertTrue(s.review_ready(self.app,state,[self.run],self.inputs))
        self.assertFalse(s.apply_ready(self.app,state,[self.run],self.inputs))
        state['review']['deferred_checks'].append('language')
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))
        state['review'].update(deferred_checks=['base_salary'],base_salary_pass=False)
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))

    def test_qualification_or_exclusion_failure_cannot_be_queued_by_high_career_fit(self):
        for key in ['qualifications_pass','resume_exclusions_pass','essential_fit_pass','non_compensation_requirements_pass']:
            state=copy.deepcopy(self.state);state['review'][key]=None
            self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))

    def test_known_failing_salary_cannot_hide_behind_a_career_pass(self):
        state=copy.deepcopy(self.state);state['review']['base_salary_pass']=False
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs))

    def test_apply_requires_ready_even_when_a_verified_pdf_is_retained(self):
        data=b'verified-pdf';digest=hashlib.sha256(data).hexdigest()
        app={**self.app,'Lifecycle status':'Ready','Resume link':'file-example','Resume version':digest,'Resume verified at':'2026-01-01','Preparation run':['prep-example']}
        state=copy.deepcopy(self.state);state['stage_runs']['preparation']='prep-example';state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1'}
        self.assertTrue(s.apply_ready(app,state,[self.run],self.inputs,data))
        self.assertFalse(s.apply_ready({**app,'Lifecycle status':'Queued'},state,[self.run],self.inputs,data))

    def test_exact_identity_does_not_merge_regional_or_same_title_roles(self):
        a={'company_id':'employer-example','role_id':'req-a','job_url':'https://jobs.example.test/roles/a?utm_source=mail'}
        self.assertTrue(s.exact_job_match(a,{**a,'job_url':'https://jobs.example.test/roles/a'}))
        self.assertFalse(s.exact_job_match(a,{**a,'role_id':'req-b','job_url':'https://jobs.example.test/roles/b'}))
        self.assertFalse(s.exact_job_match(a,{**a,'company_id':'other-employer'}))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/?jobId=1'),s.canonical_job_url('https://jobs.example.test/?jobId=2'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/?ref=role-a'),s.canonical_job_url('https://jobs.example.test/?ref=role-b'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/#/job/one'),s.canonical_job_url('https://jobs.example.test/#/job/two'))

if __name__=='__main__':unittest.main()
