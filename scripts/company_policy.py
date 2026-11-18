"""Company targeting and funding admission. Pure functions; no account access."""
SEARCH_STATUSES = ['Proposed', 'Allow', 'Exclude']
# Ordered: a minimum stage admits every later stage. Unknown never qualifies.
FUNDING_STAGES = ['Pre-seed / Seed', 'Series A', 'Series B', 'Series C', 'Series D',
                  'Series E+', 'Late private', 'Public', 'Unknown']
_STAGE_RANK = {s: i for i, s in enumerate(FUNDING_STAGES[:-1])}


def funding_qualifies(stage, minimum):
    """True only for a known stage at or after the configured minimum."""
    if minimum not in FUNDING_STAGES:
        raise ValueError('Set company_policy.discovery.min_funding_stage in private Settings or Career Goals')
    if stage not in _STAGE_RANK or minimum not in _STAGE_RANK:
        return False
    return _STAGE_RANK[stage] >= _STAGE_RANK[minimum]


def scan_enabled(company):
    """Use human-Allow targeting; respect permanent blocks retained in legacy bases."""
    return (company.get('Search status') == 'Allow'
            and company.get('Application hold status') != 'Blocked (permanent)')


def company_for_application(application, companies):
    """Resolve one current named company; cached Allow IDs do not prove targeting."""
    linked = application.get('Company') or []
    if len(linked) != 1 or companies is None:
        return None
    matches = [company for company in companies if company.get('id') == linked[0]]
    return matches[0] if len(matches) == 1 and scan_enabled(matches[0]) else None
