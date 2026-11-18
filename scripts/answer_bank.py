"""Pure answer guards. The harness reads forms, approves semantic mappings and supplies sources.

No network, credentials, generated approvals or form submissions. Field labels map to
semantic topics in the harness; this module does not pretend regex can prove meaning.
"""
import hashlib
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation

HANDLING = ('Exact', 'Adapt', 'From source')
APPROVALS = ('Draft', 'Approved', 'Retired')
QUESTION_STATUSES = ('Needs answer', 'Resolved')
SOURCES = ('career_goals.minimum_base_salary', 'career_goals.ideal_base_salary',
           'career_goals.target_total_compensation')
INVERSE_FIELDS = ('Application answers', 'Application questions')


def normalize_record(record, fields):
    """Normalize connector select/link objects once, preserving IDs rather than labels."""
    result = {'id': record['id']}
    schema = {f['id']: f for f in fields}
    for fid, value in record.get('cellValuesByFieldId', {}).items():
        field = schema[fid]
        if field['type'] == 'multipleRecordLinks':
            value = [v['id'] if isinstance(v, dict) else v for v in value]
        elif field['type'] == 'singleSelect' and isinstance(value, dict):
            value = value['name']
        result[field['name']] = value
    return result


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def _links(row, field):
    values = row.get(field) or []
    if not isinstance(values, list) or len(values) > 1 or any(not isinstance(v, str) or not v for v in values):
        raise ValueError('Expected at most one linked record: ' + field)
    return values


def validate_rules(rows):
    seen, ids = set(), set()
    for row in rows:
        if not row.get('id') or row['id'] in ids:
            raise ValueError('Missing or duplicate answer identity')
        ids.add(row['id'])
        if not isinstance(row.get('Topic'), str) or not row['Topic'].strip():
            raise ValueError('Answer needs a semantic Topic')
        company, application = _links(row, 'Company'), _links(row, 'Application')
        if company and application:
            raise ValueError('Use either company or application scope, not both')
        if row.get('Approval') not in APPROVALS or row.get('Handling') not in HANDLING:
            raise ValueError('Unknown answer approval or handling')
        if row.get('Valid until'):
            date.fromisoformat(row['Valid until'])
        if row['Approval'] != 'Approved':
            continue
        if row['Handling'] == 'From source':
            if row.get('Source field') not in SOURCES or (row.get('Answer') or '').strip():
                raise ValueError('Source answer needs one allowed source and no copied value')
        elif not (row.get('Answer') or '').strip() or row.get('Source field'):
            raise ValueError('Approved answer needs a value and no source selector')
        key = (row['Topic'], tuple(company), tuple(application))
        if key in seen:
            raise ValueError('Conflicting approved answers at the same topic and scope')
        seen.add(key)
    return rows


def field_key(form_url, native_key, question, options, field_type, occurrence=0):
    """A changed question/options produces a new identity; old answers remain historical.

    Use the observed canonical form URL, excluding tracking only when verified.
    native_key must be a stable logical field identity verified across loads, not a
    runtime-generated widget ID. If unavailable use an empty native_key and the
    observed wording/options/type/occurrence, never an invented selector.
    """
    return digest([form_url, native_key, question, options, field_type, occurrence])


def form_value_matches(topic, expected, actual):
    """Accept harmless phone formatting only when every digit remains identical."""
    if topic == 'identity.phone' and isinstance(expected, str) and isinstance(actual, str):
        clean = lambda value: re.sub(r'[ +().-]', '', value)
        return bool(clean(expected)) and clean(expected) == clean(actual)
    return expected == actual


def question_action(existing, application_id, key):
    found = [r for r in existing if r.get('Application') == [application_id]
             and r.get('Field key') == key]
    if len(found) > 1:
        raise ValueError('Duplicate application question identities; reconcile before writing')
    return {'action': 'reuse', 'id': found[0]['id']} if found else {'action': 'create'}


