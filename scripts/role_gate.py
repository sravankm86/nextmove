"""Separate basic candidate inventory from final Review acceptance.

Title screening needs contextual evidence before candidate inventory.
No model APIs, network calls, credentials or user data are required.
"""
import re
import unicodedata


def normalize(value):
    text = unicodedata.normalize('NFKC', value or '').lower()
    return re.sub(r'\s+', ' ', text.replace('–', '-').replace('—', '-')).strip()


FAMILY_KEYS = ('name', 'direct_patterns', 'possible_patterns', 'other_function_patterns', 'junior_patterns', 'ignore_patterns')


def role_family(config):
    """Compile the user's private role-family definition (Settings `role_family`).

    The repository ships no role family: each user defines the work they target
    (for example templates/role-family.example.json). A missing or malformed
    definition stops screening instead of falling back to someone else's defaults.
    """
    if isinstance(config, dict) and config.get('_compiled'):
        return config
    if not isinstance(config, dict) or not config.get('name') or not config.get('direct_patterns'):
        raise ValueError('Settings role_family needs a name and at least one direct pattern')
    unknown = set(config) - set(FAMILY_KEYS) - {'note', 'examples'}
    if unknown:
        raise ValueError('Unknown role_family keys: ' + ', '.join(sorted(unknown)))
    compiled = {'_compiled': True, 'name': config['name']}
    for key in FAMILY_KEYS[1:]:
        patterns = config.get(key) or []
        if not isinstance(patterns, list) or not all(isinstance(p, str) and p for p in patterns):
            raise ValueError('role_family.%s must be a list of regular expressions' % key)
        compiled[key] = [re.compile(p) for p in patterns]
    return compiled


def _any(patterns, text):
    return any(p.search(text) for p in patterns)


def title_screen(title, family):
    family = role_family(family)
    name = family['name']
    text = normalize(title)
    if not text or text in {'.', '-', 'n/a', 'unknown'}:
        return {'decision': 'pending_metadata', 'reason': 'No usable title; verify official posting'}
    for pattern in family['ignore_patterns']:
        text = pattern.sub('', text)
    direct = _any(family['direct_patterns'], text)
    possible = direct or _any(family['possible_patterns'], text)
    if not possible:
        return {'decision': 'reject', 'reason': 'No %s role-family signal' % name}
    if not direct and _any(family['other_function_patterns'], text):
        return {'decision': 'reject', 'reason': 'Explicit other function without a %s signal' % name}
    if _any(family['junior_patterns'], text):
        return {'decision': 'reject', 'reason': 'Explicit junior/entry %s title' % name}
    return {'decision': 'verify_jd', 'reason': 'Perform basic contextual %s check; final scope/eligibility belongs to Review' % name}


def inventory_candidate(assessment, family):
    """Broad screen; no career inputs or exhaustive scope decision.

    A reader supplies basic semantic evidence or an explicit ambiguity reason.
    Identity gaps remain Run checks. Posting availability is not a scan gate. Full JD/scope uncertainty can
    remain on the candidate row for Review. A keyword hit alone is insufficient.
    """
    if assessment.get('identity_verified') is not True:
        return 'pending'
    screen = title_screen(assessment.get('title'), family)
    role_hint = assessment.get('role_hint')
    evidence = assessment.get('basic_evidence')
    if role_hint == 'other' and evidence:
        return 'reject'
    if assessment.get('clearly_junior') is True and evidence:
        return 'reject'
    # Verified context can rescue missing/nonstandard titles, not fabricated IDs.
    if screen['decision'] == 'reject' and not (role_hint == 'plausible' and evidence):
        return 'reject'
    if role_hint not in {'plausible', 'ambiguous'} or not evidence:
        return 'pending'
    if screen['decision'] == 'pending_metadata' and role_hint != 'plausible':
        return 'pending'
    return 'pass'


def review_eligibility(assessment, *, years_threshold, role_family_name):
    """Return pass/reject/pending. Never infer company-grade equivalence.

    years_threshold is exclusive. Low posted minimums alone do not prove scope
    below the bar. Equivalent scope requires an explicit evidence-backed decision.
    """
    if not isinstance(years_threshold, (int, float)) or isinstance(years_threshold, bool):
        raise ValueError('Explicit numeric experience threshold required')
    if assessment.get('identity_verified') is not True or assessment.get('description_verified') is not True:
        return 'pending'
    if not role_family_name:
        raise ValueError('Explicit role family name required (Settings role_family.name)')
    if assessment.get('role_family', 'unknown') not in {role_family_name, 'unknown', None}:
        return 'reject'
    if assessment.get('role_family') != role_family_name or not assessment.get('role_evidence'):
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
