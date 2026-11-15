"""Regression cases for costly false exclusions and premature admissions."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from role_gate import admission, base_maximum_gate, inventory_candidate, queue_allowed, title_screen


class AdmissionTests(unittest.TestCase):
    def test_typical_aliases_reach_verification(self):
        for title in ['Senior Product Manager', 'Director of Product', 'Principal Product Mgr', 'Product Management, Staff', 'Member of Product Staff', 'Lead Product Owner, Billing', 'Product Manager', 'Senior PM', 'VP Product']:
            with self.subTest(title=title):
                self.assertEqual(title_screen(title)['decision'], 'verify_jd')

    def test_product_word_is_not_enough(self):
        for title in ['Staff Product Designer', 'VP Product Marketing', 'Staff Software Engineer, Product', 'Product Support Director', 'Associate Product Manager', 'Senior Analyst, 9:30 PM to 6:30 AM shift', 'Software Engineering Intern - Engineering PM']:
            with self.subTest(title=title):
                self.assertEqual(title_screen(title)['decision'], 'reject')

    def test_missing_metadata_is_not_a_negative(self):
        self.assertEqual(title_screen('')['decision'], 'pending_metadata')
        self.assertEqual(title_screen('.')['decision'], 'pending_metadata')
        self.assertEqual(title_screen('Senior Produktmanager')['decision'], 'verify_jd')
        self.assertEqual(title_screen('Chef de produit')['decision'], 'verify_jd')

    def test_domain_word_does_not_override_pm_function(self):
        self.assertEqual(title_screen('Principal Product Manager, Product Design Platform')['decision'], 'verify_jd')
        self.assertEqual(title_screen('Principal PM, Design Systems')['decision'], 'verify_jd')

    def test_title_alone_cannot_admit(self):
        self.assertEqual(admission({'title': 'Principal Product Manager'}, years_threshold=8), 'pending')

    def test_evidence_and_scope_boundary(self):
        row = {'identity_verified': True, 'description_verified': True, 'availability_verified': True, 'role_family': 'product_management', 'role_evidence': 'Own product strategy and roadmap', 'experience_years_target': 10, 'experience_evidence': 'Ten-plus years required'}
        self.assertEqual(admission(row, years_threshold=8), 'pass')
        row['experience_years_target'] = 8
        self.assertEqual(admission(row, years_threshold=8), 'pending')
        row.update(equivalent_senior_scope=True, scope_evidence='Verified multi-product strategy ownership and PM-team leadership')
        self.assertEqual(admission(row, years_threshold=8), 'pass')
        row['equivalent_senior_scope'] = 'true'
        self.assertEqual(admission(row, years_threshold=8), 'pending')

    def test_goal_gate_is_separate(self):
        self.assertFalse(queue_allowed(role_decision='pass', career_decision='pending', career_evidence='', versions_current=True))
        self.assertFalse(queue_allowed(role_decision='pass', career_decision='pass', career_evidence='Aligned domain', versions_current=False))
        self.assertFalse(queue_allowed(role_decision='pass', career_decision='pass', career_evidence='Aligned domain', versions_current=True))
        self.assertTrue(queue_allowed(role_decision='pass', career_decision='pass', career_evidence='Aligned domain', versions_current=True, review_decision='approve'))

    def test_plausible_ambiguity_is_inventory_not_review_approval(self):
        row = {'title': 'Product Manager', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'ambiguous_pm',
               'basic_evidence': 'Official team owns platform roadmap; level unspecified'}
        self.assertEqual(inventory_candidate(row), 'pass')
        self.assertEqual(admission(row, years_threshold=8), 'pending')
        row['career_decision'] = 'fail'
        self.assertEqual(inventory_candidate(row), 'pass')
        row['basic_evidence'] = ''
        self.assertEqual(inventory_candidate(row), 'pending')

    def test_inventory_rejects_clear_semantic_mismatch(self):
        row = {'title': 'Senior Product Manager', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'other',
               'basic_evidence': 'Responsibilities exclusively marketing campaigns'}
        self.assertEqual(inventory_candidate(row), 'reject')
        row.update(role_hint='plausible_pm', clearly_junior=True,
                   basic_evidence='Official entry-level rotational role')
        self.assertEqual(inventory_candidate(row), 'reject')
        row.update(clearly_junior=False, identity_verified=False)
        self.assertEqual(inventory_candidate(row), 'pending')

    def test_official_context_can_resolve_missing_title(self):
        row = {'title': '', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'plausible_pm',
               'basic_evidence': 'Official function: product management; owns roadmap'}
        self.assertEqual(inventory_candidate(row), 'pass')

    def test_base_maximum_is_strict_and_not_band_minimum(self):
        row = {'minimum': 80000, 'maximum': 120000, 'currency': 'USD',
               'period': 'year', 'component': 'base',
               'base_upper_bound_verified': True, 'applicable_scope_verified': True,
               'source_evidence': 'Official annual base band for applicable location'}
        check = lambda: base_maximum_gate(row, threshold=100000, currency='USD', period='year')
        self.assertEqual(check(), 'pass')
        row['maximum'] = 100000
        self.assertEqual(check(), 'reject')
        row['maximum'] = 99000
        self.assertEqual(check(), 'reject')

    def test_salary_ambiguity_is_pending_not_negative(self):
        row = {'maximum': 120000, 'currency': 'USD', 'period': 'year',
               'component': 'base', 'base_upper_bound_verified': True,
               'applicable_scope_verified': True, 'source_evidence': 'Official band'}
        for key, value in [('maximum', None), ('maximum', float('nan')),
                           ('maximum', True), ('component', 'total'),
                           ('currency', 'EUR'), ('period', 'month'),
                           ('applicable_scope_verified', False),
                           ('base_upper_bound_verified', False), ('source_evidence', '')]:
            with self.subTest(key=key, value=value):
                changed = dict(row, **{key: value})
                self.assertEqual(base_maximum_gate(changed, threshold=100000,
                                                 currency='USD', period='year'), 'pending')


if __name__ == '__main__':
    unittest.main()
