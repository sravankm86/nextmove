import json
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import answer_bank as a


class AnswerBankTests(unittest.TestCase):
    def test_phone_widget_formatting_preserves_every_digit(self):
        self.assertTrue(a.form_value_matches('identity.phone', '+15551234567', '+1 555-123-4567'))
        self.assertFalse(a.form_value_matches('identity.phone', '+15551234567', '5551234567'))
        self.assertFalse(a.form_value_matches('identity.phone', '+15551234567', '+15551234568'))
        self.assertFalse(a.form_value_matches('identity.email', 'a@example.com', 'b@example.com'))

    def test_connector_link_objects_use_ids(self):
        fields = [{'id': 'link-field', 'name': 'Company', 'type': 'multipleRecordLinks'},
                  {'id': 'select-field', 'name': 'Approval', 'type': 'singleSelect'}]
        row = a.normalize_record({'id': 'answer-one', 'cellValuesByFieldId': {
            'link-field': [{'id': 'company-one', 'name': 'Example'}],
            'select-field': {'id': 'choice-one', 'name': 'Approved'}}}, fields)
        self.assertEqual(row['Company'], ['company-one'])
        self.assertEqual(row['Approval'], 'Approved')

    def setUp(self):
        self.rule = {'id': 'answer-one', 'Topic': 'history.interviewed_here',
                     'Handling': 'Exact', 'Answer': 'No', 'Approval': 'Approved'}
        self.context = dict(company_id='company-one', application_id='role-one',
                            today='2026-11-17', mapping_verified=True, scope_verified=True)

    def run_rule(self, rules=None, **kwargs):
        return a.resolve(rules or [self.rule], self.rule['Topic'], **(self.context | kwargs))

    def test_no_approval_or_semantic_guess(self):
        self.assertEqual(self.run_rule(mapping_verified=False)['status'], 'Needs answer')
        self.assertEqual(self.run_rule(scope_verified=False)['status'], 'Needs answer')
        self.assertEqual(self.run_rule(contrary_evidence=True)['status'], 'Needs answer')
        self.rule['Approval'] = 'Draft'
        self.assertEqual(self.run_rule()['status'], 'Needs answer')

    def test_scope_and_ambiguity(self):
        other = self.rule | {'id': 'answer-two', 'Company': ['company-one'], 'Answer': 'Yes'}
        self.assertEqual(self.run_rule([self.rule, other])['answer'], 'Yes')
        self.assertEqual(self.run_rule([self.rule, other], company_id='company-two')['answer'], 'No')
        with self.assertRaises(ValueError):
            self.run_rule([self.rule, self.rule | {'id': 'answer-three'}])
        with self.assertRaises(ValueError):
            a.validate_rules([other | {'Application': ['role-one']}])

    def test_expired_specific_does_not_fall_back(self):
        specific = self.rule | {'id': 'specific', 'Application': ['role-one'], 'Valid until': '2026-11-01'}
        self.assertEqual(self.run_rule([self.rule, specific])['status'], 'Needs answer')

    def test_choice_changes_require_new_mapping(self):
        self.assertEqual(self.run_rule(options=['Yes', 'No'])['answer'], 'No')
        self.assertEqual(self.run_rule(options=['Citizen', 'Permanent resident'])['status'], 'Needs answer')
        key = a.field_key('https://example.com/apply', 'field', 'Question?', ['Yes', 'No'], 'select')
        self.assertNotEqual(key, a.field_key('https://example.com/apply', 'field', 'Question?', ['Other'], 'select'))
        existing = [{'id': 'question-one', 'Application': ['role-one'], 'Field key': key}]
        self.assertEqual(a.question_action(existing, 'role-one', key)['action'], 'reuse')
        with self.assertRaises(ValueError):
            a.question_action(existing * 2, 'role-one', key)

    def test_live_salary_and_units(self):
        self.rule.update(Topic='compensation.base_min', Handling='From source', Answer='',
                         **{'Source field': 'career_goals.minimum_base_salary'})
        source = {'verified': True, 'revision': 'goals-v1', 'value': 250000,
                  'currency': 'USD', 'period': 'annual', 'kind': 'base'}
        kwargs = dict(sources={'career_goals.minimum_base_salary': source},
                      expected_currency='USD', expected_kind='base', numeric=True)
        self.assertEqual(self.run_rule(**kwargs)['answer'], '250000')
        source.update(value=275000, revision='goals-v2')
        self.assertEqual(self.run_rule(**kwargs)['answer'], '275000')
        self.assertEqual(self.run_rule(**(kwargs | {'expected_currency': 'EUR'}))['status'], 'Needs answer')
        source['period'] = 'monthly'
        self.assertEqual(self.run_rule(**kwargs)['status'], 'Needs answer')

    def test_adaptation_and_multiple_choices(self):
        self.rule.update(Handling='Adapt', Answer='Approved office preferences')
        self.assertEqual(self.run_rule(proposed_answer=['West'], options=['West', 'East'], multiple=True)['status'], 'Needs answer')
        self.assertEqual(self.run_rule(proposed_answer=['West'], adaptation_supported=True,
                                      options=['West', 'East'], multiple=True)['answer'], ['West'])
        self.assertEqual(self.run_rule(proposed_answer=['Toronto'], adaptation_supported=True,
                                      options=['West'], multiple=True)['status'], 'Needs answer')

    def test_consent_needs_actual_policy_read(self):
        self.rule['Topic'] = 'consent.privacy'
        self.assertEqual(self.run_rule()['status'], 'Needs answer')
        self.assertEqual(self.run_rule(policy_read=True)['status'], 'Resolved')

    def test_resolved_question_cannot_self_approve(self):
        row = {'Question type': 'Form', 'Application': ['role-one'], 'Field key': 'key', 'Question': 'Question?',
               'Status': 'Resolved', 'Final answer': 'No', 'Answer rule': ['answer-one']}
        with self.assertRaises(ValueError):
            a.validate_question(row)
        a.validate_question(row, resolution=self.run_rule())
        with self.assertRaises(ValueError):
            a.validate_question(row | {'Final answer': 'Yes'}, resolution=self.run_rule())
        a.validate_question(row, user_approved=True)

    def test_form_final_must_be_an_offered_option(self):
        row = {'Question type': 'Form', 'Application': ['role-one'], 'Field key': 'key', 'Question': 'Team size?',
               'Status': 'Resolved', 'Options': json.dumps(['1-4 engineers', '10+ engineers'])}
        a.validate_question(row | {'Final answer': '10+ engineers'}, user_approved=True)
        with self.assertRaises(ValueError):
            a.validate_question(row | {'Final answer': '10+ engineers.'}, user_approved=True)
        multi = row | {'Options': json.dumps(['New York', 'Toronto', 'Austin'])}
        a.validate_question(multi | {'Final answer': json.dumps(['New York', 'Austin'])}, user_approved=True)
        with self.assertRaises(ValueError):
            a.validate_question(multi | {'Final answer': json.dumps(['New York', 'Boston'])}, user_approved=True)
        a.validate_question(row | {'Options': '[]', 'Final answer': 'Free text'}, user_approved=True)

    def test_narratives_cannot_enter_the_form_bank(self):
        with self.assertRaises(ValueError):
            a.validate_rules([self.rule | {'Topic': 'narrative.example'}])

    def test_grounded_draft_preserves_the_approved_final(self):
        row = {'id': 'question-one', 'Question type': 'Narrative', 'Application': ['role-one'],
               'Question': 'Describe a launch', 'Field key': 'key', 'Final answer': 'Previously approved text',
               'Status': 'Resolved'}
        sources = [{'kind': 'previous_question', 'reference': 'question-two', 'revision': 'sha256-of-text'}]
        with self.assertRaises(ValueError):
            a.narrative_draft(row, 'New draft', sources)
        draft = a.narrative_draft(row, 'New draft', sources, claims_verified=True,
                                 context_verified=True, policy_allows_drafting=True)
        self.assertEqual(draft['Status'], 'Needs answer')
        self.assertEqual(draft['Final answer'], 'Previously approved text')
        self.assertEqual(draft['Draft answer'], 'New draft')
        with self.assertRaises(ValueError):
            a.validate_question(draft | {'Status': 'Resolved'})
        with self.assertRaises(ValueError):
            a.narrative_draft(row, 'Unsupported draft', [], claims_verified=True,
                              context_verified=True, policy_allows_drafting=True)

    def test_form_answers_are_not_essays(self):
        row = {'Question type': 'Form', 'Application': ['role-one'], 'Question': 'Eligible?',
               'Field key': 'key', 'Status': 'Needs answer'}
        with self.assertRaises(ValueError):
            a.narrative_draft(row, 'Invented rationale', [], claims_verified=True,
                              context_verified=True, policy_allows_drafting=True)

    def test_reusable_narratives_do_not_require_a_fake_application(self):
        row = {'id': 'example-one', 'Question type': 'Narrative', 'Question': 'A launch example',
               'Field key': 'example-key', 'Status': 'Resolved', 'Final answer': 'Approved example'}
        a.validate_question(row, user_approved=True)
        self.assertEqual(a.question_action([row], None, 'example-key')['action'], 'reuse')
        with self.assertRaises(ValueError):
            a.validate_question(row | {'Question type': 'Form'}, user_approved=True)


if __name__ == '__main__':
    unittest.main()
