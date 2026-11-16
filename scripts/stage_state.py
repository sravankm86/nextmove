"""Versioned stage metadata in History, joined to fixed inputs in Runs.

Pure readers/guards: no credentials, network access, orchestration or submissions.
Fetch linked History/Run records through the harness and map field IDs first.
"""
import hashlib
import json

SCHEMA = 'nextmove.stage-state.v2'
READ_SCHEMAS = {'nextmove.stage-state.v1', SCHEMA}
RUN_LINKS = {'scan': 'Scan run', 'review': 'Review run', 'preparation': 'Preparation run', 'submission': 'Submission run'}
CORE_FIELDS = ['Application ID','Company','Role','Job key','Job description link','Lifecycle status','Manual notes','Agent notes','Posted salary range','Additional compensation','Location','Work arrangement','Job posted date','Role eligibility','Career fit','Resume fit','Job evidence','Resume link','Resume version','Resume verified at','Submission attempt key','Applied on','Confirmation reference','History','Scan run','Review run','Preparation run','Submission run']
RETIRED_FIELDS = ['Record kind','Availability','Sources','Last seen at','Career gate','Assessment summary','Blocker','Decision category','Updated at']


def application_write(values, *, creating=False, existing_keys=None, allowed_companies=None):
    """Only current fields can be written; legacy plans cannot recreate retired data."""
    bad = set(values) - (set(CORE_FIELDS) - {'Application ID', 'History'})
    if bad:
        raise ValueError('Unsupported/retired Application fields: '+', '.join(sorted(bad)))
    from lifecycle import STATUSES
    if 'Lifecycle status' in values and values['Lifecycle status'] not in STATUSES:
        raise ValueError('Unsupported lifecycle status; migrate legacy labels explicitly')
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
        if allowed_companies is None or company[0] not in allowed_companies:
            raise ValueError('New candidate company must be explicitly allowed')
        if values.get('Lifecycle status') != 'Inventoried' or values.get('Role eligibility') != 'Pending':
            raise ValueError('Scan cannot certify eligibility or queue a new candidate')
    return values


def plain(value):
    if isinstance(value, dict) and 'name' in value:
        return value['name']
    if isinstance(value, list):
        return [v.get('id') if isinstance(v, dict) and str(v.get('id', '')).startswith('rec') else plain(v) for v in value]
    return value


def named_records(records, fields, aliases=None):
    labels = {f['id']: f['name'] for f in fields}
    aliases = aliases or {}
    result = []
    for r in records:
        values = {aliases.get(labels.get(k, k), labels.get(k, k)): plain(v) for k, v in r.get('cellValuesByFieldId', {}).items()}
        result.append({'id': r['id'], 'createdTime': r.get('createdTime'), **values})
    return result


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


def review_ready(app, state, runs, current_inputs):
    if not state or app.get('Lifecycle status') != 'Queued':
        return False
    if app.get('Role eligibility') != 'Eligible':
        return False
    if 'High' not in [app.get('Career fit'), app.get('Resume fit')]:
        return False
    review = state.get('review', {})
    if review.get('role_eligible') is not True or review.get('career_requirements_pass') is not True:
        return False
    rid = state.get('stage_runs', {}).get('review')
    if not rid or app.get('Review run') != [rid] or review.get('decision') != 'approve':
        return False
    versions = stage_versions(state, 'review', runs)
    # Deployment/schema-only commits do not change a decision policy. Record the
    # instruction revision for audit; compare the versioned decision rules.
    if not all(versions.get(k) and versions.get(k) == current_inputs.get(k) for k in ['goals', 'master', 'policy', 'eligibility_policy']):
        return False
    return bool(review.get('jd_hash') and review['jd_hash'] == current_inputs.get('jd_hash') and review.get('current_description'))


def resume_ready(app, state, runs, current_inputs, pdf_bytes=None, *, provider_version=None):
    candidate = {**app, 'Lifecycle status': 'Queued'}
    if not review_ready(candidate, state, runs, current_inputs):
        return False
    p = state.get('preparation', {})
    rid = state.get('stage_runs', {}).get('preparation')
    digest = hashlib.sha256(pdf_bytes).hexdigest() if pdf_bytes is not None else provider_version
    return bool(rid and app.get('Preparation run') == [rid]
                and app.get('Resume verified at') and app.get('Resume link')
                and digest and p.get('verified') and (p.get('resume_version') or p.get('resume_hash')) == digest == app.get('Resume version')
                and p.get('master') == current_inputs.get('master')
                and p.get('jd_hash') == current_inputs.get('jd_hash')
                and p.get('goals') == current_inputs.get('goals'))


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


def run_progress(run, *, progress_contexts=None):
    """Read merged current progress plus legacy separate fields without writing pins."""
    def parsed(value):
        if value in [None, '']:
            return None
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return value
        return value
    base = parsed(run.get('Checkpoint (JSON)'))
    result = dict(base) if isinstance(base, dict) else ({'legacy_checkpoint_raw': base} if base is not None else {})
    context = (progress_contexts or {}).get(run.get('id'))
    if context and result.get('_progress_context_event') != context['event_id']:
        raw = run.get('Checkpoint (JSON)')
        digest = hashlib.sha256((raw or '').encode()).hexdigest() if isinstance(raw, (str, type(None))) else None
        if digest not in context['accepted_checkpoint_hashes']:
            raise ValueError('Run progress changed after preservation; reconcile the context')
        result = json.loads(json.dumps(context['checkpoint']))
        result['_progress_context_event'] = context['event_id']
    for field, key in [('Stages (JSON)', 'stages'), ('Pending checks (JSON)', 'pending_checks'),
                       ('Handoff (JSON)', 'handoff'), ('Next command', 'next_action'),
                       ('Mode', 'execution_mode'), ('Backup/report URL', 'report_url')]:
        value = parsed(run.get(field))
        if key not in result and value is not None:
            result[key] = value
    return result


def run_progress_contexts(histories):
    """Resolve immutable progress preservation records without rewriting old Runs."""
    matches = {}
    for event in histories:
        try:
            data = json.loads(event.get('Field changes (JSON)', '{}'))
        except (ValueError, TypeError):
            continue
        if not isinstance(data, dict) or data.get('schema') != 'nextmove.run-progress.v1':
            continue
        run_id = data['original_run_id']
        rank = (event.get('Recorded at', ''), event.get('Event key', ''))
        if run_id not in matches or rank > matches[run_id][0]:
            matches[run_id] = (rank, {'event_id': event['id'],
                'accepted_checkpoint_hashes': data['accepted_checkpoint_hashes'],
                'checkpoint': data['checkpoint']})
    return {key: value[1] for key, value in matches.items()}
