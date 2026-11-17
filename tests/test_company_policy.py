import sys, unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from company_policy import (apply_allowed, compute_hold, funding_qualifies, quota_reopens_at,
                            scan_enabled, DEFAULT_PERSONAL_LIMIT)

NOW = datetime(2026, 11, 17, 12, tzinfo=timezone.utc)


def sub(day, kind='submission'):
    return {'kind': kind, 'at': datetime(2026, 11, day, 9, tzinfo=timezone.utc), 'key': kind + str(day)}


class CompanyPolicyTests(unittest.TestCase):
    def test_default_personal_limit_is_three_per_rolling_thirty_days(self):
        self.assertEqual(DEFAULT_PERSONAL_LIMIT, {'max_applications': 3, 'window_days': 30,
                                                  'window_type': 'Rolling', 'scope': 'Company'})
        assessed = {'Policy confidence': 'Not found'}
        self.assertEqual(compute_hold(assessed, [sub(1), sub(2)], NOW)['status'], 'No known hold')
        held = compute_hold(assessed, [sub(1), sub(2), sub(3)], NOW)
        self.assertEqual(held['status'], 'Held')
        self.assertEqual(held['blocked_until'], datetime(2026, 12, 1, 9, tzinfo=timezone.utc))

    def test_rolling_window_reopens_when_enough_events_expire(self):
        times = [NOW - timedelta(days=d) for d in (25, 20, 10, 5)]
        self.assertEqual(quota_reopens_at(times, 3, 30, NOW), times[1] + timedelta(days=30))
        self.assertIsNone(quota_reopens_at(times[2:], 3, 30, NOW))

    def test_uncertain_attempts_occupy_capacity_and_duplicates_count_once(self):
        events = [sub(1), sub(1), sub(2, 'uncertain_attempt'), sub(3)]
        self.assertEqual(compute_hold({'Policy confidence': 'Not found'}, events, NOW)['status'], 'Held')
        self.assertEqual(compute_hold({'Policy confidence': 'Not found'}, events[:3], NOW)['status'], 'No known hold')

    def test_date_only_events_are_conservative_without_timezone(self):
        result = compute_hold({'Policy confidence': 'Not found'},
                              [{'kind': 'submission', 'at': date(2026, 11, d)} for d in (1, 2, 3)], NOW)
        # Nov 1 ends at 11:59:59 UTC on Nov 2 in the latest zone; +30 days.
        self.assertEqual(result['blocked_until'], datetime(2026, 12, 2, 11, 59, 59, tzinfo=timezone.utc))

    def test_employer_rule_and_rejection_cooldown_need_enforceable_confidence(self):
        rule = {'Max applications': 1, 'Application window (days)': 90, 'Application window type': 'Rolling',
                'Restriction scope': 'Company', 'Rejection cooldown (days)': 180}
        rejected = [sub(1), {'kind': 'rejection', 'at': '2026-11-10T00:00:00Z'}]
        official = compute_hold(dict(rule, **{'Policy confidence': 'Official'}), rejected, NOW)
        self.assertEqual(official['status'], 'Held')
        self.assertEqual(official['blocked_until'], datetime(2027, 5, 9, tzinfo=timezone.utc))
        community = compute_hold(dict(rule, **{'Policy confidence': 'Community'}), [], NOW)
        self.assertEqual(community['status'], 'Needs clarification')

    def test_unclear_scope_or_reset_semantics_are_never_guessed(self):
        base = {'Policy confidence': 'Official', 'Max applications': 3, 'Application window (days)': 30}
        self.assertEqual(compute_hold(dict(base, **{'Restriction scope': 'Unconfirmed'}), [], NOW)['status'], 'Needs clarification')
        calendar = dict(base, **{'Restriction scope': 'Company', 'Application window type': 'Calendar'})
        self.assertEqual(compute_hold(calendar, [], NOW)['status'], 'Needs clarification')
        role = dict(base, **{'Restriction scope': 'Exact role'})
        self.assertEqual(compute_hold(role, [], NOW)['status'], 'No known hold')

    def test_only_verified_blocks_stop_apply(self):
        allowed, result = apply_allowed({'Application hold status': 'Blocked (permanent)', 'Policy confidence': 'User'}, [], NOW)
        self.assertFalse(allowed)
        self.assertEqual(result['status'], 'Blocked (permanent)')
        allowed, result = apply_allowed({}, [], NOW)
        self.assertTrue(allowed)
        self.assertEqual(result['status'], 'Not assessed')
        unclear = {'Policy confidence': 'Community', 'Max applications': 2, 'Application window (days)': 30,
                   'Application window type': 'Rolling', 'Restriction scope': 'Company'}
        allowed, result = apply_allowed(unclear, [], NOW)
        self.assertTrue(allowed)
        self.assertEqual(result['status'], 'Needs clarification')
        events = [{'kind': 'submission', 'at': NOW - timedelta(days=d)} for d in (1, 2, 3)]
        allowed, result = apply_allowed({'Policy confidence': 'Not found'}, events, NOW)
        self.assertFalse(allowed)
        self.assertEqual(result['status'], 'Held')
        self.assertTrue(apply_allowed({'Policy confidence': 'Not found'}, [], NOW)[0])

    def test_scan_reads_only_allowed_companies_without_permanent_block(self):
        self.assertTrue(scan_enabled({'Search status': 'Allow', 'Application hold status': 'Held'}))
        self.assertFalse(scan_enabled({'Search status': 'Allow', 'Application hold status': 'Blocked (permanent)'}))
        self.assertFalse(scan_enabled({'Search status': 'Proposed'}))
        self.assertFalse(scan_enabled({'Search status': 'Exclude'}))

    def test_funding_admission_is_series_c_or_later_and_unknown_fails(self):
        for stage in ['Series C', 'Series D', 'Series E+', 'Late private', 'Public']:
            self.assertTrue(funding_qualifies(stage))
        for stage in ['Pre-seed / Seed', 'Series A', 'Series B', 'Unknown', None]:
            self.assertFalse(funding_qualifies(stage))

    def test_naive_times_are_rejected(self):
        with self.assertRaises(ValueError):
            compute_hold({}, [], datetime(2026, 11, 17))


if __name__ == '__main__':
    unittest.main()
