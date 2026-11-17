"""Company targeting, funding admission and application-hold rules for Curate and Apply.

Pure functions only: no account access. Curate uses them to recompute holds; Apply uses
apply_allowed immediately before Submit, so both stages share one implementation.
"""
from datetime import date, datetime, time, timedelta, timezone

SEARCH_STATUSES = ['Proposed', 'Allow', 'Exclude']
HOLD_STATUSES = ['Not assessed', 'No known hold', 'Held', 'Blocked (permanent)', 'Needs clarification']
POLICY_CONFIDENCE = ['Official', 'Recruiter', 'User', 'Community', 'Not found']
ENFORCEABLE = {'Official', 'Recruiter', 'User'}
WINDOW_TYPES = ['Rolling', 'Calendar', 'Fixed', 'Unconfirmed']
RESTRICTION_SCOPES = ['Company', 'Role family', 'Exact role', 'Mixed', 'Unconfirmed']
# Ordered: a minimum stage admits every later stage. Unknown never qualifies.
FUNDING_STAGES = ['Pre-seed / Seed', 'Series A', 'Series B', 'Series C', 'Series D',
                  'Series E+', 'Late private', 'Public', 'Unknown']
_STAGE_RANK = {s: i for i, s in enumerate(FUNDING_STAGES[:-1])}
# Latest instant of a calendar date anywhere on Earth: conservative for date-only events.
_LATEST_ZONE = timezone(timedelta(hours=-12))

DEFAULT_PERSONAL_LIMIT = {'max_applications': 3, 'window_days': 30, 'window_type': 'Rolling', 'scope': 'Company'}


def funding_qualifies(stage, minimum='Series C'):
    """True only for a known stage at or after the configured minimum."""
    if stage not in _STAGE_RANK or minimum not in _STAGE_RANK:
        return False
    return _STAGE_RANK[stage] >= _STAGE_RANK[minimum]


def scan_enabled(company):
    """Scan reads only human-allowed companies that are not permanently blocked."""
    return (company.get('Search status') == 'Allow'
            and company.get('Application hold status') != 'Blocked (permanent)')


def company_for_application(application, companies):
    """Resolve one current named company; cached Allow IDs do not prove targeting."""
    linked = application.get('Company') or []
    if len(linked) != 1 or companies is None:
        return None
    matches = [company for company in companies if company.get('id') == linked[0]]
    return matches[0] if len(matches) == 1 and scan_enabled(matches[0]) else None


