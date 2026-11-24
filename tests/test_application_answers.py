import copy
import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from application_answers import SCHEMA, answer_fingerprint, form_fingerprint, application_answers_ready, question_key
import stage_state
import test_stage_state


class AnswerReadinessTests(unittest.TestCase):
    def setUp(self):
        self.app = {'id': 'role-one', 'Company': ['company-one'], 'Job key': 'employer:one',
                    'Job description link': 'https://jobs.example.test/one'}
        self.bank = [{'id': 'answer-one', 'Question': 'Current location', 'Approved': True, 'Answer': 'Seattle, WA'}]
        self.narratives = [{'id': 'essay-one', 'Status': 'Resolved', 'Final answer': 'My grounded motivation.',
                            'Application': ['role-one']}]
        self.manifest = {'schema': SCHEMA, 'application_id': 'role-one', 'job_key': 'employer:one',
                         'job_url': self.app['Job description link'], 'form_url': 'https://jobs.example.test/one/apply',
                         'inspected_at': '2026-01-01T12:00:00Z', 'coverage': 'complete',
                         'evidence': 'Verified full form snapshot, including conditional fields', 'blockers': [],
                         'questions': []}
        self.add_question('location', 'Answer bank', self.bank[0])
        self.add_question('motivation', 'Application questions', self.narratives[0])

    def add_question(self, key, table, row, required=True):
        self.manifest['questions'].append({'field_key': key, 'question': key + '?',
            'type': 'Form' if table == 'Answer bank' else 'Narrative', 'required': required, 'options': [],
            'answer': {'table': table, 'record_id': row['id'], 'fingerprint': answer_fingerprint(table, row),
                       'mapped_answer': row.get('Answer') or row.get('Final answer'),
                       'mapping_verified': True, 'match_evidence': 'Same meaning, scope and valid options'}})
        self.manifest['form_hash'] = form_fingerprint(self.manifest['questions'])

    def ready(self):
        return application_answers_ready(self.app, self.manifest, self.bank, self.narratives,
                                         as_of='2026-01-01', current_form_hash=self.manifest['form_hash'])

    def test_requires_approved_form_and_resolved_final_narrative(self):
        self.assertTrue(self.ready())
        for target, key, value in [(self.bank[0], 'Approved', False),
                                   (self.narratives[0], 'Status', 'Needs answer'),
                                   (self.bank[0], 'Answer', ''), (self.narratives[0], 'Final answer', '')]:
            old = target[key]; target[key] = value
            self.assertFalse(self.ready()); target[key] = old

    def test_blank_from_source_rule_and_draft_essay_do_not_count(self):
        self.bank[0].update(Answer='', **{'Source field': 'goals.minimum'})
        self.assertFalse(self.ready())
        self.narratives[0].update(Status='Needs answer', **{'Draft answer': 'Generated draft'})
        self.assertFalse(self.ready())

    def test_live_edits_and_revoked_approval_invalidate_saved_handoff(self):
        self.bank[0]['Answer'] = 'Different location'; self.assertFalse(self.ready())
        self.bank[0]['Answer'] = 'Seattle, WA'; self.assertTrue(self.ready())
        self.narratives[0]['Final answer'] = 'Changed text'; self.assertFalse(self.ready())

    def test_guidance_edit_and_wrong_role_question_block(self):
        self.bank[0]['Guidance'] = 'Only for Snowflake'; self.assertFalse(self.ready())
        self.bank[0].pop('Guidance'); self.assertTrue(self.ready())
        self.narratives[0]['Application'] = ['other-role']; self.assertFalse(self.ready())

    def test_blocked_or_missing_inspection_never_means_zero_questions(self):
        for key, value in [('coverage', 'partial'), ('blockers', ['Login required']), ('evidence', ''),
                           ('job_url', 'https://jobs.example.test/two'), ('application_id', 'other-role')]:
            old = self.manifest[key]; self.manifest[key] = value
            self.assertFalse(self.ready()); self.manifest[key] = old
        self.assertFalse(application_answers_ready(self.app, None, [], [], as_of='2026-01-01'))

    def test_verified_empty_form_passes_and_new_conditional_required_field_blocks(self):
        self.manifest['questions'] = []; self.manifest['form_hash'] = form_fingerprint([])
        self.assertTrue(self.ready())
        self.manifest['questions'].append({'field_key': 'conditional', 'question': 'Follow up?',
                                           'type': 'Form', 'required': True, 'options': []})
        self.manifest['form_hash'] = form_fingerprint(self.manifest['questions'])
        self.assertFalse(self.ready())

    def test_optional_unanswered_question_does_not_block(self):
        self.manifest['questions'].append({'field_key': 'optional', 'question': 'Optional?',
                                           'type': 'Form', 'required': False, 'options': []})
        self.manifest['form_hash'] = form_fingerprint(self.manifest['questions'])
        self.assertTrue(self.ready())

    def test_question_option_changes_and_duplicate_field_keys_block(self):
        self.manifest['questions'][0]['options'] = ['New option']; self.assertFalse(self.ready())
        self.manifest['form_hash'] = form_fingerprint(self.manifest['questions'])
        self.manifest['questions'].append(copy.deepcopy(self.manifest['questions'][0]))
        self.manifest['form_hash'] = form_fingerprint(self.manifest['questions'])
        self.assertFalse(self.ready())

    def test_current_form_change_and_discovery_retry_identity(self):
        self.assertFalse(application_answers_ready(self.app, self.manifest, self.bank, self.narratives,
                         as_of='2026-01-01', current_form_hash='changed-live-form'))
        self.assertEqual(question_key('company-one', 'role-one', 'field-one'),
                         question_key('company-one', 'role-one', 'field-one'))
        self.assertNotEqual(question_key('company-one', 'role-one', 'field-one'),
                            question_key('company-one', 'role-two', 'field-one'))

    def test_ready_requires_resume_and_answers_and_live_records(self):
        fixture = test_stage_state.StateTests(); fixture.setUp()
        pdf = b'verified resume'; digest = hashlib.sha256(pdf).hexdigest()
        app, state = fixture.prepared(pdf, fixture.reuse(digest))
        app['Job description link'] = self.app['Job description link']
        app['id'] = self.app['id']; app['Job key'] = self.app['Job key']
        state.update(record_id=app['id'],job_key=app['Job key'])
        app['Company'] = ['company-one']
        companies = [{'id': 'company-one', 'Search status': 'Allow'}]
        inputs = {**fixture.inputs, 'answer_check_date': '2026-01-01', 'form_hash': self.manifest['form_hash']}
        self.assertTrue(stage_state.resume_verified(app, state, [fixture.run], inputs, pdf, companies=companies))
        self.assertFalse(stage_state.resume_ready(app, state, [fixture.run], inputs, pdf, companies=companies))
        state['preparation']['application_questions'] = self.manifest
        kwargs = {'companies': companies, 'answer_bank': self.bank, 'application_questions': self.narratives}
        self.assertTrue(stage_state.resume_ready(app, state, [fixture.run], inputs, pdf, **kwargs))
        self.assertFalse(stage_state.resume_ready({**app, 'Resume link': ''}, state, [fixture.run], inputs, pdf, **kwargs))
        self.bank[0]['Approved'] = False
        self.assertFalse(stage_state.resume_ready(app, state, [fixture.run], inputs, pdf, **kwargs))

    def test_prepare_outcome_is_ready_needs_answer_or_apply_manually(self):
        fixture = test_stage_state.StateTests(); fixture.setUp()
        pdf = b'verified resume'; digest = hashlib.sha256(pdf).hexdigest()
        app, state = fixture.prepared(pdf, fixture.reuse(digest))
        app.update({'Job description link': self.app['Job description link'], 'id': self.app['id'],
                    'Job key': self.app['Job key'], 'Company': ['company-one']})
        state.update(record_id=app['id'],job_key=app['Job key'])
        companies = [{'id': 'company-one', 'Search status': 'Allow'}]
        inputs = {**fixture.inputs, 'answer_check_date': '2026-01-01', 'form_hash': self.manifest['form_hash']}
        outcome = lambda a=app, st=state: stage_state.preparation_outcome(
            a, st, [fixture.run], inputs, pdf, companies=companies,
            answer_bank=self.bank, application_questions=self.narratives)
        state['preparation']['application_questions'] = self.manifest
        self.assertEqual(outcome(), 'Ready')
        self.assertEqual(outcome({**app, 'Lifecycle status': 'Needs answer'}), 'Ready')
        self.bank[0]['Approved'] = False
        self.assertEqual(outcome(), 'Needs answer')
        self.bank[0]['Approved'] = True
        self.assertEqual(outcome({**app, 'Resume link': ''}), 'Needs answer')
        blocked = copy.deepcopy(state)
        blocked['preparation']['application_questions'] = {**self.manifest, 'access': 'blocked', 'coverage': 'blocked',
            'blockers': [{'kind': 'sign_in_required', 'detail': 'Workday account sign-in before the form'}]}
        self.assertEqual(outcome(app, blocked), 'Apply manually')
        blocked['preparation']['application_questions']['blockers'] = [{'kind': 'unknown_branch', 'detail': 'Conditional page'}]
        self.assertEqual(outcome(app, blocked), 'Needs answer')
        self.assertEqual(outcome({**app, 'Resume link': ''}, blocked), 'Needs answer')


if __name__ == '__main__':
    unittest.main()
