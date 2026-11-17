"""Versioned stage metadata in History, joined to fixed inputs in Runs.

Pure readers/guards: no credentials, network access, orchestration or submissions.
Fetch linked History/Run records through the harness and map field IDs first.
"""
import hashlib
import json
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SCHEMA = 'nextmove.stage-state.v2'
READ_SCHEMAS = {'nextmove.stage-state.v1', SCHEMA}
RUN_LINKS = {'scan': 'Scan run', 'review': 'Review run', 'preparation': 'Preparation run', 'submission': 'Submission run'}
CORE_FIELDS = ['Application ID','Company','Role','Job key','Job description link','Lifecycle status','Manual notes','Agent notes','Starting salary','Max salary','Additional compensation','Location','Work arrangement','Job posted date','Role eligibility','Career fit','Resume fit','Job evidence','Resume link','Resume version','Resume verified at','Submission attempt key','Applied on','Confirmation reference','History','Scan run','Review run','Preparation run','Submission run']


def application_write(values, *, creating=False, existing_keys=None, allowed_companies=None, companies=None):
    """Only the 29 current fields can be written."""
    bad = set(values) - (set(CORE_FIELDS) - {'Application ID', 'History'})
    if bad:
        raise ValueError('Unsupported Application fields: '+', '.join(sorted(bad)))
    from lifecycle import STATUSES
    if 'Lifecycle status' in values and values['Lifecycle status'] not in STATUSES:
        raise ValueError('Unsupported lifecycle status')
    for label in ['Company', 'Scan run', 'Review run', 'Preparation run', 'Submission run']:
        if label in values and len(values[label] or []) > 1:
            raise ValueError('Expected at most one linked record: '+label)
    if creating:
        key = values.get('Job key')
        company = values.get('Company') or []
        if not key or not values.get('Role') or len(company) != 1:
            raise ValueError('New candidates require canonical identity, title and company')
        if existing_keys is None or key in existing_keys:
            raise ValueError('Canonical job key must be checked against live existing keys')
        from company_policy import company_for_application
        if not company_for_application(values, companies):
            raise ValueError('Current company records must confirm Allow and no permanent block')
        if allowed_companies is not None and company[0] not in allowed_companies:
            raise ValueError('Company is outside the frozen scan scope')
        if values.get('Lifecycle status') != 'Inventoried' or values.get('Role eligibility') != 'Pending':
            raise ValueError('Scan cannot certify eligibility or queue a new candidate')
    return values


def payload(records):
    ids = [r['record_id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate application identity in stage-state batch')
    return {'schema': SCHEMA, 'records': records}


def resolve(application, histories):
    """Return the newest complete metadata snapshot, never infer approval from status."""
    matches = []
    for event in histories:
        raw = event.get('Field changes (JSON)', {})
        try:
            data = json.loads(raw) if isinstance(raw, str) else raw
        except (ValueError, TypeError):
            continue
        if not isinstance(data, dict) or data.get('schema') not in READ_SCHEMAS:
            continue
        for state in data.get('records', []):
            if state.get('record_id') == application['id']:
                matches.append((event.get('Recorded at', ''), event.get('Event key', ''), state))
    if not matches:
        return None
    return max(matches, key=lambda x: (x[0], x[1]))[2]


def stage_versions(state, stage, runs):
    rid = state.get('stage_runs', {}).get(stage)
    run = next((r for r in runs if r['id'] == rid), None)
    raw = (run or {}).get('Input versions (JSON)', {})
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except (ValueError, TypeError):
        data = {}
    common = (data or {}).get('stage_inputs', {}).get(stage, {})
    return {**common, **state.get(stage, {}).get('version_overrides', {})}


def review_ready(app, state, runs, current_inputs, *, companies=None):
    from company_policy import company_for_application
    if not company_for_application(app, companies):
        return False
    if not state or app.get('Lifecycle status') != 'Queued':
        return False
    if app.get('Role eligibility') != 'Eligible':
        return False
    review = state.get('review', {})
    from role_gate import review_frame_contract, scored_review
    frame_policy, contract = review_frame_contract()
    if current_inputs.get('policy') != frame_policy:
        return False
    if review.get('assessment_method') != contract['assessment_method']:
        return False
    saved = review.get('scoring', {})
    try:
        expected = scored_review(app.get('Career fit'), app.get('Resume fit'))
    except (ValueError, KeyError, TypeError):
        return False
    if saved != expected or expected['outcome'] != 'Queued' or review.get('decision') != 'approve':
        return False
    if not review.get('evidence') or not review.get('assessment_complete'):
        return False
    check = state.get('run_checks', {}).get('duplicate', {})
    rid = state.get('stage_runs', {}).get('review')
    if (check.get('status') not in {'unique', 'canonical'} or not check.get('evidence')
            or check.get('checked_in_run') != rid or app.get('Review run') != [rid]):
        return False
    versions = stage_versions(state, 'review', runs)
    return bool(all(versions.get(k) and versions[k] == current_inputs.get(k)
                    for k in ['goals', 'master', 'policy', 'eligibility_policy', 'company_evidence'])
                and review.get('jd_hash') == current_inputs.get('jd_hash')
                and review.get('jd_hash') and review.get('current_description'))


def apply_ready(app, state, runs, current_inputs, pdf_bytes=None, *, provider_version=None, companies=None):
    """Ready, no open attempt and a verified resume; submission policy and holds are separate checks."""
    return bool(app.get('Lifecycle status') == 'Ready'
                and not attempt_blocks_retry(app, state)
                and resume_ready(app, state, runs, current_inputs, pdf_bytes,
                                 provider_version=provider_version, companies=companies))


def canonical_job_url(value):
    """Normalize an exact posting link; retain job-identifying query values."""
    if not value:
        return None
    parts = urlsplit(value.strip())
    if parts.scheme not in {'http', 'https'} or not parts.netloc:
        return None
    tracking = {'gh_src', 'lever-source', 'ashby_source'}
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in tracking]
    return urlunsplit(('https', parts.netloc.lower().removeprefix('www.'),
                       parts.path.rstrip('/'), urlencode(sorted(query)), parts.fragment))


