import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import stage_state as s
from role_gate import review_frame_contract,scored_review

class StateTests(unittest.TestCase):
    def setUp(self):
        self.inputs={'company_evidence':'company-capture-v1','goals':'goals-v1','master':'master-v1','policy':review_frame_contract()[0],'eligibility_policy':'scope-v3','instructions':'new-storage-release','jd_hash':'jd-v1'}
        self.run={'id':'run-example','Input versions (JSON)':json.dumps({'stage_inputs':{'review':{**self.inputs,'instructions':'original-review-release'}}})}
        self.companies=[{'id':'company-example','Search status':'Allow','Application hold status':'Held'}]
        self.app={'Company':['company-example'],'id':'role-example','Job key':'employer:role-123','Lifecycle status':'Queued','Role eligibility':'Eligible','Career fit':'High','Resume fit':'Medium','Review run':['run-example']}
        self.state={'record_id':'role-example','job_key':self.app['Job key'],'stage_runs':{'review':'run-example'},'review':{'decision':'approve','jd_hash':'jd-v1','current_description':True}}
        self.state['review'].update(assessment_method='three_step_v1',scoring=scored_review('High','Medium'),evidence='Verified indexed qualification evidence',assessment_complete=True)
        self.state['run_checks']={'duplicate':{'status':'unique','checked_in_run':'run-example','evidence':'Verified official role ID'}}

    def reuse(self, digest):
        return {'path':'base_reuse','base':'base-ainative','base_version':digest,'base_master':'master-v1','coverage':'complete','company_consistency':'not_applicable','company_history':{'status':'complete','matches':0,'evidence':'Checked live application and registered historical records'}}

    def prepared(self, pdf, preparation):
        digest=hashlib.sha256(pdf).hexdigest()
        app={**self.app,'Lifecycle status':'Ready','Resume link':'file-example','Resume version':digest,'Resume verified at':'2026-01-01','Preparation run':['prep-example']}
        state=copy.deepcopy(self.state);state['stage_runs']['preparation']='prep-example'
        state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1',**preparation}
        return app,state

    def test_prepare_reuses_a_current_base_only_with_complete_coverage(self):
        pdf=b'base pdf';digest=hashlib.sha256(pdf).hexdigest()
        app,state=self.prepared(pdf,self.reuse(digest))
        self.assertTrue(s.resume_verified(app,state,[self.run],self.inputs,pdf,companies=self.companies))
        for change in [{'coverage':'partial'},{'base_master':'master-v0'},{'base_version':'other-file'},{'path':None},{'company_consistency':'conflict'}]:
            bad=copy.deepcopy(state);bad['preparation'].update(change)
            self.assertFalse(s.resume_verified(app,bad,[self.run],self.inputs,pdf,companies=self.companies))

    def test_prepare_tailored_version_needs_grounding_and_guideline_check(self):
        pdf=b'tailored pdf'
        tailored={'path':'tailored','base':'base-bigtech-a','base_version':'base-hash','grounding':'pass','guideline_check':'pass','guidelines':'guidelines-v2','company_consistency':'pass','company_history':{'status':'complete','matches':1,'evidence':'Historical submission and PDF comparison','compared_versions':['prior-pdf']}}
        app,state=self.prepared(pdf,tailored)
        inputs={**self.inputs,'resume_guidelines':'guidelines-v2'}
        self.assertTrue(s.resume_verified(app,state,[self.run],inputs,pdf,companies=self.companies))
        self.assertFalse(s.resume_verified(app,state,[self.run],{**inputs,'resume_guidelines':'guidelines-v3'},pdf,companies=self.companies))
        for change in [{'grounding':'fail'},{'guideline_check':None},{'base':None}]:
            bad=copy.deepcopy(state);bad['preparation'].update(change)
            self.assertFalse(s.resume_verified(app,bad,[self.run],inputs,pdf,companies=self.companies))

    def test_manual_queue_cannot_create_acceptance(self):
        self.assertFalse(s.review_ready(self.app,None,[self.run],self.inputs, companies=self.companies))
        changed=copy.deepcopy(self.state);changed['review']['decision']='Needs review'
        self.assertFalse(s.review_ready(self.app,changed,[self.run],self.inputs, companies=self.companies))
    def test_legacy_preference_flags_cannot_replace_current_scored_acceptance(self):
        self.assertTrue(s.review_ready(self.app,self.state,[self.run],self.inputs, companies=self.companies))
        state=copy.deepcopy(self.state);state['review'].pop('scoring')
        state['review'].update(general_role_verified=True,general_preference_applied=True,seniority_pass=True)
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs, companies=self.companies))

    def test_schema_only_release_preserves_policy_but_changed_inputs_block(self):
        self.assertTrue(s.review_ready(self.app,self.state,[self.run],self.inputs, companies=self.companies))
        for key in ['goals','master','policy','eligibility_policy','company_evidence','jd_hash']:
            self.assertFalse(s.review_ready(self.app,self.state,[self.run],{**self.inputs,key:'changed'}, companies=self.companies))
    def test_queue_needs_current_scores_and_evidence_without_extra_gate_columns(self):
        for key in ['evidence','assessment_complete','assessment_method','scoring']:
            state=copy.deepcopy(self.state);state['review'].pop(key)
            self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs, companies=self.companies))
        for field in ['Posted salary range','Career gate','Assessment summary']:
            with self.assertRaises(ValueError):s.application_write({field:'old value'})
        with self.assertRaises(ValueError):s.application_write({'Application ID':'invented'})

    def test_later_complete_snapshot_supersedes_old_approval(self):
        history=[{'Recorded at':'2026-01-01','Field changes (JSON)':json.dumps(s.payload([self.state]))}]
        later=copy.deepcopy(self.state);later['review']['decision']='Not aligned'
        history.append({'Recorded at':'2026-01-02','Field changes (JSON)':json.dumps(s.payload([later]))})
        self.assertEqual(s.resolve(self.app,history)['review']['decision'],'Not aligned')
    def test_changed_pdf_bytes_and_unknown_verification_block(self):
        pdf=b'original verified pdf';digest=hashlib.sha256(pdf).hexdigest();app={**self.app,'Lifecycle status':'Ready','Resume link':'verified-file','Resume version':digest,'Resume verified at':'2026-01-01','Preparation run':['prep-example']}
        state=copy.deepcopy(self.state);state['stage_runs']['preparation']='prep-example';state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1',**self.reuse(digest)}
        self.assertTrue(s.resume_verified(app,state,[self.run],self.inputs,pdf, companies=self.companies))
        self.assertFalse(s.resume_verified(app,state,[self.run],self.inputs,b'edited pdf', companies=self.companies))
        app['Resume verified at']=None;self.assertFalse(s.resume_verified(app,state,[self.run],self.inputs,pdf, companies=self.companies))
    def test_pending_attempt_survives_manual_status_reset(self):
        self.assertTrue(s.protected_history({**self.app,'Lifecycle status':'Ready','Submission attempt key':'attempt-example'},self.state))
        self.assertTrue(s.protected_history(self.app,{'submission':{'attempt_key':'attempt-example'}}))
    def test_legacy_columns_and_multiple_context_links_are_rejected(self):
        with self.assertRaises(ValueError):s.application_write({'Evidence versions (JSON)':'old plan'})
        with self.assertRaises(ValueError):s.application_write({'Company':['one','two']})
        self.assertEqual(len(s.CORE_FIELDS),27)
    def test_separate_harness_recovers_without_legacy_columns(self):
        h=[{'Recorded at':'2026-01-01','Field changes (JSON)':json.dumps(s.payload([self.state]))}]
        self.assertTrue(s.review_ready(self.app,s.resolve(self.app,h),[self.run],self.inputs, companies=self.companies))
    def test_new_candidate_requires_checked_identity_and_explicit_allow(self):
        candidate={'Job key':'employer:role-123','Role':'Product Manager','Company':['company-example'],'Lifecycle status':'Inventoried','Role eligibility':'Pending'}
        self.assertEqual(s.application_write(candidate,creating=True,existing_keys=set(),allowed_companies={'company-example'}, companies=self.companies),candidate)
        with self.assertRaises(ValueError):s.application_write(candidate,creating=True,existing_keys={'employer:role-123'},allowed_companies={'company-example'}, companies=self.companies)
        with self.assertRaises(ValueError):s.application_write(candidate,creating=True,existing_keys=set(),allowed_companies=set(), companies=self.companies)

    def test_provisional_or_unresolved_review_cannot_prepare(self):
        state=copy.deepcopy(self.state);state['review']['decision']='approve_provisional'
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs, companies=self.companies))
        state['review']['decision']='approve';state['review']['scoring']=scored_review('Unresolved','High')
        self.assertFalse(s.review_ready(self.app,state,[self.run],self.inputs, companies=self.companies))

    def test_changed_ratings_cannot_reuse_a_prior_queue_score(self):
        for field in ['Career fit','Resume fit']:
            app={**self.app,field:'Low'}
            self.assertFalse(s.review_ready(app,self.state,[self.run],self.inputs, companies=self.companies))

    def test_old_policy_label_cannot_bypass_current_scoring(self):
        inputs={**self.inputs,'policy':'review-v3'}
        run=copy.deepcopy(self.run);run['Input versions (JSON)']=json.dumps({'stage_inputs':{'review':inputs}})
        self.assertFalse(s.review_ready(self.app,self.state,[run],inputs, companies=self.companies))

    def test_ready_endpoint_rejects_protected_outcomes_even_with_a_verified_pdf(self):
        data=b'verified-pdf';digest=hashlib.sha256(data).hexdigest()
        app={**self.app,'Lifecycle status':'Ready','Resume link':'file-example','Resume version':digest,'Resume verified at':'2026-01-01','Preparation run':['prep-example']}
        state=copy.deepcopy(self.state);state['stage_runs']['preparation']='prep-example';state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1',**self.reuse(digest)}
        self.assertTrue(s.resume_verified(app,state,[self.run],self.inputs,data, companies=self.companies))
        for status in ['Needs answer','Applied','Interviewing','Rejected','Not pursuing','Duplicate']:
            self.assertFalse(s.resume_verified({**app,'Lifecycle status':status},state,[self.run],self.inputs,data,companies=self.companies))
        self.assertFalse(s.resume_verified({**app,'Submission attempt key':'legacy'},state,[self.run],self.inputs,data,companies=self.companies))
        old=copy.deepcopy(state);old['submission']={'attempt_key':'legacy'}
        self.assertFalse(s.resume_verified(app,old,[self.run],self.inputs,data,companies=self.companies))

    def test_exact_identity_does_not_merge_regional_or_same_title_roles(self):
        self.assertEqual(s.canonical_job_url('https://jobs.example.test/roles/a?utm_source=mail'),s.canonical_job_url('https://jobs.example.test/roles/a'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/?jobId=1'),s.canonical_job_url('https://jobs.example.test/?jobId=2'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/?ref=role-a'),s.canonical_job_url('https://jobs.example.test/?ref=role-b'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/#/job/one'),s.canonical_job_url('https://jobs.example.test/#/job/two'))

if __name__=='__main__':unittest.main()
