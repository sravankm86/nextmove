import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from company_policy import company_for_application, scan_enabled
from role_gate import review_frame_contract, scored_review
from stage_state import application_write, merge_company_state, payload, resolve, review_ready, run_progress


class CurateHandoffTests(unittest.TestCase):
    def setUp(self):
        self.company = {'id': 'company-example', 'Search status': 'Allow',
                        'Application hold status': 'Held', 'Funding stage': 'Series B'}
        self.candidate = {'Company': ['company-example'], 'Job key': 'employer:role',
                          'Role': 'Senior Product Manager', 'Lifecycle status': 'Inventoried',
                          'Role eligibility': 'Pending'}

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

    def test_curate_snapshot_recovers_without_an_application_or_job_key(self):
        values = {'company_research': {'status': 'Partial'},
                  'discovery': {'status': 'Blocked', 'pending_feeds': ['feed-example']},
                  'funding': {'stage': 'Series C', 'amount': '$100M', 'event_date': '2025-12-01',
                              'source': 'official-announcement', 'retrieved_at': '2026-01-01'},
                  'company_fit': {'rating': 'High', 'reason': 'Meets stated company preferences'},
                  'origin': 'Discovered'}
        state = merge_company_state(None, company_id=self.company['id'], company_key='employer',
                                    run_id='curate-run', values=values)
        event = {'Recorded at': '2026-01-01', 'Field changes (JSON)': json.dumps(payload([state]))}
        recovered = resolve(self.company, [event])
        self.assertEqual(recovered, state)
        self.assertNotIn('job_key', state)
        self.assertEqual(state['stage_runs']['curate'], 'curate-run')
        with self.assertRaises(ValueError):
            merge_company_state(state, company_id='other', company_key='other', run_id='next', values={})

    def test_partial_curate_progress_survives_later_scan_completion(self):
        stages = {'curate': {'status': 'Partial', 'discovery': {'pending_feeds': ['feed-example']}},
                  'scan': {'status': 'Complete'}}
        run = {'Checkpoint (JSON)': json.dumps({'stages': stages})}
        self.assertEqual(run_progress(run)['stages'], stages)

    def test_review_uses_current_targeting_and_decisive_company_evidence(self):
        policy, contract = review_frame_contract()
        inputs = {'goals': 'g', 'master': 'm', 'policy': policy, 'eligibility_policy': 'e',
                  'company_evidence': 'funding-capture-v1', 'jd_hash': 'jd'}
        run = {'id': 'review-run', 'Input versions (JSON)': {'stage_inputs': {'review': inputs}}}
        app = {'id': 'role', 'Company': [self.company['id']], 'Lifecycle status': 'Queued',
               'Role eligibility': 'Eligible', 'Career fit': 'High', 'Resume fit': 'Medium',
               'Review run': ['review-run']}
        state = {'stage_runs': {'review': 'review-run'},
                 'run_checks': {'duplicate': {'status': 'unique', 'checked_in_run': 'review-run', 'evidence': 'official ID'}},
                 'review': {'assessment_method': contract['assessment_method'], 'decision': 'approve',
                            'scoring': scored_review('High', 'Medium'), 'assessment_complete': True,
                            'evidence': 'JD/goals/master/company findings', 'jd_hash': 'jd', 'current_description': True}}
        frozen = copy.deepcopy(state)
        self.assertTrue(review_ready(app, state, [run], inputs, companies=[self.company]))
        # Hold changes do not change accepted fit or require Curate policy/discovery completion.
        for status in ['Held', 'Not assessed', 'Needs clarification', 'No known hold']:
            self.assertTrue(review_ready(app, state, [run], inputs,
                                         companies=[{**self.company, 'Application hold status': status}]))
        for changes in [{'Search status': 'Proposed'}, {'Search status': 'Exclude'},
                        {'Application hold status': 'Blocked (permanent)'}]:
            self.assertFalse(review_ready(app, state, [run], inputs, companies=[{**self.company, **changes}]))
        self.assertFalse(review_ready(app, state, [run], {**inputs, 'company_evidence': 'funding-capture-v2'},
                                      companies=[self.company]))
        self.assertFalse(review_ready(app, state, [run], inputs))
        missing = {k: value for k, value in inputs.items() if k != 'company_evidence'}
        self.assertFalse(review_ready(app, state, [run], missing, companies=[self.company]))
        self.assertEqual(state, frozen)  # Scope skips preserve scores, history and lifecycle.


if __name__ == '__main__':
    unittest.main()
