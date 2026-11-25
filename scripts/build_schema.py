"""Build the nine-table public blueprint. No account access or provisioning."""
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
    tables = []

    def table(name, fields, key, purpose):
        tables.append({'name': name, 'business_key': key, 'description': purpose, 'fields': fields})

    from company_policy import SEARCH_STATUSES, FUNDING_STAGES
    table('Companies', [field('Company'), field('Company key'), field('Search status', 'singleSelect', SEARCH_STATUSES), field('Manual notes', 'multilineText'), field('Feedback', 'multilineText'), field('Agent notes', 'multilineText'), field('Funding stage', 'singleSelect', FUNDING_STAGES), field('Company evidence', 'url'), field('Careers URLs', 'multilineText'), field('Last scanned', 'dateTime'), field('Scan notes', 'multilineText')], 'Company key', 'Human targeting, agent-discovered Proposed companies, funding and company evidence, plus the official careers boards Scan reads (one URL per line, with region when relevant) and the latest scan result. No automatic Allow.')
    app = [field('Application ID', 'formula'), field('Role'), field('Job key'), field('Job description link', 'url'), field('Lifecycle status', 'singleSelect', status), field('Manual notes', 'multilineText'), field('Feedback', 'multilineText'), field('Starting salary', 'number'), field('Max salary', 'number'), field('Additional compensation', 'multipleSelects', ['Equity', 'Bonus', 'Commission', 'Bonus or commission', 'Not stated']), field('Location'), field('Work arrangement', 'singleSelect', ['Remote', 'Hybrid', 'On-site', 'Unspecified']), field('Job posted date', 'date'), field('Career fit', 'singleSelect', ['High', 'Medium', 'Low', 'Unresolved']), field('Resume fit', 'singleSelect', ['High', 'Medium', 'Low', 'Unresolved']), field('Agent notes', 'multilineText'), field('Job evidence', 'url'), field('Resume link', 'url'), field('Resume version'), field('Resume verified at', 'dateTime'), field('Evidence (JSON)', 'multilineText')]
    app[0]['options'] = {'formula': 'RECORD_ID()'}
    table('Applications', app, 'Canonical Job key; native record ID for preserved unmatched history', 'Current job facts, lifecycle, human/agent notes, resume references and the role\'s current stage evidence (Evidence (JSON), DATA.md). The Audit log records how it got here.')
    table('Settings', [field('Key'), field('Value', 'multilineText'), field('Reference URL', 'url'), field('Version'), field('Verification', 'singleSelect', ['Located', 'Verified', 'Missing', 'Needs verification', 'Inaccessible']), field('Notes', 'multilineText')], 'Key', 'Private resource references, criteria, scope and live controls. Instructions/command routes stay in Git.')
    table('Audit log', [field('Event key'), field('Recorded at', 'dateTime'), field('Agent'), field('Action'), field('Table reference'), field('Record reference'), field('Summary', 'multilineText'), field('Details (JSON)', 'multilineText'), field('Evidence URL', 'url')], 'Event key', 'Append-only record of every agent action and decision: when, which agent, what changed and why, with before/after values and evidence links. The full timeline can be rebuilt from it; stages never need it to decide.')
    from review_eval import VERDICTS, REASON_TYPES, SPLITS, PREDICTIONS
    table('Review eval', [field('Example'), field('Application record'), field('Job link', 'url'), field('Your verdict', 'singleSelect', VERDICTS), field('Reason', 'multilineText'), field('Reason type', 'singleSelect', REASON_TYPES), field('Split', 'singleSelect', SPLITS), field('Active', 'checkbox'), field('Inputs snapshot', 'url'), field('Last prediction', 'singleSelect', PREDICTIONS), field('Last eval'), field('Added on', 'date'), field('Match', 'formula')], 'Application record', 'Golden answer key for Review built from the user\'s graded Feedback: frozen verdict and reason, holdout split, the latest eval prediction and its match. Self-contained (no links) so Applications gains no columns. DATA.md "Review eval".')
    table('Answer bank', [field('Question'), field('Answer', 'multilineText'), field('Additional guidance', 'multilineText'), field('Agent notes', 'multilineText'), field('Approved', 'checkbox')], 'Native record ID; question meaning and Additional guidance scope checked before create', 'Reusable user-provided Form answers. Only a nonempty Answer with Approved ticked is ready; other phrasings it covers and any company or role restriction are written in Additional guidance; Agent notes holds agent remarks.')
    table('Application questions', [field('Question ID'), field('Question', 'multilineText'), field('Draft answer', 'multilineText'), field('Final answer', 'multilineText'), field('Status', 'singleSelect', ['Needs answer', 'Resolved']), field('Field key'), field('Options', 'multilineText'), field('Question type', 'singleSelect', ['Form', 'Narrative']), field('Sources', 'multilineText'), field('Answered on', 'date')], 'Question ID', 'Role-specific narrative questions and final answers; existing Form rows are preserved. Only nonempty Resolved final answers count for this application.')
    links = [
        ('Applications', 'Company', 'Companies', '0..1'),
        ('Audit log', 'Application', 'Applications', 'many'),
        ('Application questions', 'Application', 'Applications', '1')]
    result = {'version': 24, 'description': 'Seven-table logical blueprint; reactivate answer tables without deleting existing data; preserve other legacy fields/tables as read-only history, not raw connector request payloads. Map and preserve existing fields by ID; computed metadata never receives input values. DATA.md defines compact displays, manual feedback and view visibility.', 'tables': tables, 'links': [{'from_table': a, 'field': b, 'target_table': c, 'cardinality': d} for a,b,c,d in links]}
    inverse = {('Applications','Company'):'Applications',('Audit log','Application'):'Audit log',('Application questions','Application'):'Application questions'}
    for link in result['links']:
        link['inverse_field'] = inverse[(link['from_table'],link['field'])]
    from stage_state import CORE_FIELDS
    result['application_required_fields'] = CORE_FIELDS
    (ROOT/'contracts/core-schema.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
