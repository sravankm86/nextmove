"""Separate basic candidate inventory from final Review acceptance.

Title screening needs contextual evidence before candidate inventory.
No model APIs, network calls, credentials or user data are required.
"""
import re
import unicodedata
import math


def normalize(value):
    text = unicodedata.normalize('NFKC', value or '').lower()
    return re.sub(r'\s+', ' ', text.replace('–', '-').replace('—', '-')).strip()


DIRECT_PM = re.compile(r'\bproduct\s+(?:(?:inbound|outbound|technical|platform|portfolio|growth|group|security|senior|staff|principal|lead|ai|data|digital|tax)\s+){0,3}(?:manager|mgr|management)\b')
FLAT_PM = re.compile(r'\bmember\s+of\s+product\s+(?:staff|team)\b')
OWNER_LEAD = re.compile(r'\bproduct\s+(?:owner|lead|leadership)\b')
LEADERSHIP = re.compile(r'\b(?:director|head|vp|svp|evp|vice president|chief)\b.{0,45}\bproduct\b|\bproduct\b.{0,45}\b(?:director|head|vp|svp|evp|vice president)\b')
ABBREVIATION = re.compile(r'\b(?:gpm|cpo|pm|gm)\b|\bgeneral manager\b')
LOCALIZED_PM = re.compile(r'produktmanager|produktmanagement|chef(?:fe)?\s+de\s+produit|responsable(?:\s+de)?\s+produit|director(?:a)?\s+de\s+producto|gerente\s+de\s+produt[oa]|gestor\s+de\s+produto|产品经理|產品經理|プロダクトマネージャー|제품\s*관리자')
CLEAR_OTHER = re.compile(r'\b(?:marketing|designer|design|security engineer|product security|support|success|sales|business development|communications|public relations|data scientist|data science|analytics|analyst|software engineer|engineering|engineer|legal|counsel|operations|supply chain|finance|policy|enablement|assistant|program manager|project manager)\b')
JUNIOR = re.compile(r'^(?:intern|internship|junior|entry.level|graduate)\b|\bassociate\s+(?:technical\s+)?product\s+(?:manager|mgr)\b|\bproduct\s+(?:manager|mgr|management)\s+(?:intern|internship|i|1)\b')


def title_screen(title):
    text = normalize(title)
    if not text or text in {'.', '-', 'n/a', 'unknown'}:
        return {'decision': 'pending_metadata', 'reason': 'No usable title; verify official posting'}
    # A shift time ending in PM is not a product-role abbreviation.
    text = re.sub(r'\b\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm)\b', '', text)
    role_abbrev = re.search(r'^(?:(?:senior|sr\.?|staff|principal|lead|group|technical|platform)\s+)*(?:pm|gpm)\b', text)
    direct = bool(DIRECT_PM.search(text) or FLAT_PM.search(text) or OWNER_LEAD.search(text) or LOCALIZED_PM.search(text) or role_abbrev)
    possible = direct or bool(LEADERSHIP.search(text) or ABBREVIATION.search(text))
    if not possible:
        return {'decision': 'reject', 'reason': 'No PM role-family signal'}
    if not direct and CLEAR_OTHER.search(text):
        return {'decision': 'reject', 'reason': 'Explicit other function without a PM role signal'}
    if JUNIOR.search(text):
        return {'decision': 'reject', 'reason': 'Explicit junior/entry PM title'}
    return {'decision': 'verify_jd', 'reason': 'Perform basic contextual PM check; final scope/eligibility belongs to Review'}


def inventory_candidate(assessment):
    """Broad screen; no career inputs or exhaustive scope decision.

    A reader supplies basic semantic evidence or an explicit ambiguity reason.
    Identity gaps remain Run checks. Posting availability is not a scan gate. Full JD/scope uncertainty can
    remain on the candidate row for Review. A keyword hit alone is insufficient.
    """
    if assessment.get('identity_verified') is not True:
        return 'pending'
    screen = title_screen(assessment.get('title'))
    role_hint = assessment.get('role_hint')
    evidence = assessment.get('basic_evidence')
    if role_hint == 'other' and evidence:
        return 'reject'
    if assessment.get('clearly_junior') is True and evidence:
        return 'reject'
    # Verified context can rescue missing/nonstandard titles, not fabricated IDs.
    if screen['decision'] == 'reject' and not (role_hint == 'plausible_pm' and evidence):
        return 'reject'
    if role_hint not in {'plausible_pm', 'ambiguous_pm'} or not evidence:
        return 'pending'
    if screen['decision'] == 'pending_metadata' and role_hint != 'plausible_pm':
        return 'pending'
    return 'pass'


