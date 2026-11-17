import sys, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from submission_policy import DEFAULT_POLICY, policy_problems, submission_gate

NOW = datetime(2026, 11, 20, 12, tzinfo=timezone.utc)
ON = {'Pause applications': False, 'Stop all': False}


def done(hours_ago, outcome='submitted'):
    return {'at': NOW - timedelta(hours=hours_ago), 'outcome': outcome}


class SubmissionPolicyTests(unittest.TestCase):
    def test_defaults_never_submit(self):
        self.assertEqual(DEFAULT_POLICY, {'max_per_day': 0})
        self.assertEqual(submission_gate(DEFAULT_POLICY, now=NOW, controls=ON, history=[], run={})[0], 'preflight_only')

    def test_daily_limit_counts_unclear_attempts(self):
        policy = {'max_per_day': 3}
        self.assertEqual(submission_gate(policy, now=NOW, controls=ON, history=[done(2), done(30)], run={}), ('submit', []))
        decision, reasons = submission_gate(policy, now=NOW, controls=ON, history=[done(1), done(2), done(3, 'uncertain')], run={})
        self.assertEqual((decision, reasons), ('preflight_only', ['daily limit 3 reached']))

    def test_pause_stop_and_unclear_submission_block(self):
        policy = {'max_per_day': 5}
        for controls in [{'Pause applications': True, 'Stop all': False}, {'Pause applications': False, 'Stop all': True}, {}]:
            self.assertEqual(submission_gate(policy, now=NOW, controls=controls, history=[], run={})[0], 'preflight_only')
        self.assertEqual(submission_gate(policy, now=NOW, controls=ON, history=[], run={'uncertain': 1})[0], 'preflight_only')

    def test_invalid_limit_is_rejected(self):
        for bad in [{}, {'max_per_day': -1}, {'max_per_day': 'five'}, {'max_per_day': True}]:
            self.assertTrue(policy_problems(bad))
            self.assertEqual(submission_gate(bad, now=NOW, controls=ON, history=[], run={})[0], 'preflight_only')


if __name__ == '__main__':
    unittest.main()
