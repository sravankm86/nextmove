import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from company_policy import company_for_application, scan_enabled
from role_gate import review_frame_contract, scored_review
from stage_state import application_write, review_ready


class CurateHandoffTests(unittest.TestCase):
    def setUp(self):
        self.company = {'id': 'company-example', 'Search status': 'Allow',
                        'Application hold status': 'Held', 'Funding stage': 'Series B'}
        self.candidate = {'Company': ['company-example'], 'Job key': 'employer:role',
                          'Role': 'Senior Product Manager', 'Lifecycle status': 'Inventoried'}

    def test_temporary_hold_and_below_preference_funding_do_not_filter_inventory(self):
        for status in ['Held', 'Not assessed', 'Needs clarification', 'No known hold']:
            company = {**self.company, 'Application hold status': status}
            self.assertTrue(scan_enabled(company))
            self.assertEqual(application_write(self.candidate, creating=True, existing_keys=set(),
                                              companies=[company]), self.candidate)

    def test_stale_allow_ids_cannot_bypass_a_live_scope_change(self):
        for changed in [{'Search status': 'Proposed'}, {'Search status': 'Exclude'},
                        {'Application hold status': 'Blocked (permanent)'}]:
            with self.assertRaises(ValueError):
                application_write(self.candidate, creating=True, existing_keys=set(),
                                  allowed_companies={'company-example'}, companies=[{**self.company, **changed}])
        with self.assertRaises(ValueError):
            application_write(self.candidate, creating=True, existing_keys=set(),
                              allowed_companies={'company-example'})

    def test_missing_or_conflicting_company_identity_never_advances(self):
        self.assertIsNone(company_for_application(self.candidate, []))
        self.assertIsNone(company_for_application(self.candidate, [self.company, self.company]))
        self.assertIsNone(company_for_application({'Company': ['other']}, [self.company]))

    def test_review_uses_current_targeting_and_decisive_company_evidence(self):
        policy, contract = review_frame_contract()
        inputs = {'goals': 'g', 'master': 'm', 'policy': policy,
                  'company_evidence': 'funding-capture-v1', 'jd_hash': 'jd'}
        app = {'id': 'role', 'Company': [self.company['id']], 'Lifecycle status': 'Queued', 'Career fit': 'High', 'Resume fit': 'Medium'}
        state = {'run_checks': {'duplicate': {'status': 'unique', 'checked_at': '2026-01-01', 'evidence': 'official ID'}},
                 'review': {'assessment_method': contract['assessment_method'], 'decision': 'approve',
                            'scoring': scored_review('High', 'Medium'), 'assessment_complete': True,
                            'evidence': 'JD/goals/master/company findings', 'jd_hash': 'jd', 'current_description': True,
                            'inputs': inputs}}
        frozen = copy.deepcopy(state)
        self.assertTrue(review_ready(app, state, inputs, companies=[self.company]))
        # Hold changes do not change accepted fit or require Curate policy/discovery completion.
        for status in ['Held', 'Not assessed', 'Needs clarification', 'No known hold']:
            self.assertTrue(review_ready(app, state, inputs,
                                         companies=[{**self.company, 'Application hold status': status}]))
        for changes in [{'Search status': 'Proposed'}, {'Search status': 'Exclude'},
                        {'Application hold status': 'Blocked (permanent)'}]:
            self.assertFalse(review_ready(app, state, inputs, companies=[{**self.company, **changes}]))
        self.assertFalse(review_ready(app, state, {**inputs, 'company_evidence': 'funding-capture-v2'},
                                      companies=[self.company]))
        self.assertFalse(review_ready(app, state, inputs))
        missing = {k: value for k, value in inputs.items() if k != 'company_evidence'}
        self.assertFalse(review_ready(app, state, missing, companies=[self.company]))
        self.assertEqual(state, frozen)  # Scope skips preserve scores, history and lifecycle.


if __name__ == '__main__':
    unittest.main()