def review_eligibility(assessment, *, years_threshold):
    """Return pass/reject/pending. Never infer company-grade equivalence.

    years_threshold is exclusive. Low posted minimums alone do not prove scope
    below the bar. Equivalent scope requires an explicit evidence-backed decision.
    """
    if not isinstance(years_threshold, (int, float)) or isinstance(years_threshold, bool):
        raise ValueError('Explicit numeric experience threshold required')
    if assessment.get('identity_verified') is not True or assessment.get('description_verified') is not True:
        return 'pending'
    if assessment.get('role_family', 'unknown') not in {'product_management', 'unknown', None}:
        return 'reject'
    if assessment.get('role_family') != 'product_management' or not assessment.get('role_evidence'):
        return 'pending'
    years = assessment.get('experience_years_target')
    experience_pass = isinstance(years, (int, float)) and not isinstance(years, bool) and years > years_threshold and bool(assessment.get('experience_evidence'))
    scope_pass = assessment.get('equivalent_senior_scope') is True and bool(assessment.get('scope_evidence'))
    pay_scope_pass = (assessment.get('pay_supported_scope') is True
                      and assessment.get('meaningful_pm_ownership') is True
                      and bool(assessment.get('role_specific_pay_evidence'))
                      and bool(assessment.get('scope_evidence'))
                      and assessment.get('explicitly_below_scope') is not True)
    if experience_pass or scope_pass or pay_scope_pass:
        return 'pass'
    if assessment.get('explicitly_below_scope') is True and assessment.get('scope_evidence'):
        return 'reject'
    return 'pending'


def general_pm_gate(assessment):
    """Explicit user preference; reader verifies general scope, never the title alone.

    This accepts a disclosed generic-qualification exception, not fabricated skills.
    Specialist requirements and incomplete descriptions cannot use this route.
    """
    if assessment.get('preference_enabled') is not True:
        return 'not_applicable'
    if assessment.get('description_complete') is not True:
        return 'pending'
    if (assessment.get('general_role_verified') is not True
            or assessment.get('no_required_specialist_expertise') is not True):
        return 'not_applicable'
    for key in ['seniority_pass', 'remaining_hard_restrictions_pass',
                'critical_minimums_pass', 'overall_alignment_pass']:
        if assessment.get(key) is False:
            return 'reject'
        if assessment.get(key) is not True:
            return 'pending'
    if assessment.get('base_salary_pass') is False:
        return 'reject'
    if assessment.get('base_salary_pass') is True:
        return 'approve'
    return 'approve_provisional' if assessment.get('allow_salary_provisional') is True else 'pending'


def qualification_gate(minimum, preferred, *, preferred_listed=True):
    """Evaluate evidence-based qualification findings; unknown is not failure.

    The reader identifies distinct requirements, preserves AND/OR alternatives,
    and supplies candidate/JD evidence. This function does not infer skills.
    """
    def statuses(items):
        result = []
        for item in items:
            status = item.get('status')
            if status not in {'met', 'not_met', 'unknown'}:
                raise ValueError('Qualification status must be met/not_met/unknown')
            if status != 'unknown' and not item.get('evidence'):
                raise ValueError('A qualification finding needs evidence')
            result.append(status)
        return result
    required, desirable = statuses(minimum), statuses(preferred)
    if 'not_met' in required:
        return 'reject'
    if 'unknown' in required:
        return 'pending'
    if not preferred_listed:
        return 'pass'
    if not desirable:
        return 'pending'
    matched, unknown = desirable.count('met'), desirable.count('unknown')
    if matched * 2 > len(desirable):
        return 'pass'
    if (matched + unknown) * 2 <= len(desirable):
        return 'reject'
    return 'pending'


def admission(assessment, *, years_threshold):
    """Legacy callable alias for final Review eligibility, not inventory."""
    return review_eligibility(assessment, years_threshold=years_threshold)


def queue_allowed(*, role_decision, career_decision, career_evidence, versions_current,
                  review_decision=None, qualifications_decision=None,
                  resume_exclusions_pass=None, essential_fit_pass=None):
    return (role_decision == 'pass' and career_decision == 'pass'
            and bool(career_evidence) and versions_current is True
            and review_decision == 'approve' and qualifications_decision == 'pass'
            and resume_exclusions_pass is True and essential_fit_pass is True)


def base_maximum_gate(assessment, *, threshold, currency, period):
    """Compare a reader-verified applicable base maximum, never estimated TC.

    This gate belongs to Review. Threshold and comparison units come from
    private preferences; the reader supplies a normalized official band.
    """
    if (not isinstance(threshold, (int, float)) or isinstance(threshold, bool)
            or not math.isfinite(threshold) or threshold < 0
            or not currency or not period):
        raise ValueError('A finite threshold and explicit comparison units are required')
    if (assessment.get('base_upper_bound_verified') is not True
            or assessment.get('applicable_scope_verified') is not True
            or assessment.get('component') != 'base'
            or not assessment.get('source_evidence')
            or assessment.get('currency') != currency
            or assessment.get('period') != period):
        return 'pending'
    maximum = assessment.get('maximum')
    if (not isinstance(maximum, (int, float)) or isinstance(maximum, bool)
            or not math.isfinite(maximum) or maximum < 0):
        return 'pending'
    return 'pass' if maximum > threshold else 'reject'


