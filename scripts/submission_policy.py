"""Basic submission guard rails for Apply.

Settings.submission_policy holds one number, max_per_day; the live Pause applications
control is the on/off switch. The user sets both; agents never edit them. Company holds,
apply_ready and the fixed safety rules in stages/apply.md still apply.
"""
from datetime import datetime, timedelta, timezone

DEFAULT_POLICY = {'max_per_day': 0}


def _time(value):
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    return datetime.fromisoformat(str(value).replace('Z', '+00:00')).astimezone(timezone.utc)


def policy_problems(policy):
    cap = (policy or {}).get('max_per_day')
    return [] if isinstance(cap, int) and not isinstance(cap, bool) and cap >= 0 else ['max_per_day must be a whole number']


def submission_gate(policy, *, now, controls, history, run):
    """Return ('submit' | 'preflight_only', reasons) for the next real Submit.

    controls: live {'Pause applications': bool, 'Stop all': bool}.
    history: real submit attempts [{'at': time, 'outcome': 'submitted'|'uncertain'|'failed'}].
    run: {'uncertain': int} for this Run.
    """
    reasons = policy_problems(policy)
    if controls.get('Stop all') is not False:
        reasons.append('Stop all is on or unreadable')
    if controls.get('Pause applications') is not False:
        reasons.append('Pause applications is on or unreadable')
    if run.get('uncertain', 0):
        reasons.append('an earlier submission in this Run is unclear')
    now = now.astimezone(timezone.utc)
    today = sum(1 for h in history if h.get('outcome') in ('submitted', 'uncertain') and _time(h['at']) > now - timedelta(days=1))
    cap = (policy or {}).get('max_per_day', 0)
    if not reasons and today >= cap:
        reasons.append('daily limit %s reached' % cap)
    return ('preflight_only', reasons) if reasons else ('submit', [])
