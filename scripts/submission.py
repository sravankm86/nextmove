"""Pure guards for the explicit-only Submit stage (stages/submit.md).

The harness drives the browser; these readers decide whether a role may be submitted,
what exactly will be sent and whether the saved proof justifies Applied. They never
browse, sign in, fill, upload or click anything themselves.
"""
import hashlib
import json
from urllib.parse import urlsplit

ATTEMPT_SCHEMA = 'nextmove.submit-attempt.v1'
POLICY_DEFAULTS = {'enabled': False, 'max_per_run': 10, 'max_per_company_per_day': 1}

# Every attempted role that fails ends at Apply manually with one of these kinds and the
# exact detail. Roles never attempted (disabled policy, Stop all, caps, no current answer
# check yet) stay Ready and are only reported.
SUBMIT_BLOCKERS = (
    'not_ready', 'inputs_changed', 'posting_closed',
    'duplicate_application', 'prior_attempt_uncertain',
    'sign_in_required', 'account_creation', 'mfa_required', 'bot_check',
    'unexpected_domain', 'form_changed', 'unapproved_field', 'prefill_conflict',
    'upload_failed', 'assessment_required', 'payment_or_identity_request',
    'technical_error', 'no_confirmation', 'portal_error',
)


def policy(settings_value):
    """Settings.submission_policy, failing closed to disabled with conservative caps."""
    value = settings_value if isinstance(settings_value, dict) else {}
    result = dict(POLICY_DEFAULTS)
    if value.get('enabled') is True:
        result['enabled'] = True
    for key in ('max_per_run', 'max_per_company_per_day'):
        if type(value.get(key)) is int and value[key] >= 0:
            result[key] = value[key]
    return result


def same_site(url, reference):
    """Host must equal the inspected form's host or be a subdomain of the same parent."""
    a = (urlsplit(url or '').hostname or '').lower().rstrip('.')
    b = (urlsplit(reference or '').hostname or '').lower().rstrip('.')
    if not a or not b or urlsplit(url).scheme != 'https':
        return False
    parent = '.'.join(b.split('.')[-2:])
    return a == b or a.endswith('.' + parent) or a == parent


def manifest(application, inspection, resume_sha256, attachments=()):
    """Exact values to send: approved mapped answers, the verified resume and approved files.

    Required and sensitive questions must already carry verified approved mappings
    (application_answers_ready). Optional non-sensitive questions are sent only when mapped.
    """
    fields = []
    for q in inspection.get('questions') or []:
        ref = q.get('answer') or {}
        if ref.get('mapping_verified') is True and isinstance(ref.get('mapped_answer'), str) and ref['mapped_answer'].strip():
            fields.append({'field_key': q['field_key'], 'value': ref['mapped_answer']})
        elif q.get('required') or q.get('sensitive'):
            raise ValueError('Required or sensitive question has no approved mapping: ' + str(q.get('field_key')))
    files = [{'kind': 'resume', 'sha256': resume_sha256}]
    for item in attachments:
        if not (isinstance(item, dict) and item.get('approved') is True and item.get('sha256') and item.get('field_key')):
            raise ValueError('Attachment must be an approved, hashed file for a known field')
        files.append({'kind': item.get('kind', 'attachment'), 'field_key': item['field_key'], 'sha256': item['sha256']})
    if not resume_sha256:
        raise ValueError('Verified resume hash required')
    body = {'application_id': application.get('id'), 'job_key': application.get('Job key'),
            'form_url': inspection.get('form_url'), 'form_hash': inspection.get('form_hash'),
            'fields': sorted(fields, key=lambda f: f['field_key']), 'files': files}
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    return {**body, 'sha256': digest}


def attempts(state):
    value = ((state or {}).get('submit') or {}).get('attempts')
    return value if isinstance(value, list) else []


def prior_attempt_uncertain(state):
    """Any earlier attempt where Submit may have been clicked blocks automatic resubmission."""
    return any(not isinstance(a, dict) or a.get('submit_clicked') is not False for a in attempts(state))


def submission_eligible(app, state, *, ready, human_request=None):
    """Only Ready roles whose live Prepare checks still pass (`ready`, from preparation_outcome)
    and with no attempt that might already have reached the employer."""
    from stage_state import protected_history
    if app.get('Lifecycle status') != 'Ready' or protected_history(app, state) or ready is not True:
        return False
    if prior_attempt_uncertain(state):
        # Only the user's explicit, recorded instruction can authorize another try.
        return bool(isinstance(human_request, dict) and isinstance(human_request.get('quote'), str)
                    and human_request['quote'].strip() and human_request.get('observed_at'))
    return True


def proof_verified(attempt):
    proof = attempt.get('proof') if isinstance(attempt, dict) else None
    if not isinstance(proof, dict):
        return False
    return bool(attempt.get('schema') == ATTEMPT_SCHEMA and attempt.get('submit_clicked') is True
                and attempt.get('manifest_sha256') and attempt.get('started_at')
                and attempt.get('form_url') and same_site(proof.get('page_url'), attempt['form_url'])
                and isinstance(proof.get('confirmation_text'), str) and proof['confirmation_text'].strip()
                and proof.get('file_id') and proof.get('sha256') and proof.get('observed_at')
                and proof.get('verified') is True)


def submission_result(attempt):
    """Applied only with verified proof; everything else is Apply manually with a reason.

    possibly_submitted is true whenever Submit was or may have been clicked; the
    Agent notes must then warn the user to check before applying again.
    """
    if proof_verified(attempt):
        return {'status': 'Applied'}
    attempt = attempt if isinstance(attempt, dict) else {}
    blocker = attempt.get('blocker') if isinstance(attempt.get('blocker'), dict) else {}
    kind = blocker.get('kind') if blocker.get('kind') in SUBMIT_BLOCKERS else 'no_confirmation'
    clicked = attempt.get('submit_clicked')
    return {'status': 'Apply manually', 'kind': kind, 'detail': blocker.get('detail') or '',
            'possibly_submitted': clicked is not False}
