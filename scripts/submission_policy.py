"""Standing submission authorization for Apply: one human approval, bounded autonomy.

Settings.submission_policy holds the policy below. The user sets it; agents never edit it.
These pure functions decide whether a browser agent may press Submit for one role right now.
They do not replace scripts/stage_state.py:apply_ready, the company hold check
(scripts/company_policy.py:apply_allowed) or the live Pause applications / Stop all controls;
all of them must pass.
"""
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

DEFAULT_POLICY = {
    'enabled': False,                 # master switch for real submissions
    'mode': 'preflight',              # 'preflight' (never submit) or 'submit'
    'authorized_by': None,            # who approved this policy
    'authorized_at': None,            # ISO8601 time of approval
    'expires_at': None,               # ISO8601; required for 'submit'
    'caps': {'per_run': 0, 'per_day': 0, 'per_week': 0},
    'allowed_ats': [],                # ATS families or exact hosts, e.g. ['greenhouse', 'lever']
    'supervised_first_per_ats': 1,    # submissions per ATS family that need a human go-ahead first
    'min_minutes_between_submissions': 5,
    'circuit_breaker': {'consecutive_failures': 2, 'uncertain_submissions': 1},
    'allow_account_creation': False,
    'allow_credential_entry': False,
    'unknown_required_question': 'stop',   # never guess
    'optional_question_without_answer': 'leave_blank',
    'cover_letter': 'only_if_prepared',    # never write one on the fly
}

# Hostname suffix -> ATS family. Unknown hosts are their own family (the bare host).
ATS_FAMILIES = {
    'greenhouse.io': 'greenhouse', 'lever.co': 'lever', 'ashbyhq.com': 'ashby',
    'myworkdayjobs.com': 'workday', 'myworkdaysite.com': 'workday', 'smartrecruiters.com': 'smartrecruiters',
    'icims.com': 'icims', 'workable.com': 'workable', 'jobvite.com': 'jobvite', 'bamboohr.com': 'bamboohr',
}


def ats_family(url):
    """Classify an application URL by ATS family, or return its bare host."""
    host = (urlsplit(url or '').hostname or '').lower().removeprefix('www.')
    if not host:
        return None
    for suffix, family in ATS_FAMILIES.items():
        if host == suffix or host.endswith('.' + suffix):
            return family
    return host


def _time(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    return datetime.fromisoformat(str(value).replace('Z', '+00:00')).astimezone(timezone.utc)


def policy_problems(policy):
    """Structural problems that make a 'submit' policy unusable."""
    p = {**DEFAULT_POLICY, **(policy or {})}
    problems = []
    if p['mode'] not in ('preflight', 'submit'):
        problems.append('mode must be preflight or submit')
    if p['mode'] == 'submit':
        for key in ('authorized_by', 'authorized_at', 'expires_at'):
            if not p.get(key):
                problems.append('%s is required for submit mode' % key)
        caps = p.get('caps') or {}
        if not all(isinstance(caps.get(k), int) and caps.get(k) > 0 for k in ('per_run', 'per_day', 'per_week')):
            problems.append('caps.per_run, per_day and per_week must be positive whole numbers')
        if not p.get('allowed_ats'):
            problems.append('allowed_ats must list at least one ATS family or host')
    if p.get('allow_credential_entry') or p.get('allow_account_creation'):
        problems.append('credential entry and account creation stay with the human')
    if p.get('unknown_required_question') != 'stop':
        problems.append('unknown required questions must stop the application')
    return problems


def submission_gate(policy, *, now, controls, url, history, run):
    """Decide one role: 'submit', 'needs_confirmation' or 'preflight_only', with reasons.

    controls: {'Pause applications': bool, 'Stop all': bool} read live from Settings.
    history: list of {'at': time, 'ats': family, 'outcome': 'submitted'|'uncertain'|'failed',
             'supervised': bool} for real submit attempts (all runs).
    run: {'submitted': int, 'consecutive_failures': int, 'uncertain': int, 'last_submit_at': time}.
    """
    p = {**DEFAULT_POLICY, **(policy or {})}
    now = now.astimezone(timezone.utc)
    reasons = []
    if controls.get('Stop all') is not False:
        reasons.append('Stop all is on or unreadable')
    if controls.get('Pause applications') is not False:
        reasons.append('Pause applications is on or unreadable')
    if not p['enabled'] or p['mode'] != 'submit':
        reasons.append('submission policy is not enabled in submit mode')
    reasons += policy_problems(p)
    expires = _time(p.get('expires_at'))
    if expires and now >= expires:
        reasons.append('submission authorization expired at %s' % expires.isoformat())

    family = ats_family(url)
    allowed = [str(a).lower() for a in p.get('allowed_ats') or []]
    if family not in allowed:
        reasons.append('ATS %s is not in allowed_ats' % family)

    caps = p.get('caps') or {}
    done = [h for h in history if h.get('outcome') in ('submitted', 'uncertain')]
    day = sum(1 for h in done if _time(h['at']) > now - timedelta(days=1))
    week = sum(1 for h in done if _time(h['at']) > now - timedelta(days=7))
    if run.get('submitted', 0) >= caps.get('per_run', 0):
        reasons.append('per-run cap %s reached' % caps.get('per_run', 0))
    if day >= caps.get('per_day', 0):
        reasons.append('daily cap %s reached' % caps.get('per_day', 0))
    if week >= caps.get('per_week', 0):
        reasons.append('weekly cap %s reached' % caps.get('per_week', 0))

    breaker = p.get('circuit_breaker') or {}
    if run.get('consecutive_failures', 0) >= breaker.get('consecutive_failures', 2):
        reasons.append('circuit breaker: consecutive failures')
    if run.get('uncertain', 0) >= breaker.get('uncertain_submissions', 1):
        reasons.append('circuit breaker: uncertain submission in this run')
    last = _time(run.get('last_submit_at'))
    gap = p.get('min_minutes_between_submissions', 0)
    if last and now < last + timedelta(minutes=gap):
        reasons.append('wait %s minutes between submissions' % gap)

    if reasons:
        return 'preflight_only', reasons
    supervised_done = sum(1 for h in done if h.get('ats') == family and h.get('outcome') == 'submitted')
    if supervised_done < p.get('supervised_first_per_ats', 0):
        return 'needs_confirmation', ['first %s submission(s) on %s need a human go-ahead'
                                      % (p['supervised_first_per_ats'], family)]
    return 'submit', []
