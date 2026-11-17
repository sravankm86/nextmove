"""Regression cases for costly false exclusions and premature admissions."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from role_gate import inventory_candidate, review_eligibility, title_screen


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

    def test_posting_availability_is_not_an_inventory_or_review_requirement(self):
        row = {'identity_verified': True, 'title': 'Senior Product Manager',
               'role_hint': 'plausible_pm', 'basic_evidence': 'Own the roadmap',
               'description_verified': True, 'role_family': 'product_management',
               'role_evidence': 'Own product strategy', 'experience_years_target': 10,
               'experience_evidence': 'Ten years required'}
        for value in [None, False, True]:
            with self.subTest(availability=value):
                candidate = {**row, 'availability_verified': value}
                self.assertEqual(inventory_candidate(candidate), 'pass')
                self.assertEqual(review_eligibility(candidate, years_threshold=8), 'pass')
        self.assertEqual(inventory_candidate({**row, 'identity_verified': False}), 'pending')
        self.assertEqual(review_eligibility({**row, 'description_verified': False}, years_threshold=8), 'pending')

    def test_title_alone_cannot_admit(self):
        self.assertEqual(review_eligibility({'title': 'Principal Product Manager'}, years_threshold=8), 'pending')

    def test_evidence_and_scope_boundary(self):
        row = {'identity_verified': True, 'description_verified': True, 'availability_verified': True, 'role_family': 'product_management', 'role_evidence': 'Own product strategy and roadmap', 'experience_years_target': 10, 'experience_evidence': 'Ten-plus years required'}
        self.assertEqual(review_eligibility(row, years_threshold=8), 'pass')
        row['experience_years_target'] = 8
        self.assertEqual(review_eligibility(row, years_threshold=8), 'pending')
        row.update(equivalent_senior_scope=True, scope_evidence='Verified multi-product strategy ownership and PM-team leadership')
        self.assertEqual(review_eligibility(row, years_threshold=8), 'pass')
        row['equivalent_senior_scope'] = 'true'
        self.assertEqual(review_eligibility(row, years_threshold=8), 'pending')

    def test_plausible_ambiguity_is_inventory_not_review_approval(self):
        row = {'title': 'Product Manager', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'ambiguous_pm',
               'basic_evidence': 'Official team owns platform roadmap; level unspecified'}
        self.assertEqual(inventory_candidate(row), 'pass')
        self.assertEqual(review_eligibility(row, years_threshold=8), 'pending')
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

class QualificationTests(unittest.TestCase):
    def q(self,status):
        return {'status':status,'evidence':'Exact source or confirmed candidate evidence' if status!='unknown' else None}
    def test_pay_with_meaningful_ownership_can_support_scope(self):
        evidence={'identity_verified':True,'description_verified':True,'role_family':'product_management','role_evidence':'Own end-to-end roadmap','pay_supported_scope':True,'meaningful_pm_ownership':True,'role_specific_pay_evidence':'Applicable senior band','scope_evidence':'Strategy and multi-team product accountability'}
        self.assertEqual(review_eligibility(evidence,years_threshold=8),'pass')
        evidence['meaningful_pm_ownership']=False
        self.assertEqual(review_eligibility(evidence,years_threshold=8),'pending')

if __name__ == '__main__':
    unittest.main()
