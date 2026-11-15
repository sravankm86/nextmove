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
    if experience_pass or scope_pass:
        return 'pass'
    if assessment.get('explicitly_below_scope') is True and assessment.get('scope_evidence'):
        return 'reject'
    return 'pending'


def admission(assessment, *, years_threshold):
    """Legacy callable alias for final Review eligibility, not inventory."""
    return review_eligibility(assessment, years_threshold=years_threshold)


def queue_allowed(*, role_decision, career_decision, career_evidence, versions_current,
                  review_decision=None):
    return (role_decision == 'pass' and career_decision == 'pass'
            and bool(career_evidence) and versions_current is True
            and review_decision == 'approve')


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
