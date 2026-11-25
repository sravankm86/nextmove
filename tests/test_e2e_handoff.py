"""Logical handoffs only: no account, careers-site or real PDF validation."""
import hashlib
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from application_answers import SCHEMA, answer_fingerprint, form_fingerprint
from artifact_reader import select
from role_gate import inventory_candidate, review_frame_contract, scored_review
from stage_state import application_write, merge_state, payload, resolve, resume_ready, resume_verified


class EndToEndHandoffTests(unittest.TestCase):
    def build(self, separate):
        ids = dict(zip(['scan', 'review', 'preparation'], ['scan-run', 'review-run', 'prepare-run'])) if separate else dict.fromkeys(['scan', 'review', 'preparation'], 'full-run')
        company = {'id': 'company-one', 'Search status': 'Proposed', 'Company evidence': 'verified-company-capture'}
        app = {'id': 'role-one', 'Role': 'Senior Analyst', 'Company': ['company-one'],
               'Job key': 'employer:one', 'Job description link': 'https://jobs.example.test/one',
               'Lifecycle status': 'Inventoried', 'Manual notes': 'Keep my annotation.'}
        create = {k: v for k, v in app.items() if k not in {'id', 'Manual notes'}}
        with self.assertRaises(ValueError):
            application_write(create, creating=True, existing_keys=set(), companies=[company])
        company['Search status'] = 'Allow'  # Simulated explicit human checkpoint.
        family = {'name': 'analysis', 'direct_patterns': [r'\banalyst\b']}
        self.assertEqual(inventory_candidate({'identity_verified': True, 'title': app['Role'],
            'role_hint': 'plausible', 'basic_evidence': 'Owns the target analysis product charter'}, family), 'pass')
        application_write(create, creating=True, existing_keys=set(), companies=[company])
        jd = 'Complete exact fictional description'; jd_hash = hashlib.sha256(jd.encode()).hexdigest()
        state = merge_state(None, record_id=app['id'], job_key=app['Job key'], stage='scan',
                            run_id=ids['scan'], values={'jd_hash': jd_hash, 'current_description': True})
        capture = {'records': [{'record_id': app['id'], 'company': 'Example employer', 'role': app['Role'],
                    'source': {'description': jd, 'description_sha256': jd_hash,
                               'url': app['Job description link'], 'job_key': app['Job key']}}]}
        captured = select(json.loads(json.dumps(capture)), 'job', app['id'])
        self.assertEqual(captured['description_sha256'], jd_hash)
        state['source'] = {'description_sha256': jd_hash, 'role_id': 'employer-one'}
        state['details'] = {'file_id': 'capture-example', 'selector': {'record_id': app['id']},
                            'sha256': hashlib.sha256(json.dumps(capture).encode()).hexdigest()}
        app['Scan run'] = [ids['scan']]
        state = self.recover(app, state, '01')
        inputs = {'goals': 'goals-one', 'master': 'master-one', 'policy': review_frame_contract()[0],
                  'company_evidence': company['Company evidence'],
                  'jd_hash': jd_hash, 'resume_guidelines': 'guidelines-one', 'answer_check_date': '2026-01-01'}
        runs = [{'id': rid, 'Input versions (JSON)': json.dumps({'stage_inputs': {'review': inputs}})} for rid in set(ids.values())]
        # Run preflight is refreshed for a separately invoked Review, not inherited blindly.
        state['run_checks'] = {'duplicate': {'status': 'unique', 'checked_in_run': ids['review'],
                                            'evidence': 'Verified company-scoped employer role ID'}}
        state = merge_state(state, record_id=app['id'], job_key=app['Job key'], stage='review', run_id=ids['review'],
            values={'assessment_method': 'three_step_v1', 'decision': 'approve', 'jd_hash': jd_hash,
                    'current_description': True, 'assessment_complete': True,
                    'scoring': scored_review('High', 'Medium'), 'evidence': 'JD/goals/master qualification passages'})
        queue_values={'Career fit': 'High', 'Resume fit': 'Medium', 'Review run': [ids['review']], 'Lifecycle status': 'Queued'}
        application_write(queue_values, existing_application=app, existing_state=state,
                          runs=runs, current_inputs=inputs, companies=[company])
        app.update(queue_values)
        state = self.recover(app, state, '02')
        pdf = b'fictional already-verified PDF bytes'; digest = hashlib.sha256(pdf).hexdigest()
        state = merge_state(state, record_id=app['id'], job_key=app['Job key'], stage='preparation', run_id=ids['preparation'],
            values={'path': 'base_reuse', 'base': 'approved-base', 'base_version': digest,
                    'base_master': inputs['master'], 'coverage': 'complete', 'master': inputs['master'],
                    'goals': inputs['goals'], 'jd_hash': jd_hash, 'guidelines': inputs['resume_guidelines'],
                    'verified': True, 'resume_version': digest, 'company_consistency': 'not_applicable',
                    'company_history': {'status': 'complete', 'matches': 0, 'evidence': 'Verified empty relevant history'}})
        app.update({'Preparation run': [ids['preparation']], 'Resume link': 'https://files.example.test/resume.pdf',
                    'Resume version': digest, 'Resume verified at': '2026-01-01T12:00:00Z'})
        bank = [{'id': 'answer-one', 'Question': 'Current location', 'Answer': 'Seattle', 'Approved': True}]
        questions = [{'id': 'essay-one', 'Question': 'Why this role?', 'Final answer': 'Grounded final response.',
                      'Status': 'Resolved', 'Application': [app['id']]}]
        manifest = {'schema': SCHEMA, 'application_id': app['id'], 'job_key': app['Job key'],
                    'job_url': app['Job description link'], 'form_url': 'https://jobs.example.test/one/apply',
                    'inspected_at': '2026-01-01T12:00:00Z', 'coverage': 'complete',
                    'evidence': 'Verified exact full form capture', 'blockers': [], 'questions': []}
        for key, table, row, text in [('location', 'Answer bank', bank[0], 'Seattle'),
                                     ('motivation', 'Application questions', questions[0], 'Grounded final response.')]:
            manifest['questions'].append({'field_key': key, 'question': key+'?', 'options': [], 'required': True, 'sensitive': False,
                'type': 'Form' if table == 'Answer bank' else 'Narrative',
                'answer': {'table': table, 'record_id': row['id'], 'fingerprint': answer_fingerprint(table, row),
                           'mapped_answer': text, 'mapping_verified': True, 'match_evidence': 'Same intent and valid options'}})
        manifest['form_hash'] = form_fingerprint(manifest['questions']); inputs['form_hash'] = manifest['form_hash']
        return app, state, runs, inputs, pdf, [company], bank, questions, manifest

    def recover(self, app, state, suffix):
        event = {'Recorded at': '2026-01-01T12:00:'+suffix+'Z', 'Field changes (JSON)': json.dumps(payload([state]))}
        # Only persisted record-shaped JSON reaches the simulated next harness.
        restored = resolve(json.loads(json.dumps(app)), json.loads(json.dumps([event])))
        self.assertEqual(restored, state)
        return restored

    def test_single_agent_and_separate_stages_reach_the_same_ready_handoff(self):
        for separate in [False, True]:
            with self.subTest(separate=separate):
                app, state, runs, inputs, pdf, companies, bank, questions, manifest = self.build(separate)
                self.assertTrue(resume_verified(app, state, runs, inputs, pdf, companies=companies))
                self.assertFalse(resume_ready(app, state, runs, inputs, pdf, companies=companies,
                                              answer_bank=bank, application_questions=questions))
                state['preparation']['application_questions'] = manifest
                state = self.recover(app, state, '03')
                self.assertTrue(resume_ready(app, state, runs, inputs, pdf, companies=companies,
                                             answer_bank=bank, application_questions=questions))
                self.assertEqual(app['Manual notes'], 'Keep my annotation.')
                self.assertNotIn('Role eligibility', app)

    def test_saved_resume_survives_unanswered_form_but_cannot_advance(self):
        app, state, runs, inputs, pdf, companies, bank, questions, manifest = self.build(True)
        state['preparation']['application_questions'] = manifest
        bank[0]['Approved'] = False
        self.assertFalse(resume_ready(app, state, runs, inputs, pdf, companies=companies,
                                      answer_bank=bank, application_questions=questions))
        self.assertTrue(resume_verified(app, state, runs, inputs, pdf, companies=companies))
        self.assertEqual(app['Lifecycle status'], 'Queued')

    def test_manual_queue_recovers_in_another_harness_without_review_approval(self):
        app, state, runs, inputs, pdf, companies, bank, questions, manifest = self.build(False)
        state['preparation']['application_questions'] = manifest
        app.update({'Career fit':'Unresolved','Resume fit':'Low','Review run':[]})
        state.pop('review');state['stage_runs'].pop('review')
        state = self.recover(app, state, '04')
        self.assertTrue(resume_ready(app, state, [], inputs, pdf, companies=[],
                                    answer_bank=bank, application_questions=questions))
        bank[0]['Approved']=False
        self.assertFalse(resume_ready(app, state, [], inputs, pdf, companies=[],
                                     answer_bank=bank, application_questions=questions))
        with self.assertRaises(ValueError):
            application_write({'Role eligibility': 'Eligible'}, existing_application=app, existing_state=state)


if __name__ == '__main__':
    unittest.main()
