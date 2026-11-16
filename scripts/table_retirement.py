"""Pure consolidation helpers; the harness owns preservation and verified writes."""
import copy
import json

from stage_state import run_progress


def parsed(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return value
    return copy.deepcopy(value)


def source_checkpoint(source):
    """Keep the current cursor/proof and the retired reader/source context."""
    value = parsed(source.get('Checkpoint (JSON)'))
    result = copy.deepcopy(value) if isinstance(value, dict) else ({'legacy_checkpoint_raw': value} if value not in [None, ''] else {})
    context = copy.deepcopy(result.get('source_context', {}))
    if not isinstance(context, dict):
        raise ValueError('Existing source_context must be reconciled before migration')
    for field, key in [('source_verification', 'verification'), ('Manifest version', 'manifest_version'),
                       ('Pagination contract (JSON)', 'pagination'), ('run_id', 'legacy_run_key'),
                       ('snapshot_at', 'legacy_observed_at'), ('Reader reference', 'reader_reference')]:
        if source.get(field) in [None, '']:
            continue
        value = parsed(source[field])
        if key in context and context[key] != value:
            raise ValueError('Conflicting source context: ' + key)
        context[key] = value
    if context:
        result['source_context'] = context
    return result


def consolidated_run(run):
    """Never replace current progress with a conflicting legacy fragment."""
    checkpoint = parsed(run.get('Checkpoint (JSON)'))
    checkpoint = checkpoint if isinstance(checkpoint, dict) else {}
    for field, key in [('Stages (JSON)', 'stages'), ('Pending checks (JSON)', 'pending_checks'),
                       ('Handoff (JSON)', 'handoff'), ('Next command', 'next_action'),
                       ('Mode', 'execution_mode'), ('Backup/report URL', 'report_url')]:
        if field in run and run[field] not in [None, ''] and key in checkpoint and parsed(run[field]) != checkpoint[key]:
            raise ValueError('Conflicting Run progress: ' + key)
    return run_progress(run)


def historical_event_type(event):
    """Classify only from recorded facts; preserve existing event labels."""
    if event.get('Event type'):
        return event['Event type']
    operation, phase = event.get('Operation'), event.get('Phase')
    if not operation:
        raise ValueError('Missing event classification evidence')
    return str(operation) + (' / ' + str(phase) if phase else '')
