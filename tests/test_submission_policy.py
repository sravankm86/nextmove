import sys, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from submission_policy import DEFAULT_POLICY, ats_family, policy_problems, submission_gate

NOW = datetime(2026, 11, 20, 12, tzinfo=timezone.utc)
OPEN = {'Pause applications': False, 'Stop all': False}
URL = 'https://boards.greenhouse.io/example/jobs/123'


def policy(**changes):
    p = {**DEFAULT_POLICY, 'enabled': True, 'mode': 'submit', 'authorized_by': 'user', 'authorized_at': '2026-11-18T00:00:00Z',
         'expires_at': '2026-12-18T00:00:00Z', 'caps': {'per_run': 3, 'per_day': 5, 'per_week': 15},
         'allowed_ats': ['greenhouse', 'lever'], 'supervised_first_per_ats': 1}
    p.update(changes)
    return p


def done(days_ago, ats='greenhouse', outcome='submitted'):
    return {'at': NOW - timedelta(days=days_ago), 'ats': ats, 'outcome': outcome}


class SubmissionPolicyTests(unittest.TestCase):
    def test_defaults_never_submit(self):
        self.assertFalse(DEFAULT_POLICY['enabled'])
        self.assertEqual(DEFAULT_POLICY['mode'], 'preflight')
        decision, reasons = submission_gate(DEFAULT_POLICY, now=NOW, controls=OPEN, url=URL, history=[], run={})
        self.assertEqual(decision, 'preflight_only')
        self.assertTrue(reasons)

    def test_ats_families(self):
        self.assertEqual(ats_family('https://jobs.lever.co/acme/1'), 'lever')
        self.assertEqual(ats_family('https://acme.wd5.myworkdayjobs.com/x'), 'workday')
        self.assertEqual(ats_family('https://careers.example.com/apply'), 'careers.example.com')
        self.assertIsNone(ats_family(''))

    def test_first_submission_per_ats_needs_confirmation_then_runs_unattended(self):
        decision, _ = submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=[], run={})
        self.assertEqual(decision, 'needs_confirmation')
        decision, reasons = submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=[done(3)], run={})
        self.assertEqual((decision, reasons), ('submit', []))

    def test_controls_expiry_and_unlisted_ats_block(self):
        history = [done(3)]
        for controls in [{'Pause applications': True, 'Stop all': False}, {'Pause applications': False, 'Stop all': True}, {}]:
            self.assertEqual(submission_gate(policy(), now=NOW, controls=controls, url=URL, history=history, run={})[0], 'preflight_only')
        self.assertEqual(submission_gate(policy(expires_at='2026-11-19T00:00:00Z'), now=NOW, controls=OPEN, url=URL, history=history, run={})[0], 'preflight_only')
        self.assertEqual(submission_gate(policy(), now=NOW, controls=OPEN, url='https://acme.wd1.myworkdayjobs.com/a', history=history, run={})[0], 'preflight_only')

    def test_caps_count_uncertain_attempts(self):
        week = [done(d) for d in (1.5, 2, 3, 4, 5)] + [done(6, outcome='uncertain')] * 9 + [done(6.5)]
        self.assertIn('weekly cap 15 reached', submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=week, run={})[1])
        today = [done(0.1)] * 4 + [done(0.2, outcome='uncertain')]
        self.assertIn('daily cap 5 reached', submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=today, run={})[1])
        self.assertIn('per-run cap 3 reached', submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=[done(3)], run={'submitted': 3})[1])

    def test_circuit_breaker_and_pacing(self):
        history = [done(3)]
        self.assertEqual(submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=history, run={'uncertain': 1})[0], 'preflight_only')
        self.assertEqual(submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=history, run={'consecutive_failures': 2})[0], 'preflight_only')
        self.assertEqual(submission_gate(policy(), now=NOW, controls=OPEN, url=URL, history=history, run={'last_submit_at': NOW - timedelta(minutes=2)})[0], 'preflight_only')

    def test_unsafe_policies_are_rejected(self):
        self.assertTrue(policy_problems(policy(allow_credential_entry=True)))
        self.assertTrue(policy_problems(policy(unknown_required_question='best_guess')))
        self.assertTrue(policy_problems(policy(expires_at=None)))
        self.assertTrue(policy_problems(policy(caps={'per_run': 0, 'per_day': 5, 'per_week': 10})))
        self.assertEqual(policy_problems(policy()), [])


if __name__ == '__main__':
    unittest.main()