def resolve(rows, topic, *, company_id, application_id, today, mapping_verified=False,
            scope_verified=False, sources=None, expected_currency=None, expected_kind=None,
            proposed_answer=None, adaptation_supported=False, options=None, multiple=False,
            numeric=False, policy_read=False, contrary_evidence=False):
    """Return Resolved only after explicit harness checks; never infer user approval.

    Caller checks question meaning, negation, named subjects, policy definitions and
    Guidance. Matching a topic alone does not establish applicability.
    """
    validate_rules(rows)
    def pending(reason):
        return {'status': 'Needs answer', 'reason': reason}
    if not mapping_verified or not scope_verified:
        return pending('Question meaning or answer boundaries have not been verified')
    if contrary_evidence:
        return pending('Verified current facts contradict the proposed answer')
    current = date.fromisoformat(today)
    candidates = []
    for row in rows:
        if row['Topic'] != topic or row['Approval'] != 'Approved':
            continue
        if row.get('Application'):
            if row['Application'] != [application_id]:
                continue
            rank = 2
        elif row.get('Company'):
            if row['Company'] != [company_id]:
                continue
            rank = 1
        else:
            rank = 0
        # An expired specific answer must not silently fall back to a general answer.
        candidates.append((rank, row))
    if not candidates:
        return pending('No approved applicable answer')
    rule = max(candidates, key=lambda x: x[0])[1]
    if rule.get('Valid until') and date.fromisoformat(rule['Valid until']) < current:
        return pending('The applicable answer has expired')
    if topic.startswith('consent.') and not policy_read:
        return pending('Read the actual notice, policy or agreement before acknowledging it')
    source_revision = None
    if rule['Handling'] == 'From source':
        source = (sources or {}).get(rule['Source field']) or {}
        if source.get('verified') is not True or not source.get('revision'):
            return pending('Current source value and revision are not verified')
        if not expected_currency or source.get('currency') != expected_currency:
            return pending('Compensation currency is missing or differs from the field')
        if source.get('period') != 'annual' or not expected_kind or source.get('kind') != expected_kind:
            return pending('Annual base versus total compensation has not been established')
        answer, source_revision = source.get('value'), source['revision']
    elif rule['Handling'] == 'Adapt':
        if proposed_answer is None or adaptation_supported is not True:
            return pending('Adaptation is missing or adds unsupported meaning')
        answer = proposed_answer
    else:
        answer = rule['Answer']
    if numeric:
        try:
            number = Decimal(str(answer))
            if isinstance(answer, bool) or not number.is_finite() or number < 0:
                raise ValueError()
            answer = format(number, 'f')
        except (InvalidOperation, ValueError, TypeError):
            return pending('Answer is not a supported nonnegative number')
    if options is not None:
        if multiple:
            if not isinstance(answer, list) or not answer or len(set(answer)) != len(answer) or any(a not in options for a in answer):
                return pending('Answer is not a supported selection from the actual options')
        elif not isinstance(answer, str) or answer not in options:
            return pending('Answer is not one of the actual options')
    if answer is None or answer == '' or isinstance(answer, (dict, bool)):
        return pending('Answer has no supported final value')
    return {'status': 'Resolved', 'answer': answer, 'answer_id': rule['id'],
            'answer_sha256': digest(rule), 'source_revision': source_revision}


def validate_question(row, *, user_approved=False, resolution=None):
    if len(row.get('Application') or []) != 1 or not row.get('Field key') or not row.get('Question'):
        raise ValueError('Question needs one application, a field key and exact wording')
    _links(row, 'Answer rule')
    if row.get('Status') not in QUESTION_STATUSES:
        raise ValueError('Unknown question status')
    if row['Status'] == 'Resolved':
        valid_resolution = (resolution or {}).get('status') == 'Resolved'
        if not row.get('Final answer') or not (user_approved or valid_resolution):
            raise ValueError('Resolved requires explicit user approval or a verified resolution')
        if valid_resolution:
            value = resolution['answer']
            expected = json.dumps(value, ensure_ascii=False) if isinstance(value, list) else str(value)
            if row['Final answer'] != expected or row.get('Answer rule') != [resolution['answer_id']]:
                raise ValueError('Final answer or rule differs from the validated resolution')
    return row
