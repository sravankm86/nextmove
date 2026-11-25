import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import stage_state as s
from role_gate import review_frame_contract,scored_review

class StateTests(unittest.TestCase):
    def setUp(self):
        self.inputs={'company_evidence':'company-capture-v1','goals':'goals-v1','master':'master-v1','policy':review_frame_contract()[0],'instructions':'new-storage-release','jd_hash':'jd-v1'}
        self.companies=[{'id':'company-example','Search status':'Allow','Application hold status':'Held'}]
        self.app={'Company':['company-example'],'id':'role-example','Job key':'employer:role-123','Lifecycle status':'Queued','Career fit':'High','Resume fit':'Medium'}
        self.state={'record_id':'role-example','job_key':self.app['Job key'],'schema':s.SCHEMA,'review':{'decision':'approve','jd_hash':'jd-v1','current_description':True}}
        self.state['review'].update(assessment_method='three_step_v1',scoring=scored_review('High','Medium'),evidence='Verified indexed qualification evidence',assessment_complete=True)
        self.state['review']['inputs']={**self.inputs,'instructions':'original-review-release'}
        self.state['run_checks']={'duplicate':{'status':'unique','checked_at':'2026-01-01T00:00:00Z','evidence':'Verified official role ID'}}

    def reuse(self, digest):
        return {'path':'base_reuse','base':'base-ainative','base_version':digest,'base_master':'master-v1','coverage':'complete','company_consistency':'not_applicable','company_history':{'status':'complete','matches':0,'evidence':'Checked live application and registered historical records'}}

    def prepared(self, pdf, preparation):
        digest=hashlib.sha256(pdf).hexdigest()
        app={**self.app,'Lifecycle status':'Ready','Resume link':'file-example','Resume version':digest,'Resume verified at':'2026-01-01'}
        state=copy.deepcopy(self.state)
        state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1',**preparation}
        return app,state

    def test_prepare_reuses_a_current_base_only_with_complete_coverage(self):
        pdf=b'base pdf';digest=hashlib.sha256(pdf).hexdigest()
        app,state=self.prepared(pdf,self.reuse(digest))
        self.assertTrue(s.resume_verified(app,state,self.inputs,pdf,companies=self.companies))
        for change in [{'coverage':'partial'},{'base_master':'master-v0'},{'base_version':'other-file'},{'path':None},{'company_consistency':'conflict'}]:
            bad=copy.deepcopy(state);bad['preparation'].update(change)
            self.assertFalse(s.resume_verified(app,bad,self.inputs,pdf,companies=self.companies))

    def test_prepare_tailored_version_needs_grounding_and_guideline_check(self):
        pdf=b'tailored pdf'
        tailored={'path':'tailored','base':'base-bigtech-a','base_version':'base-hash','grounding':'pass','guideline_check':'pass','guidelines':'guidelines-v2','company_consistency':'pass','company_history':{'status':'complete','matches':1,'evidence':'Historical submission and PDF comparison','compared_versions':['prior-pdf']}}
        app,state=self.prepared(pdf,tailored)
        inputs={**self.inputs,'resume_guidelines':'guidelines-v2'}
        self.assertTrue(s.resume_verified(app,state,inputs,pdf,companies=self.companies))
        self.assertFalse(s.resume_verified(app,state,{**inputs,'resume_guidelines':'guidelines-v3'},pdf,companies=self.companies))
        for change in [{'grounding':'fail'},{'guideline_check':None},{'base':None}]:
            bad=copy.deepcopy(state);bad['preparation'].update(change)
            self.assertFalse(s.resume_verified(app,bad,inputs,pdf,companies=self.companies))

    def test_current_resume_can_proceed_without_old_submitted_files(self):
        pdf=b'current verified base'; digest=hashlib.sha256(pdf).hexdigest()
        p=self.reuse(digest)
        p.update(company_consistency='not_required', company_history={
            'status':'not_required','policy':'current_resume_only',
            'reason':'Prior submitted files unavailable; use the current approved base.',
            'evidence':'Current registered guidelines authorize this path.',
            'missing_details':['Earlier PDF and date are unavailable.']})
        app,state=self.prepared(pdf,p)
        self.assertTrue(s.resume_verified(app,state,self.inputs,pdf))
        # The new PDF is still checked against the current master, never waived.
        self.assertFalse(s.resume_verified(app,state,{**self.inputs,'master':'new-master'},pdf))
        state['preparation']['company_history'].pop('evidence')
        self.assertFalse(s.resume_verified(app,state,self.inputs,pdf))

    def test_manual_queue_authorizes_prepare_without_forging_review_approval(self):
        self.assertTrue(s.preparation_eligible(self.app))
        self.assertFalse(s.review_ready(self.app,None,self.inputs, companies=self.companies))
        changed=copy.deepcopy(self.state);changed['review']['decision']='Needs review'
        self.assertTrue(s.preparation_eligible(self.app,changed))
        self.assertFalse(s.review_ready(self.app,changed,self.inputs, companies=self.companies))

    def test_agent_queue_admission_enforces_review_before_the_transition(self):
        old={**self.app,'Lifecycle status':'Need review'}
        values={'Lifecycle status':'Queued'}
        with self.assertRaises(ValueError):
            s.application_write(values,existing_application=old,existing_state=self.state)
        self.assertEqual(s.application_write(values,existing_application=old,existing_state=self.state,
            current_inputs=self.inputs,companies=self.companies),values)
        changed=copy.deepcopy(self.state);changed['review']['scoring']=scored_review('Unresolved','Medium')
        with self.assertRaises(ValueError):
            s.application_write(values,existing_application=old,existing_state=changed,
                current_inputs=self.inputs,companies=self.companies)
        # An already Queued role does not go through admission again.
        self.assertEqual(s.application_write(values,existing_application=self.app),values)

    def test_prepare_handoff_only_uses_active_queue_and_preserves_prior_submissions(self):
        for status in ['Queued','Needs answer']:
            self.assertTrue(s.preparation_eligible({**self.app,'Lifecycle status':status}))
        for status in ['Inventoried','Need review','Duplicate','Not pursuing','Applied','Interviewing','Rejected']:
            self.assertFalse(s.preparation_eligible({**self.app,'Lifecycle status':status}))
        self.assertFalse(s.preparation_eligible({**self.app,'Submission attempt key':'previous'}))
        self.assertFalse(s.preparation_eligible(self.app,{'submission':{'attempt_key':'previous'}}))

    def test_prepare_never_reapplies_fit_or_company_preferences(self):
        pdf=b'base pdf';digest=hashlib.sha256(pdf).hexdigest()
        app,state=self.prepared(pdf,self.reuse(digest))
        app.update({'Career fit':'Unresolved','Resume fit':'Low'})
        state.pop('review');state.pop('run_checks')
        inputs={**self.inputs,'goals':'changed','policy':'changed','company_evidence':'changed'}
        self.assertTrue(s.resume_verified(app,state,inputs,pdf,companies=[]))
        for change in [{'master':'changed'},{'jd_hash':'changed'}]:
            self.assertFalse(s.resume_verified(app,state,{**inputs,**change},pdf))

    def test_manual_queue_cannot_use_another_roles_resume_snapshot(self):
        pdf=b'base pdf';digest=hashlib.sha256(pdf).hexdigest()
        app,state=self.prepared(pdf,self.reuse(digest))
        for change in [{'record_id':'other-role'},{'job_key':'employer:other-role'}]:
            changed={**state,**change}
            self.assertFalse(s.resume_verified(app,changed,self.inputs,pdf))
    def test_legacy_preference_flags_cannot_replace_current_scored_acceptance(self):
        self.assertTrue(s.review_ready(self.app,self.state,self.inputs, companies=self.companies))
        state=copy.deepcopy(self.state);state['review'].pop('scoring')
        state['review'].update(general_role_verified=True,general_preference_applied=True,seniority_pass=True)
        self.assertFalse(s.review_ready(self.app,state,self.inputs, companies=self.companies))

    def test_schema_only_release_preserves_policy_but_changed_inputs_block(self):
        self.assertTrue(s.review_ready(self.app,self.state,self.inputs, companies=self.companies))
        for key in ['goals','master','policy','company_evidence','jd_hash']:
            self.assertFalse(s.review_ready(self.app,self.state,{**self.inputs,key:'changed'}, companies=self.companies))
    def test_queue_needs_current_scores_and_evidence_without_extra_gate_columns(self):
        for key in ['evidence','assessment_complete','assessment_method','scoring']:
            state=copy.deepcopy(self.state);state['review'].pop(key)
            self.assertFalse(s.review_ready(self.app,state,self.inputs, companies=self.companies))
        for field in ['Posted salary range','Career gate','Assessment summary']:
            with self.assertRaises(ValueError):s.application_write({field:'old value'})
        with self.assertRaises(ValueError):s.application_write({'Application ID':'invented'})

    def test_legacy_migration_takes_the_newest_snapshot_and_folds_run_inputs(self):
        old=copy.deepcopy(self.state);old.pop('schema');old['review'].pop('inputs');old['stage_runs']={'review':'run-example'}
        run={'id':'run-example','Input versions (JSON)':json.dumps({'stage_inputs':{'review':self.inputs}})}
        batch=lambda st:json.dumps({'schema':'nextmove.stage-state.v2','records':[st]})
        later=copy.deepcopy(old);later['review']['decision']='Not aligned'
        history=[{'Recorded at':'2026-01-01','Field changes (JSON)':batch(old)},{'Recorded at':'2026-01-02','Field changes (JSON)':batch(later)}]
        migrated=s.legacy_evidence(self.app,history,[run])
        self.assertEqual(migrated['review']['decision'],'Not aligned')
        self.assertEqual(migrated['review']['inputs'],self.inputs)
        self.assertNotIn('stage_runs',migrated);self.assertEqual(migrated['schema'],s.SCHEMA)
        self.assertIsNone(s.legacy_evidence(self.app,[{'Field changes (JSON)':'{"Lifecycle status":["Queued","Ready"]}'}]))
    def test_changed_pdf_bytes_and_unknown_verification_block(self):
        pdf=b'original verified pdf';digest=hashlib.sha256(pdf).hexdigest();app={**self.app,'Lifecycle status':'Ready','Resume link':'verified-file','Resume version':digest,'Resume verified at':'2026-01-01'}
        state=copy.deepcopy(self.state);state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1',**self.reuse(digest)}
        self.assertTrue(s.resume_verified(app,state,self.inputs,pdf, companies=self.companies))
        self.assertFalse(s.resume_verified(app,state,self.inputs,b'edited pdf', companies=self.companies))
        app['Resume verified at']=None;self.assertFalse(s.resume_verified(app,state,self.inputs,pdf, companies=self.companies))
    def test_pending_attempt_survives_manual_status_reset(self):
        self.assertTrue(s.protected_history({**self.app,'Lifecycle status':'Ready','Submission attempt key':'attempt-example'},self.state))
        self.assertTrue(s.protected_history(self.app,{'submission':{'attempt_key':'attempt-example'}}))
    def test_legacy_columns_and_multiple_context_links_are_rejected(self):
        with self.assertRaises(ValueError):s.application_write({'Evidence versions (JSON)':'old plan'})
        with self.assertRaises(ValueError):s.application_write({'Company':['one','two']})
        self.assertEqual(len(s.CORE_FIELDS),24)
    def test_separate_harness_recovers_without_legacy_columns(self):
        app={**self.app,'Evidence (JSON)':s.evidence_json(self.state)}
        self.assertTrue(s.review_ready(app,s.evidence(app),self.inputs, companies=self.companies))
        self.assertIsNone(s.evidence({**app,'id':'other-role'}))
        self.assertIsNone(s.evidence({**app,'Evidence (JSON)':'not json'}))
        with self.assertRaises(ValueError):s.application_write({'Evidence (JSON)':'{}'},existing_application=self.app)
        self.assertEqual(s.application_write({'Evidence (JSON)':s.evidence_json(self.state)},existing_application=self.app)['Evidence (JSON)'],s.evidence_json(self.state))
    def test_new_candidate_requires_checked_identity_and_explicit_allow(self):
        candidate={'Job key':'employer:role-123','Role':'Product Manager','Company':['company-example'],'Lifecycle status':'Inventoried'}
        self.assertEqual(s.application_write(candidate,creating=True,existing_keys=set(),allowed_companies={'company-example'}, companies=self.companies),candidate)
        with self.assertRaises(ValueError):s.application_write(candidate,creating=True,existing_keys={'employer:role-123'},allowed_companies={'company-example'}, companies=self.companies)
        with self.assertRaises(ValueError):s.application_write(candidate,creating=True,existing_keys=set(),allowed_companies=set(), companies=self.companies)

    def test_provisional_or_unresolved_review_cannot_agent_queue(self):
        state=copy.deepcopy(self.state);state['review']['decision']='approve_provisional'
        self.assertFalse(s.review_ready(self.app,state,self.inputs, companies=self.companies))
        state['review']['decision']='approve';state['review']['scoring']=scored_review('Unresolved','High')
        self.assertFalse(s.review_ready(self.app,state,self.inputs, companies=self.companies))

    def test_changed_ratings_cannot_reuse_a_prior_queue_score(self):
        for field in ['Career fit','Resume fit']:
            app={**self.app,field:'Low'}
            self.assertFalse(s.review_ready(app,self.state,self.inputs, companies=self.companies))

    def test_old_policy_label_cannot_bypass_current_scoring(self):
        inputs={**self.inputs,'policy':'review-v3'}
        state=copy.deepcopy(self.state);state['review']['inputs']=inputs
        self.assertFalse(s.review_ready(self.app,state,inputs, companies=self.companies))

    def test_ready_endpoint_rejects_protected_outcomes_even_with_a_verified_pdf(self):
        data=b'verified-pdf';digest=hashlib.sha256(data).hexdigest()
        app={**self.app,'Lifecycle status':'Ready','Resume link':'file-example','Resume version':digest,'Resume verified at':'2026-01-01'}
        state=copy.deepcopy(self.state);state['preparation']={'verified':True,'resume_hash':digest,'master':'master-v1','goals':'goals-v1','jd_hash':'jd-v1',**self.reuse(digest)}
        self.assertTrue(s.resume_verified(app,state,self.inputs,data, companies=self.companies))
        for status in ['Applied','Interviewing','Rejected','Not pursuing','Duplicate']:
            self.assertFalse(s.resume_verified({**app,'Lifecycle status':status},state,self.inputs,data,companies=self.companies))
        self.assertFalse(s.resume_verified({**app,'Submission attempt key':'legacy'},state,self.inputs,data,companies=self.companies))
        old=copy.deepcopy(state);old['submission']={'attempt_key':'legacy'}
        self.assertFalse(s.resume_verified(app,old,self.inputs,data,companies=self.companies))

    def test_exact_identity_does_not_merge_regional_or_same_title_roles(self):
        self.assertEqual(s.canonical_job_url('https://jobs.example.test/roles/a?utm_source=mail'),s.canonical_job_url('https://jobs.example.test/roles/a'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/?jobId=1'),s.canonical_job_url('https://jobs.example.test/?jobId=2'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/?ref=role-a'),s.canonical_job_url('https://jobs.example.test/?ref=role-b'))
        self.assertNotEqual(s.canonical_job_url('https://jobs.example.test/#/job/one'),s.canonical_job_url('https://jobs.example.test/#/job/two'))

    def test_ready_without_answer_check_is_prepared_again(self):
        ready={**self.app,'Lifecycle status':'Ready'}
        self.assertTrue(s.preparation_eligible(ready,{}))
        self.assertTrue(s.answer_check_due(ready,{'preparation':{}}))
        checked={'preparation':{'application_questions':{'schema':'nextmove.application-questions.v2'}}}
        self.assertFalse(s.preparation_eligible(ready,checked))
        self.assertFalse(s.preparation_eligible({**ready,'Lifecycle status':'Apply manually'},{}))
        self.assertTrue(s.preparation_eligible({**self.app,'Lifecycle status':'Queued'},checked))


    def test_explicit_user_request_lets_an_agent_queue_without_review(self):
        app={**self.app,'Lifecycle status':'Need review'}
        with self.assertRaises(ValueError):
            s.application_write({'Lifecycle status':'Queued'},existing_application=app,existing_state={})
        request={'quote':'Please queue the Stripe payouts role','observed_at':'2026-11-24T10:00:00Z'}
        self.assertEqual(s.application_write({'Lifecycle status':'Queued'},existing_application=app,existing_state={},human_request=request),{'Lifecycle status':'Queued'})
        with self.assertRaises(ValueError):
            s.application_write({'Lifecycle status':'Queued'},existing_application=app,existing_state={},human_request={'quote':' '})


if __name__ == '__main__':
    unittest.main()
