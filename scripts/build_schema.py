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
    status = ['Needs eligibility', 'Inventoried', 'Not aligned', 'Queued', 'Shortlisted', 'Not a fit', 'Ready', 'Applied', 'Confirmed', 'In process', 'Offer', 'Accepted', 'Rejected', 'Withdrawn', 'Not pursuing', 'Closed', 'Needs review', 'Submission uncertain', 'Duplicate']
    execution = ['Pending', 'Running', 'Complete', 'Partial', 'Blocked', 'Failed', 'Interrupted', 'Cancelled', 'No work']
    tables = []

    def table(name, fields, key, purpose):
        tables.append({'name': name, 'business_key': key, 'description': purpose, 'fields': fields})

    table('Companies', [field('Company'), field('Company key'), field('Search status', 'singleSelect', ['Allow', 'Exclude']), field('Pool'), field('Notes', 'multilineText'), field('Max applications', 'number'), field('Application window (days)', 'number'), field('Application window type'), field('Rejection cooldown (days)', 'number'), field('Restriction scope'), field('Apply blocked until', 'dateTime'), field('Application hold status', 'singleSelect', ['Not assessed', 'No known hold', 'Held', 'Needs clarification']), field('Restriction details / source', 'multilineText'), field('Last rejection date', 'date'), field('Restriction last verified', 'date'), field('Restriction timezone')], 'Company key', 'Explicit company choices and confirmed simple quota/cooldown rules. Complex unclear rules block submission; no automatic Allow.')
    app = [field('Application'), field('Job key'), field('Company name'), field('Role'), field('Job description link', 'url'), field('Lifecycle status', 'singleSelect', status)]
    app += [field('Scan evidence', 'multilineText'), field('Scan policy version'), field('Decision category'), field('Decision reason', 'multilineText'), field('Feedback versions (JSON)', 'multilineText')]
    app += [field('Role eligibility', 'singleSelect', ['Pending', 'Eligible', 'Excluded']), field('Eligibility evidence', 'multilineText'), field('Eligibility policy version'), field('Career gate', 'singleSelect', ['Pending', 'Pass', 'Fail']), field('Career evidence', 'multilineText'), field('Career goals version')]
    app += [field('Description content (Drive)', 'url'), field('Description status'), field('Availability'), field('Posted salary range', 'multilineText'), field('Location'), field('Work arrangement'), field('Job posted date', 'date'), field('First seen at', 'dateTime'), field('Last seen at', 'dateTime')]
    app += [field('Career fit', 'singleSelect', ['High', 'Medium', 'Low', 'Unresolved']), field('Resume fit', 'singleSelect', ['High', 'Medium', 'Low', 'Unresolved']), field('Fit rationale - Career goals', 'multilineText'), field('Fit rationale - Resume', 'multilineText'), field('Resume link', 'url'), field('Resume file name'), field('Resume version'), field('Resume verified at', 'dateTime'), field('Resume notes', 'multilineText'), field('Evidence versions (JSON)', 'multilineText'), field('Submission attempt key'), field('Submitted resume version'), field('Confirmation reference', 'multilineText'), field('Applied on', 'date'), field('Confirmed on', 'date'), field('Outcome on', 'date'), field('Blocker', 'multilineText')]
    table('Applications', app, 'Job key for canonical roles; immutable record identity for preserved legacy history', 'Plausible PM candidates become Inventoried after basic semantics. Review owns full eligibility/career/resume acceptance before Queued. Needs eligibility and Shortlisted are legacy aliases only; preserve historical outcomes.')
    table('Sources', [field('Source'), field('Source key'), field('Official careers URL', 'url'), field('Catalog URL', 'url'), field('Region'), field('Reader reference', 'url'), field('Reader version'), field('Latest coverage', 'singleSelect', ['Complete', 'Partial', 'Failed', 'Unverified']), field('Checkpoint (JSON)', 'multilineText'), field('Last error', 'multilineText'), field('Last scanned at', 'dateTime')], 'Source key', 'One official board/region. Enumerate all pages transiently; preserve coverage and minimal source/identity checks; plausible role/scope ambiguities are inventoried for Review.')
    table('Runs', [field('Run key'), field('Run type', 'singleSelect', ['Full run', 'Scan', 'Review', 'Prepare', 'Apply', 'Track', 'Migration', 'Experiment']), field('Status', 'singleSelect', execution), field('Mode', 'singleSelect', ['review', 'prepare', 'auto-apply']), field('Owner'), field('Instruction revision'), field('Input versions (JSON)', 'multilineText'), field('Scope (JSON)', 'multilineText'), field('Stages (JSON)', 'multilineText'), field('Checkpoint (JSON)', 'multilineText'), field('Pending checks (JSON)', 'multilineText'), field('Expected items', 'number'), field('Completed items', 'number'), field('Blocked items', 'number'), field('Started at', 'dateTime'), field('Finished at', 'dateTime'), field('Handoff (JSON)', 'multilineText'), field('Backup/report URL', 'url'), field('Blockers', 'multilineText')], 'Run key', 'One row per full run by default; manual stage invocations use the identical checkpoint/handoff shape. No per-job work-item or general attempt tables.')
    table('Settings', [field('Key'), field('Value', 'multilineText'), field('Reference URL', 'url'), field('Version'), field('Verification', 'singleSelect', ['Located', 'Verified', 'Missing', 'Needs verification', 'Inaccessible']), field('Required by'), field('Notes', 'multilineText')], 'Key', 'Private resource references, criteria, scope and live controls. Instructions/command routes stay in Git.')
    table('History', [field('Event key'), field('Operation ID'), field('Event type'), field('Recorded at', 'dateTime'), field('Occurred at', 'dateTime'), field('Actor / channel'), field('Table reference'), field('Record reference'), field('Field changes (JSON)', 'multilineText'), field('Evidence URL', 'url'), field('Notes', 'multilineText')], 'Event key', 'Meaningful mutations and business events; failed/uncertain operations retain evidence. No routine per-read/per-row access logging. Not a universal immutable audit system.')
    links = [
        ('Applications', 'Company', 'Companies', '0..1'), ('Applications', 'Sources', 'Sources', 'many'),
        ('Sources', 'Company', 'Companies', '1'), ('Sources', 'Last run', 'Runs', '0..1'),
        ('History', 'Application', 'Applications', 'many'), ('History', 'Run', 'Runs', '0..1')]
    common = [field('Record ID', 'formula'), field('System created at', 'createdTime'), field('System updated at', 'lastModifiedTime'), field('Created by', 'createdBy'), field('Updated by', 'lastModifiedBy'), field('Archived at', 'dateTime')]
    common[0]['options'] = {'formula': 'RECORD_ID()'}
    result = {'version': 4, 'description': 'Six-table logical blueprint, not raw connector request payloads. Map and preserve existing fields by ID; computed metadata never receives input values.', 'tables': tables, 'links': [{'from_table': a, 'field': b, 'target_table': c, 'cardinality': d} for a,b,c,d in links], 'common_fields': common, 'legacy_aliases': {'Companies': ['Target Companies'], 'Sources': ['Catalog Sources'], 'Settings': ['Controls', 'Context Registry'], 'Runs': ['Stage Runs', 'Runs'], 'History': ['Audit Events', 'Lifecycle Events']}}
    (ROOT/'contracts/core-schema.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
