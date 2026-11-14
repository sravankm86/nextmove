"""Regression cases for costly false exclusions and premature admissions."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from role_gate import admission, queue_allowed, title_screen


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
        self.assertTrue(queue_allowed(role_decision='pass', career_decision='pass', career_evidence='Aligned domain', versions_current=True))


if __name__ == '__main__':
    unittest.main()
