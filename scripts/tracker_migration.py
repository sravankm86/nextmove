"""Pure migration helpers for the 28-column tracker; no account access or writes.

The harness supplies named live records and resolved complete snapshots, persists
the proposed state in History, rereads it, and only then consolidates display data.
"""
import copy

from stage_state import RETIRED_FIELDS, review_ready, stage_versions


def agent_notes(application):
    assessment = (application.get('Assessment summary') or '').strip()
    blocker = (application.get('Blocker') or '').strip()
    existing = (application.get('Agent notes') or '').strip()
    parts = [existing or assessment] if existing or assessment else []
    if blocker and blocker not in '\n'.join(parts):
        parts.append('Next: ' + blocker)
    return '\n'.join(parts) or (application.get('Decision category') or '').strip()


def migrate(application, previous, runs):
    """Preserve exact prior values; never manufacture review acceptance."""
    if not previous or previous.get('record_id') != application['id']:
        raise ValueError('A complete identity-matched prior snapshot is required')
    state = copy.deepcopy(previous)
    review = state.setdefault('review', {})
    for field, key, values in [
        ('Role eligibility', 'role_eligible', {'Eligible': True, 'Excluded': False}),
        ('Career gate', 'career_requirements_pass', {'Pass': True, 'Fail': False}),
    ]:
        if field in application:
            review[key] = values.get(application[field])
        else:
            review.setdefault(key, None)
    if application.get('Decision category'):
        review['reason_category'] = application['Decision category']
    source = state.setdefault('source', {})
    if 'Sources' in application:
        source['memberships'] = copy.deepcopy(application['Sources'])
    if 'Last seen at' in application:
        source['last_observed_at'] = application['Last seen at']
    state.setdefault('details', {})['tracker_migration_v7'] = {
        'previous_fields': {k: copy.deepcopy(application[k]) for k in RETIRED_FIELDS if k in application},
        'previous_primary_label': application.get('Application'),
        'posting_availability_policy': 'apply-form-only-v1',
    }
    status = application.get('Lifecycle status')
    if status == 'Needs eligibility':
        status = 'Need review'
    elif status in {'Queued', 'Shortlisted'}:
        versions = stage_versions(state, 'review', runs)
        current = {**versions, 'jd_hash': review.get('jd_hash')}
        if not review_ready({**application, 'Lifecycle status': 'Queued'}, state, runs, current):
            status = 'Need review'
        elif status == 'Shortlisted':
            # Legacy labels are not promoted by a storage migration.
            status = 'Need review'
    notes = agent_notes(application)
    state['details']['tracker_migration_v7'].update(agent_notes_after=notes, lifecycle_after=status)
    return state, notes, status
