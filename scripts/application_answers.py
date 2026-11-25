"""Pure checks for a complete form inspection and current approved/resolved answers.

The harness discovers questions and maps meaning/options; this reader never browses,
drafts, approves, resolves, fills, uploads or submits anything. Sensitive questions
(demographics/EEO, disability, veteran status, criminal history, legal attestations and
consents) need approved answers even when optional, because Submit may only send approved values.
"""
import hashlib
import json
import re
from datetime import date

# Documents a Form answer may be grounded in without an Answer bank row.
GROUNDING_SOURCES = ('master_resume', 'role_resume', 'career_goals')


def _normalized(text):
    return re.sub(r'\s+', ' ', text or '').strip().casefold()


def grounded_ready(question, grounded, grounding_sources):
    """A factual Form answer stated in, or mechanically derived from, a current source passage.

    Each item names the source, its exact current version, a verbatim quote and how the
    answer follows (formatting, arithmetic or choosing the matching option). Sensitive and
    Narrative questions never qualify; they need an approved or resolved answer.
    """
    if question.get('type') != 'Form' or question.get('sensitive') is not False:
        return False
    items = grounded if isinstance(grounded, list) else [grounded]
    if not items or not isinstance(grounding_sources, dict):
        return False
    for item in items:
        if not isinstance(item, dict) or item.get('source') not in GROUNDING_SOURCES:
            return False
        current = grounding_sources.get(item['source'])
        quote = item.get('quote')
        if (not isinstance(current, dict) or not current.get('version') or item.get('version') != current['version']
                or not has_answer(quote) or not has_answer(item.get('derivation'))
                or _normalized(quote) not in _normalized(current.get('text'))):
            return False
    return True

SCHEMA = 'nextmove.application-questions.v2'
# Agent notes is free-form remarks and is excluded: editing it never invalidates an approval.
BANK_FIELDS = ('Question', 'Answer', 'Additional guidance', 'Approved')
QUESTION_FIELDS = ('Question', 'Options', 'Field key', 'Question type',
                   'Final answer', 'Status', 'Application')


def answer_fingerprint(table, record):
    fields = BANK_FIELDS if table == 'Answer bank' else QUESTION_FIELDS if table == 'Application questions' else None
    if fields is None:
        raise ValueError('Unknown answer table')
    value = {k: record.get(k) for k in fields}
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def form_fingerprint(questions):
    fields = ('field_key', 'question', 'options', 'type', 'required')
    definitions = [{k: q.get(k) for k in fields} for q in questions]
    return hashlib.sha256(json.dumps(definitions, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def has_answer(value):
    return isinstance(value, str) and bool(value.strip())


def question_key(company_id, application_id, field_key):
    """Stable per-application discovery key; semantic cross-role reuse is separate."""
    if not all(isinstance(v, str) and v.strip() for v in (company_id, application_id, field_key)):
        raise ValueError('Company, application and exact employer field identity required')
    return hashlib.sha256(json.dumps([company_id, application_id, field_key], separators=(',', ':')).encode()).hexdigest()


def answer_ready(table, record, application, *, as_of):
    """Named, normalized live records, never select objects or cached statuses."""
    if table == 'Answer bank':
        # Variations and any company/role restriction live in Additional guidance; the harness verifies it when mapping.
        return record.get('Approved') is True and has_answer(record.get('Answer'))
    return bool(table == 'Application questions'
                and record.get('Status') == 'Resolved'
                and has_answer(record.get('Final answer'))
                and record.get('Application') == [application.get('id')])


def application_answers_ready(application, inspection, answer_bank, application_questions, *, as_of, current_form_hash=None, grounding_sources=None):
    """Fail closed on unknown form coverage, missing rows or changed approvals."""
    if not isinstance(inspection, dict) or answer_bank is None or application_questions is None:
        return False
    from stage_state import canonical_job_url
    if (inspection.get('schema') != SCHEMA or inspection.get('application_id') != application.get('id')
            or not application.get('id') or not application.get('Job key')
            or inspection.get('job_key') != application['Job key']
            or not inspection.get('job_url') or not application.get('Job description link')
            or canonical_job_url(inspection['job_url']) != canonical_job_url(application['Job description link'])
            or inspection.get('coverage') != 'complete' or not inspection.get('inspected_at')
            or not inspection.get('form_url') or not inspection.get('evidence')
            or inspection.get('blockers') != []):
        return False
    try:
        date.fromisoformat(as_of)
    except (ValueError, TypeError):
        return False
    questions = inspection.get('questions')
    if not isinstance(questions, list) or any(not isinstance(q, dict) for q in questions):
        return False
    if (not current_form_hash or inspection.get('form_hash') != current_form_hash
            or inspection.get('form_hash') != form_fingerprint(questions)):
        return False
    keys = [q.get('field_key') for q in questions if isinstance(q, dict)]
    if len(keys) != len(questions) or any(not k for k in keys) or len(set(keys)) != len(keys):
        return False
    tables = {'Answer bank': answer_bank, 'Application questions': application_questions}
    for q in questions:
        if (not has_answer(q.get('question')) or q.get('type') not in {'Form', 'Narrative'}
                or type(q.get('required')) is not bool or type(q.get('sensitive')) is not bool):
            return False
        if not q['required'] and not q['sensitive']:
            continue
        ref = q.get('answer') or {}
        if not isinstance(ref, dict):
            return False
        if (not has_answer(ref.get('mapped_answer')) or ref.get('mapping_verified') is not True
                or not has_answer(ref.get('match_evidence'))):
            return False
        if 'grounded' in ref:
            if any(k in ref for k in ('sources', 'table', 'record_id', 'fingerprint')):
                return False
            if not grounded_ready(q, ref['grounded'], grounding_sources):
                return False
            continue
        sources = ref.get('sources')
        if sources is not None:
            # Form wording may be assembled from multiple approved facts without
            # inventing another bank row. Every contributing approval stays live.
            if (q['type'] != 'Form' or not isinstance(sources, list) or not sources
                    or not has_answer(ref.get('composition'))
                    or any(k in ref for k in ('table', 'record_id', 'fingerprint'))):
                return False
        else:
            sources = [ref]
        seen = set()
        for source in sources:
            if not isinstance(source, dict):
                return False
            table, rid = source.get('table'), source.get('record_id')
            if table not in tables or not rid or (table, rid) in seen:
                return False
            seen.add((table, rid))
            rows = [r for r in tables[table] if r.get('id') == rid]
            if len(rows) != 1 or not answer_ready(table, rows[0], application, as_of=as_of):
                return False
            if source.get('fingerprint') != answer_fingerprint(table, rows[0]):
                return False
    return True