# Current Review reads the human-facing tables directly; no copied score config.
def review_frame_contract(review_path=None):
    import hashlib
    from pathlib import Path
    path = Path(review_path) if review_path else Path(__file__).resolve().parents[1] / 'stages/review.md'
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    try:
        career_text = text.split('## Step 2.', 1)[1].split('## Step 3.', 1)[0]
        resume_text = text.split('## Step 3.', 1)[1]
    except IndexError as exc:
        raise ValueError('Review requires its career and resume sections') from exc
    mappings = []
    for section in [career_text, resume_text]:
        pairs = re.findall(r'^\|\s*(Low|Medium|High)\s*\|[^\n|]+\|\s*(\d+)\s*\|\s*$', section, re.M)
        mapping = {label: int(score) for label, score in pairs}
        if len(pairs) != 3 or set(mapping) != {'Low', 'Medium', 'High'} or not mapping['Low'] < mapping['Medium'] < mapping['High']:
            raise ValueError('Review needs three distinct ascending scores per rating table')
        mappings.append(mapping)
    conditions = ['Career fit is Unresolved', 'Every possible total is Not pursuing', 'Any score is Unresolved']
    expected_statuses = ['Need review', 'Not pursuing', 'Need review']
    decisions, special, totals = [], [], {}
    for line in text.splitlines():
        cells = [x.strip() for x in line.strip().strip('|').split('|')]
        if len(cells) != 2 or cells[1] not in {'Queued', 'Need review', 'Not pursuing'}:
            continue
        check, outcome = cells
        match = re.fullmatch(r'Total (\d+)(?:[–-](\d+))?', check)
        if match:
            lo, hi = int(match[1]), int(match[2] or match[1])
            if lo > hi or any(t in totals for t in range(lo, hi + 1)):
                raise ValueError('Review decision totals overlap or have a reversed range')
            for value in range(lo, hi + 1):
                totals[value] = outcome
            decisions.append({'check': check, 'outcome': outcome})
        elif check in conditions:
            special.append((check, outcome))
            decisions.append({'check': check, 'outcome': outcome})
        else:
            raise ValueError('Unsupported Review decision condition: ' + check)
    if special != list(zip(conditions, expected_statuses)) or [x['check'] for x in decisions[:3]] != conditions:
        raise ValueError('Review must preserve the explicit career/early-stop/missing-score decision order')
    possible = {a + b for a in mappings[0].values() for b in mappings[1].values()}
    if not possible.issubset(totals) or set(totals.values()) != {'Queued', 'Need review', 'Not pursuing'}:
        raise ValueError('Review decision table must cover every possible total and outcome')
    return 'review-sha256:' + hashlib.sha256(raw).hexdigest(), {
        'assessment_method': 'three_step_v1', 'career': mappings[0], 'resume': mappings[1],
        'decisions': decisions, 'total_outcomes': totals}


def _findings(items):
    values = []
    for item in items:
        value = item.get('status')
        if value not in {'met', 'not_met', 'unknown'}:
            raise ValueError('Expected met, not_met or unknown')
        if value != 'unknown' and not item.get('evidence'):
            raise ValueError('A known finding requires source evidence')
        values.append(value)
    return values


def career_rating(criteria):
    values = _findings(criteria)
    if any(v == 'not_met' and c.get('objective') is True for c, v in zip(criteria, values)):
        return 'Low'
    if not values or 'unknown' in values:
        return 'Unresolved'
    return 'High' if all(v == 'met' for v in values) else 'Medium'


def resume_rating(minimum, preferred, *, minimum_listed=True, preferred_listed=True):
    required, desired = _findings(minimum), _findings(preferred)
    if 'not_met' in required:
        return 'Low'
    if 'unknown' in required or minimum_listed and not required:
        return 'Unresolved'
    if not preferred_listed:
        return 'High'
    if 'not_met' in desired:
        return 'Medium'
    if not desired or 'unknown' in desired:
        return 'Unresolved'
    return 'High'


def scored_review(career, resume, *, objective_failure=False, minimum_failure=False, contract=None):
    # Legacy flags remain accepted for callers, but cannot override the sole source.
    if contract is None:
        _, contract = review_frame_contract()
    ratings = {'Low', 'Medium', 'High', 'Unresolved'}
    if career not in ratings or resume not in ratings:
        raise ValueError('Unknown fit rating')
    for axis in ['career', 'resume']:
        mapping = contract[axis]
        if set(mapping) != ratings - {'Unresolved'} or any(type(v) is not int for v in mapping.values()):
            raise ValueError('Each axis requires the published numeric rating table')
    c, r = contract['career'].get(career), contract['resume'].get(resume)
    total = c + r if c is not None and r is not None else None
    outcomes = contract['total_outcomes']
    possible = {a + b for a in ([c] if c is not None else contract['career'].values())
                for b in ([r] if r is not None else contract['resume'].values())}
    if career == 'Unresolved':
        outcome = 'Need review'
    elif all(outcomes[value] == 'Not pursuing' for value in possible):
        outcome = 'Not pursuing'
    elif total is None:
        outcome = 'Need review'
    else:
        outcome = outcomes[total]
    return {'career_rating': career, 'career_score': c, 'resume_rating': resume,
            'resume_score': r, 'total': total, 'outcome': outcome}
