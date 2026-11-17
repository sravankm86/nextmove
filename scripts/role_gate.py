"""Separate basic candidate inventory from final Review acceptance.

Title screening needs contextual evidence before candidate inventory.
No model APIs, network calls, credentials or user data are required.
"""
import re
import unicodedata


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
    ratings = ['Unresolved', 'Low', 'Medium', 'High']
    for section in [career_text, resume_text]:
        pairs = re.findall(r'^\|\s*(Unresolved|Low|Medium|High)\s*\|[^\n|]+\|\s*(\d+)\s*\|\s*$', section, re.M)
        mapping = {label: int(score) for label, score in pairs}
        if len(pairs) != 4 or set(mapping) != set(ratings) or not all(mapping[a] < mapping[b] for a, b in zip(ratings, ratings[1:])):
            raise ValueError('Review needs four distinct ascending scores per rating table')
        mappings.append(mapping)
    decisions, totals, specials = [], {}, {}
    low_outcome = None
    for line in text.splitlines():
        cells = [x.strip() for x in line.strip().strip('|').split('|')]
        if len(cells) != 2 or cells[1] not in {'Queued', 'Need review', 'Not pursuing'}:
            continue
        check, outcome = cells
        if check == 'Either fit is Low':
            if low_outcome is not None:
                raise ValueError('Duplicate Low-fit routing rule')
            low_outcome = outcome
            continue
        match = re.fullmatch(r'Total (\d+)(?:[–-](\d+))?(?: (with|without) Unresolved)?', check)
        if not match:
            raise ValueError('Unsupported Review decision condition: ' + check)
        lo, hi, qualifier = int(match[1]), int(match[2] or match[1]), match[3]
        if lo > hi or qualifier and lo != hi:
            raise ValueError('Invalid Review total range')
        for value in range(lo, hi + 1):
            key = (value, qualifier)
            if key in specials or not qualifier and value in totals:
                raise ValueError('Duplicate Review total condition')
            if qualifier:
                specials[key] = outcome
            else:
                totals[value] = outcome
        decisions.append({'check': check, 'outcome': outcome, 'minimum': lo, 'maximum': hi, 'unresolved': qualifier})
    if low_outcome != 'Not pursuing':
        raise ValueError('Review must publish Low on either axis as Not pursuing')
    for career, c in mappings[0].items():
        for resume, r in mappings[1].items():
            qualifier = 'with' if 'Unresolved' in [career, resume] else 'without'
            matched = [d for d in decisions if d['minimum'] <= c + r <= d['maximum'] and (d['unresolved'] is None or d['unresolved'] == qualifier)]
            if len(matched) != 1:
                raise ValueError('Review routing must cover each rating pair exactly once')
    if {d['outcome'] for d in decisions} != {'Queued', 'Need review', 'Not pursuing'}:
        raise ValueError('Review requires all three outcomes')
    return 'review-sha256:' + hashlib.sha256(raw).hexdigest(), {
        'assessment_method': 'three_step_v1', 'career': mappings[0], 'resume': mappings[1],
        'decisions': decisions, 'total_outcomes': totals, 'low_outcome': low_outcome}


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


def resume_rating(minimum, preferred, *, critical=None, minimum_listed=True, preferred_listed=True):
    # Critical asks are identified by the assessor from the whole JD, not keywords.
    required, desired = _findings(minimum), _findings(preferred)
    central = _findings(critical or [])
    if 'not_met' in required or 'not_met' in central:
        return 'Low'
    if 'unknown' in required or 'unknown' in central or minimum_listed and not required:
        return 'Unresolved'
    if not preferred_listed:
        return 'High'
    if 'not_met' in desired or 'unknown' in desired:
        return 'Medium'
    if not desired:
        return 'Unresolved'
    return 'High'


def scored_review(career, resume, *, contract=None):
    if contract is None:
        _, contract = review_frame_contract()
    ratings = {'Low', 'Medium', 'High', 'Unresolved'}
    if career not in ratings or resume not in ratings:
        raise ValueError('Unknown fit rating')
    for axis in ['career', 'resume']:
        mapping = contract[axis]
        if set(mapping) != ratings or any(type(v) is not int for v in mapping.values()):
            raise ValueError('Each axis requires the published numeric rating table')
    c, r = contract['career'][career], contract['resume'][resume]
    total = c + r
    qualifier = 'with' if 'Unresolved' in [career, resume] else 'without'
    matched = [d for d in contract['decisions'] if d['minimum'] <= total <= d['maximum'] and (d['unresolved'] is None or d['unresolved'] == qualifier)]
    if len(matched) != 1:
        raise ValueError('Review routing must match exactly once')
    return {'career_rating': career, 'career_score': c, 'resume_rating': resume,
            'resume_score': r, 'total': total,
            'outcome': contract['low_outcome'] if 'Low' in [career, resume] else matched[0]['outcome']}