def _instant(value, tz=None):
    """Datetime -> aware UTC. Date-only -> end of that date in tz (or the latest zone)."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError('Naive datetimes are ambiguous; supply an offset')
        return value.astimezone(timezone.utc)
    if isinstance(value, date):
        return datetime.combine(value, time(23, 59, 59), tz or _LATEST_ZONE).astimezone(timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        return _instant(date.fromisoformat(text) if len(text) == 10 else datetime.fromisoformat(text.replace('Z', '+00:00')), tz)
    raise ValueError('Unsupported event time')


def _zone(name):
    if not name:
        return None
    from zoneinfo import ZoneInfo
    return ZoneInfo(name)


def _dedupe(events):
    seen, out = set(), []
    for e in events:
        key = e.get('key') or (e.get('kind'), str(e.get('at')))
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def quota_reopens_at(times, max_applications, window_days, now):
    """Return None if one more submission fits now, else when enough events expire.

    Counts events in (now - window, now]. One more is allowed when count < max. The window
    reopens when the (count - max + 1)th oldest event leaves it, not necessarily the oldest.
    """
    window = timedelta(days=window_days)
    live = sorted(t for t in times if now - window < t <= now)
    if len(live) < max_applications:
        return None
    return live[len(live) - max_applications] + window


def compute_hold(company, events, now, personal_limit=None, personal_timezone=None):
    """Recompute company-level hold from policy fields plus application events.

    events: dicts with kind 'submission' | 'uncertain_attempt' | 'rejection', at (datetime,
    date or ISO text) and optional key. Uncertain attempts occupy quota. Returns
    {'status', 'blocked_until', 'reasons'}; Curate writes status/blocked_until and Apply
    refuses unless status is 'No known hold'.
    """
    if now.tzinfo is None:
        raise ValueError('now must be timezone-aware')
    now = now.astimezone(timezone.utc)
    if company.get('Application hold status') == 'Blocked (permanent)':
        return {'status': 'Blocked (permanent)', 'blocked_until': None,
                'reasons': ['Permanent block; only the user removes it']}
    events = _dedupe(events)
    company_tz = _zone(company.get('Restriction timezone'))
    reasons, blocks, unresolved = [], [], []

    def times(kinds, tz):
        return [_instant(e['at'], tz) for e in events if e.get('kind') in kinds]

    submissions = ('submission', 'uncertain_attempt')
    limit = DEFAULT_PERSONAL_LIMIT if personal_limit is None else personal_limit
    if limit:
        until = quota_reopens_at(times(submissions, _zone(personal_timezone)),
                                 limit['max_applications'], limit['window_days'], now)
        if until:
            blocks.append(until)
            reasons.append('Personal limit %d per %d days reached; reopens %s'
                           % (limit['max_applications'], limit['window_days'], until.isoformat()))

    confidence = company.get('Policy confidence')
    has_rule = any(company.get(k) not in (None, '') for k in
                   ['Max applications', 'Application window (days)', 'Rejection cooldown (days)'])
    scope = company.get('Restriction scope')
    if has_rule and confidence not in ENFORCEABLE:
        unresolved.append('Recorded rule has %s confidence; confirm before enforcing' % (confidence or 'no'))
    elif has_rule and scope in {'Role family', 'Exact role'}:
        reasons.append('%s-scoped rule; Apply checks the affected roles' % scope)
    elif has_rule and scope != 'Company':
        unresolved.append('Restriction scope %s needs clarification' % (scope or 'blank'))
    elif has_rule:
        maximum, days = company.get('Max applications'), company.get('Application window (days)')
        if maximum or days:
            kind = company.get('Application window type')
            if not (maximum and days) or kind != 'Rolling':
                # Calendar/Fixed resets need boundaries from details; never guess them.
                unresolved.append('Quota needs count, days and Rolling semantics (or explicit reset boundaries)')
            else:
                until = quota_reopens_at(times(submissions, company_tz), int(maximum), int(days), now)
                if until:
                    blocks.append(until)
                    reasons.append('Employer limit %d per %d days reached; reopens %s'
                                   % (maximum, days, until.isoformat()))
        cooldown = company.get('Rejection cooldown (days)')
        if cooldown:
            rejected = [t for t in times(('rejection',), company_tz) if t <= now]
            if rejected:
                until = max(rejected) + timedelta(days=int(cooldown))
                if until > now:
                    blocks.append(until)
                    reasons.append('Rejection cooldown %d days; ends %s' % (cooldown, until.isoformat()))

    if blocks:
        return {'status': 'Held', 'blocked_until': max(blocks), 'reasons': reasons + unresolved}
    if unresolved:
        return {'status': 'Needs clarification', 'blocked_until': None, 'reasons': reasons + unresolved}
    if not confidence:
        return {'status': 'Not assessed', 'blocked_until': None,
                'reasons': reasons + ['Employer policy not yet researched by Curate']}
    return {'status': 'No known hold', 'blocked_until': None, 'reasons': reasons}


VERIFIED_BLOCKS = ('Held', 'Blocked (permanent)')


def apply_allowed(company, events, now, personal_limit=None, personal_timezone=None):
    """Apply preflight: recompute live; only a verified block stops Submit.

    Held (an enforceable employer rule or the user's personal limit is reached) and
    Blocked (permanent) stop the submission. Needs clarification and Not assessed do not:
    the careers site surfaces any real restriction during the application, and Apply then
    records it on the company row (stages/apply.md "Company application holds").
    """
    result = compute_hold(company, events, now, personal_limit, personal_timezone)
    return result['status'] not in VERIFIED_BLOCKS, result
