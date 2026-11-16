"""Build the six-table public blueprint. No account access or provisioning."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def field(name, kind='singleLineText', choices=None):
    f = {'name': name, 'type': kind}
    if choices:
        f['options'] = {'choices': [{'name': x} for x in choices]}
    elif kind == 'number':
        f['options'] = {'precision': 0}
    elif kind == 'dateTime':
        f['options'] = {'dateFormat': {'name': 'iso'}, 'timeFormat': {'name': '24hour'}, 'timeZone': 'utc'}
    elif kind == 'date':
        f['options'] = {'dateFormat': {'name': 'iso'}}
    return f


def main():
    from lifecycle import STATUSES
    status = STATUSES
    execution = ['Pending', 'Running', 'Complete', 'Partial', 'Blocked', 'Failed', 'Interrupted', 'Cancelled', 'No work']
    tables = []

    def table(name, fields, key, purpose):
        tables.append({'name': name, 'business_key': key, 'description': purpose, 'fields': fields})

    table('Companies', [field('Company'), field('Company key'), field('Search status', 'singleSelect', ['Allow', 'Exclude']), field('Notes', 'multilineText'), field('Max applications', 'number'), field('Application window (days)', 'number'), field('Application window type'), field('Rejection cooldown (days)', 'number'), field('Restriction scope'), field('Apply blocked until', 'dateTime'), field('Application hold status', 'singleSelect', ['Not assessed', 'No known hold', 'Held', 'Needs clarification']), field('Restriction details / source', 'multilineText'), field('Restriction timezone')], 'Company key', 'Explicit company choices and confirmed simple quota/cooldown rules. Complex unclear rules block submission; no automatic Allow.')
    app = [field('Application ID', 'formula'), field('Role'), field('Job key'), field('Job description link', 'url'), field('Lifecycle status', 'singleSelect', status), field('Manual notes', 'multilineText'), field('Posted salary range'), field('Additional compensation', 'multipleSelects', ['Equity', 'Bonus', 'Commission', 'Bonus or commission', 'Not stated']), field('Location'), field('Work arrangement', 'singleSelect', ['Remote', 'Hybrid', 'On-site', 'Unspecified']), field('Job posted date', 'date'), field('Role eligibility', 'singleSelect', ['Pending', 'Eligible', 'Excluded']), field('Career fit', 'singleSelect', ['High', 'Medium', 'Low', 'Unresolved']), field('Resume fit', 'singleSelect', ['High', 'Medium', 'Low', 'Unresolved']), field('Agent notes', 'multilineText'), field('Job evidence', 'url'), field('Resume link', 'url'), field('Resume version'), field('Resume verified at', 'dateTime'), field('Submission attempt key'), field('Applied on', 'date'), field('Confirmation reference', 'multilineText')]
    app[0]['options'] = {'formula': 'RECORD_ID()'}
    table('Applications', app, 'Canonical Job key; native record ID for preserved unmatched history', '28 physical fields including relationships. Current job facts, nine-state lifecycle, human/agent notes and readiness references live here; bounded stage snapshots in History join fixed shared inputs in Runs under DATA.md.')
    tables[-1]['common_fields'] = []  # Native record IDs/createdTime need no duplicate columns.
    table('Sources', [field('Source key'), field('Official careers URL', 'url'), field('Catalog URL', 'url'), field('Region'), field('Reader'), field('Reader version'), field('Latest coverage', 'singleSelect', ['Complete', 'Partial', 'Failed', 'Unverified']), field('Checkpoint (JSON)', 'multilineText'), field('Last error', 'multilineText'), field('Last scanned at', 'dateTime'), field('Archived at', 'dateTime')], 'Source key', 'One official board/region. Enumerate all pages transiently; preserve coverage and minimal source/identity checks; plausible role/scope ambiguities are inventoried for Review.')
    table('Runs', [field('Run key'), field('Run type', 'singleSelect', ['Full run', 'Scan', 'Review', 'Prepare', 'Apply', 'Track', 'Migration', 'Experiment']), field('Status', 'singleSelect', execution), field('Owner'), field('Instruction revision'), field('Input versions (JSON)', 'multilineText'), field('Scope (JSON)', 'multilineText'), field('Checkpoint (JSON)', 'multilineText'), field('Expected items', 'number'), field('Completed items', 'number'), field('Blocked items', 'number'), field('Started at', 'dateTime'), field('Finished at', 'dateTime'), field('Agent notes', 'multilineText')], 'Run key', 'One row per full run by default; manual stage invocations use the identical checkpoint/handoff shape. No per-job work-item or general attempt tables.')
    table('Settings', [field('Key'), field('Value', 'multilineText'), field('Reference URL', 'url'), field('Version'), field('Verification', 'singleSelect', ['Located', 'Verified', 'Missing', 'Needs verification', 'Inaccessible']), field('Notes', 'multilineText')], 'Key', 'Private resource references, criteria, scope and live controls. Instructions/command routes stay in Git.')
    table('History', [field('Event key'), field('Operation ID'), field('Event type'), field('Recorded at', 'dateTime'), field('Occurred at', 'dateTime'), field('Actor / channel'), field('Table reference'), field('Record reference'), field('Field changes (JSON)', 'multilineText'), field('Evidence URL', 'url'), field('Notes', 'multilineText')], 'Event key', 'Meaningful mutations and business events; failed/uncertain operations retain evidence. No routine per-read/per-row access logging. Not a universal immutable audit system.')
    links = [
        ('Applications', 'Company', 'Companies', '0..1'),
        ('Sources', 'Company', 'Companies', '1'), ('Sources', 'Last run', 'Runs', '0..1'),
        ('History', 'Application', 'Applications', 'many'), ('History', 'Run', 'Runs', '0..1'),
        ('Applications', 'Scan run', 'Runs', '0..1'), ('Applications', 'Review run', 'Runs', '0..1'), ('Applications', 'Preparation run', 'Runs', '0..1'), ('Applications', 'Submission run', 'Runs', '0..1')]
    common = []  # Native record metadata is not duplicated into every table.
    for definition in tables:
        definition['common_fields'] = []
    result = {'version': 9, 'description': 'Six-table logical blueprint, not raw connector request payloads. Map and preserve existing fields by ID; computed metadata never receives input values. DATA.md defines compact displays, manual feedback and view visibility.', 'tables': tables, 'links': [{'from_table': a, 'field': b, 'target_table': c, 'cardinality': d} for a,b,c,d in links], 'common_fields': common, 'legacy_aliases': {'Companies': ['Target Companies'], 'Sources': ['Catalog Sources'], 'Settings': ['Controls', 'Context Registry'], 'Runs': ['Stage Runs', 'Runs'], 'History': ['Audit Events', 'Lifecycle Events']}}
    inverse = {('Applications','Company'):'Applications',('Sources','Company'):'Sources',('Sources','Last run'):'Sources',('History','Run'):'History'}
    for link in result['links']:
        if (link['from_table'],link['field']) in inverse:
            link['inverse_field'] = inverse[(link['from_table'],link['field'])]
        if link['from_table'] == 'History' and link['field'] == 'Application':
            link['inverse_field'] = 'History'
        elif link['from_table'] == 'Applications' and link['target_table'] == 'Runs':
            link['inverse_field'] = link['field'].replace(' run', ' applications')
    from stage_state import CORE_FIELDS
    result['application_required_fields'] = CORE_FIELDS
    (ROOT/'contracts/core-schema.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