def resume_ready(app, state, runs, current_inputs, pdf_bytes=None, *, provider_version=None, companies=None):
    candidate = {**app, 'Lifecycle status': 'Queued'}
    if not review_ready(candidate, state, runs, current_inputs, companies=companies):
        return False
    p = state.get('preparation', {})
    rid = state.get('stage_runs', {}).get('preparation')
    digest = hashlib.sha256(pdf_bytes).hexdigest() if pdf_bytes is not None else provider_version
    return bool(rid and app.get('Preparation run') == [rid]
                and app.get('Resume verified at') and app.get('Resume link')
                and digest and p.get('verified') and (p.get('resume_version') or p.get('resume_hash')) == digest == app.get('Resume version')
                and p.get('master') == current_inputs.get('master')
                and p.get('jd_hash') == current_inputs.get('jd_hash')
                and p.get('goals') == current_inputs.get('goals')
                and preparation_complete(p, current_inputs, digest))


PREPARATION_PATHS = ('base_reuse', 'tailored')


def preparation_complete(p, current_inputs, digest):
    """Prepare's two paths under stages/prepare.md; each needs its own evidence.

    base_reuse: an approved base built from the current master covers every critical
    requirement and main theme; the exact base PDF is the role resume.
    tailored: a new role version derived from the closest base, grounded claim by claim in
    the master and checked against the registered resume guidelines.
    """
    path = p.get('path')
    if path not in PREPARATION_PATHS:
        return False
    if current_inputs.get('resume_guidelines') and p.get('guidelines') != current_inputs['resume_guidelines']:
        return False
    if p.get('company_consistency') not in ('pass', 'not_applicable'):
        return False
    if path == 'base_reuse':
        return bool(p.get('base') and p.get('coverage') == 'complete'
                    and p.get('base_master') == current_inputs.get('master')
                    and p.get('base_version') == digest)
    return bool(p.get('base') and p.get('grounding') == 'pass' and p.get('guideline_check') == 'pass'
                and p.get('base_version') != digest)


def attempt_blocks_retry(app, state):
    """An existing attempt is reconciled before any new submit, regardless of UI state."""
    return bool(app.get('Submission attempt key') or (state or {}).get('submission', {}).get('attempt_key'))


def merge_state(previous, *, record_id, job_key, stage, run_id, values):
    if stage not in RUN_LINKS:
        raise ValueError('Unknown stage')
    previous = previous or {'record_id': record_id, 'job_key': job_key, 'stage_runs': {}}
    if previous['record_id'] != record_id:
        raise ValueError('Application identity mismatch')
    result = json.loads(json.dumps(previous))
    result['stage_runs'][stage] = run_id
    result[stage] = values
    return result


def merge_company_state(previous, *, company_id, company_key, run_id, values):
    """Curate history uses company identity, never an Application or Job key."""
    previous = previous or {'record_id': company_id, 'entity': 'company',
                            'company_key': company_key, 'stage_runs': {}}
    if previous.get('record_id') != company_id or previous.get('entity') != 'company':
        raise ValueError('Company identity mismatch')
    result = json.loads(json.dumps(previous))
    result['stage_runs']['curate'] = run_id
    result['curate'] = values
    return result


def run_progress(run):
    """Parse a Run's Checkpoint (JSON); non-JSON text is kept under raw_checkpoint."""
    raw = run.get('Checkpoint (JSON)')
    if raw in (None, ''):
        return {}
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (ValueError, TypeError):
            return {'raw_checkpoint': raw}
    return dict(raw) if isinstance(raw, dict) else {'raw_checkpoint': raw}


def run_duplicate_match(left, right):
    """Run-owned objective identity. Titles/dates corroborate, never prove identity."""
    if not left.get('company_id') or left.get('company_id') != right.get('company_id'):
        return {'decision': 'distinct', 'basis': 'different or unknown company'}
    lid = left.get('role_id') if left.get('role_id_verified') is True else None
    rid = right.get('role_id') if right.get('role_id_verified') is True else None
    lu = canonical_job_url(left.get('job_url')) if left.get('job_url_verified_specific') is True else None
    ru = canonical_job_url(right.get('job_url')) if right.get('job_url_verified_specific') is True else None
    same_link = bool(lu and lu == ru)
    if lid and rid:
        if lid == rid:
            return {'decision': 'duplicate', 'basis': 'verified company-scoped employer role ID'}
        return {'decision': 'unresolved' if same_link else 'distinct',
                'basis': 'conflicting verified IDs/link' if same_link else 'distinct verified role IDs'}
    if same_link:
        return {'decision': 'duplicate', 'basis': 'verified exact posting-specific canonical link'}
    name = lambda x: ' '.join((x or '').casefold().split())
    if (name(left.get('role_name')) and name(left.get('role_name')) == name(right.get('role_name'))
            and left.get('posted_date') and left.get('posted_date') == right.get('posted_date')):
        return {'decision': 'unresolved', 'basis': 'same title/date only; exact identity needs verification'}
    return {'decision': 'distinct', 'basis': 'no confirmed shared posting identity'}
