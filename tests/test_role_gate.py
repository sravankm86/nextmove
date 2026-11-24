"""Regression cases for costly false exclusions and premature admissions."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import json
from role_gate import inventory_candidate, role_family, title_screen

_EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / 'templates' / 'role-family.example.json').read_text())
FAMILY = role_family({k: v for k, v in _EXAMPLE.items() if k != 'examples'})
NAME = FAMILY['name']


class AdmissionTests(unittest.TestCase):
    def test_typical_aliases_reach_verification(self):
        for title in ['Senior Product Manager', 'Director of Product', 'Principal Product Mgr', 'Product Management, Staff', 'Member of Product Staff', 'Lead Product Owner, Billing', 'Product Manager', 'Senior PM', 'VP Product']:
            with self.subTest(title=title):
                self.assertEqual(title_screen(title, FAMILY)['decision'], 'verify_jd')

    def test_product_word_is_not_enough(self):
        for title in ['Staff Product Designer', 'VP Product Marketing', 'Staff Software Engineer, Product', 'Product Support Director', 'Associate Product Manager', 'Senior Analyst, 9:30 PM to 6:30 AM shift', 'Software Engineering Intern - Engineering PM']:
            with self.subTest(title=title):
                self.assertEqual(title_screen(title, FAMILY)['decision'], 'reject')

    def test_missing_metadata_is_not_a_negative(self):
        self.assertEqual(title_screen('', FAMILY)['decision'], 'pending_metadata')
        self.assertEqual(title_screen('.', FAMILY)['decision'], 'pending_metadata')
        self.assertEqual(title_screen('Senior Produktmanager', FAMILY)['decision'], 'verify_jd')
        self.assertEqual(title_screen('Chef de produit', FAMILY)['decision'], 'verify_jd')

    def test_domain_word_does_not_override_pm_function(self):
        self.assertEqual(title_screen('Principal Product Manager, Product Design Platform', FAMILY)['decision'], 'verify_jd')
        self.assertEqual(title_screen('Principal PM, Design Systems', FAMILY)['decision'], 'verify_jd')

    def test_posting_availability_is_not_an_inventory_or_review_requirement(self):
        row = {'identity_verified': True, 'title': 'Senior Product Manager',
               'role_hint': 'plausible', 'basic_evidence': 'Own the roadmap',
               'description_verified': True, 'role_family': NAME,
               'role_evidence': 'Own product strategy', 'experience_years_target': 10,
               'experience_evidence': 'Ten years required'}
        for value in [None, False, True]:
            with self.subTest(availability=value):
                candidate = {**row, 'availability_verified': value}
                self.assertEqual(inventory_candidate(candidate, FAMILY), 'pass')
        self.assertEqual(inventory_candidate({**row, 'identity_verified': False}, FAMILY), 'pending')

    def test_title_alone_cannot_admit(self):
        self.assertEqual(inventory_candidate({'title': 'Principal Product Manager'}, FAMILY), 'pending')

    def test_plausible_ambiguity_is_inventory_not_review_approval(self):
        row = {'title': 'Product Manager', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'ambiguous',
               'basic_evidence': 'Official team owns platform roadmap; level unspecified'}
        self.assertEqual(inventory_candidate(row, FAMILY), 'pass')
        row['career_decision'] = 'fail'
        self.assertEqual(inventory_candidate(row, FAMILY), 'pass')
        row['basic_evidence'] = ''
        self.assertEqual(inventory_candidate(row, FAMILY), 'pending')

    def test_inventory_rejects_clear_semantic_mismatch(self):
        row = {'title': 'Senior Product Manager', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'other',
               'basic_evidence': 'Responsibilities exclusively marketing campaigns'}
        self.assertEqual(inventory_candidate(row, FAMILY), 'reject')
        row.update(role_hint='plausible', clearly_junior=True,
                   basic_evidence='Official entry-level rotational role')
        self.assertEqual(inventory_candidate(row, FAMILY), 'reject')
        row.update(clearly_junior=False, identity_verified=False)
        self.assertEqual(inventory_candidate(row, FAMILY), 'pending')

    def test_official_context_can_resolve_missing_title(self):
        row = {'title': '', 'identity_verified': True,
               'availability_verified': True, 'role_hint': 'plausible',
               'basic_evidence': 'Official function: product management; owns roadmap'}
        self.assertEqual(inventory_candidate(row, FAMILY), 'pass')

if __name__ == '__main__':
    unittest.main()
