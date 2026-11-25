"""Dependency-free checks for public contracts/docs, not a live integration test."""
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PATTERNS = {
    "private service record/base identifier": re.compile(r"\b(?:app|tbl|fld|rec|wsp)(?=[A-Za-z0-9]{0,13}[A-Z0-9])[A-Za-z0-9]{14}\b"),
    "private Google content reference": re.compile(r"https://(?:docs\.google\.com/(?:document|spreadsheets|presentation)/d/|drive\.google\.com/(?:file/d/|drive/folders/))[A-Za-z0-9_-]{15,}"),
    "credential-like value": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{24,}|sk-[A-Za-z0-9_-]{24,}|pat_[A-Za-z0-9]{24,})\b"),
}


def public_issues(text):
    return [name for name, pattern in PRIVATE_PATTERNS.items() if pattern.search(text)]


def files(root):
    return sorted(p for p in root.rglob("*") if p.is_file() and not any(x in {".git", "__pycache__", ".venv"} for x in p.relative_to(root).parts))


def check(root):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    for name in ["README.md", "LICENSE", "AGENTS.md", "WORKFLOW.md", "SETUP.md", "DATA.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "CAREER-GOALS.md", "RESUME-FILES.md", "docs/MAINTENANCE.md", "templates/career-goals.md"]:
        require((root / name).is_file(), "Missing required public file: " + name)

    runtime = ['AGENTS.md','WORKFLOW.md','SETUP.md','DATA.md','CAREER-GOALS.md','RESUME-FILES.md'] + ['stages/'+x+'.md' for x in ['curate','scan','review','prepare','submit']]
    require(len(runtime)==11 and all((root/p).is_file() for p in runtime), 'Expected eleven canonical operational instruction files')

    decoded = {}
    for p in files(root):
        rel = str(p.relative_to(root))
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append("Non-text/unreadable public artifact: " + rel)
            continue
        require(text.endswith("\n"), "Missing final newline: " + rel)
        for issue in public_issues(text):
            errors.append(rel + ": " + issue + " (value withheld)")
        if p.suffix == ".json":
            try:
                decoded[rel] = json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(rel + ": invalid JSON at line " + str(exc.lineno))
        if rel == ".github/workflows/validate.yml":
            root_keys = set(re.findall(r"(?m)^([A-Za-z_+][A-Za-z0-9_+ -]*):", text))
            allowed = {"name", "on", "permissions", "concurrency", "jobs", "env", "defaults", "run-name"}
            require({"name", "on", "jobs"}.issubset(root_keys) and root_keys.issubset(allowed), "Invalid GitHub workflow root keys")
        if p.suffix == ".md":
            for script, symbol in ([] if rel == 'CHANGELOG.md' else re.findall(r'\b(scripts/[A-Za-z0-9_./-]+\.py):([A-Za-z_]\w*)', text)):
                target = root / script
                if not target.is_file():
                    errors.append(rel + ': missing documented helper: ' + script)
                    continue
                module = ast.parse(target.read_text())
                symbols = {node.name for node in module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
                symbols |= {name.id for node in module.body if isinstance(node, ast.Assign)
                            for name in node.targets if isinstance(name, ast.Name)}
                require(symbol in symbols, rel + ': missing documented symbol: ' + script + ':' + symbol)
            # Fenced examples may deliberately contain placeholder paths.
            plain = re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*$", "", text)
            for dest in re.findall(r"\[[^\]\n]*\]\(([^)]+)\)", plain):
                dest = dest.strip().split(' "', 1)[0].strip("<>")
                if not dest or dest.startswith("#") or urlsplit(dest).scheme:
                    continue
                path = unquote(dest.split("#", 1)[0])
                target = (p.parent / path).resolve()
                require(target.is_relative_to(root.resolve()) and target.exists(), rel + ": broken/outside local link: " + path)

    try:
        core = decoded["contracts/core-schema.json"]
        command = decoded["contracts/commands.json"]
        seed = decoded["contracts/setup-seed.json"]
    except KeyError as exc:
        errors.append("Missing/invalid contract: " + str(exc))
        return errors
    tables = core["tables"]
    names = [t["name"] for t in tables]
    expected = {"Companies", "Applications", "Settings", "Audit log", "Review eval", "Answer bank", "Application questions"}
    require(len(names) == 7 and set(names) == expected, "Expected exactly seven active logical tables")
    lookup = {t["name"]:t for t in tables}
    for table in tables:
        fields = table["fields"]
        labels = [f["name"] for f in fields]
        require(len(labels) == len(set(labels)), "Duplicate fields: " + table["name"])
        for f in fields:
            if f["type"] == "singleSelect":
                choices = [c["name"] for c in f.get("options", {}).get("choices", [])]
                require(bool(choices) and len(choices) == len(set(choices)), "Invalid enum: " + f["name"])
    for link in core["links"]:
        require(link["from_table"] in lookup and link["target_table"] in lookup, "Unknown linked table")
    from lifecycle import STATUSES
    lifecycle = next(f for f in lookup['Applications']['fields'] if f['name']=='Lifecycle status')
    require([c['name'] for c in lifecycle['options']['choices']] == STATUSES and len(STATUSES)==9 and STATUSES[-3]=='Applied', 'Expected nine lifecycle states including Submit\'s Applied')
    counts = {}
    for table in tables:
        fields = {f['name'] for f in table['fields']}
        fields |= {l['field'] for l in core['links'] if l['from_table']==table['name']}
        fields |= {l['inverse_field'] for l in core['links'] if l['target_table']==table['name'] and l.get('inverse_field')}
        counts[table['name']] = len(fields)
    require(counts=={'Companies':12,'Applications':24,'Settings':6,'Audit log':10,'Review eval':13,'Answer bank':5,'Application questions':11}, 'Unexpected minimal table profile')
    from company_policy import SEARCH_STATUSES
    companies = {f['name']: f for f in lookup['Companies']['fields']}
    require(not {'Origin', 'Company fit', 'Latest funding', 'Funding date'} & companies.keys(),
            'Retired company columns must stay outside the active schema')
    require([c['name'] for c in companies['Search status']['options']['choices']] == SEARCH_STATUSES and 'Proposed' in SEARCH_STATUSES, 'Companies Search status must offer Proposed/Allow/Exclude')
    pipeline = ['Curate', 'Scan', 'Review', 'Prepare']
    require(command['pipeline'] == pipeline and next(x['value'] for x in seed['policies'] if x['key'] == 'execution_policy')['pipeline'] == pipeline, 'Command and setup pipelines must agree across every stage')
    require(decoded['contracts/policy-versions.json']['schema_version'] == core['version'], 'Policy manifest must match the schema release')
    resources = [x["key"] for x in seed["resources"]] + [x["key"] for x in seed["policies"]]
    require(len(resources) == len(set(resources)), "Duplicate Settings key")
    require(set(command["tables"]) == expected and command["default_command"] == "Run", "Wrong command/schema default")
    aliases = []
    for cmd in command["commands"]:
        require((root / cmd["instructions"]).is_file(), "Missing command path: " + cmd["command"])
        require(set(cmd["required_resources"]).issubset(resources), "Unseeded command resource")
        aliases += cmd["aliases"]
    require(len(aliases) == len(set(aliases)), "Ambiguous aliases")
    require(command.get('endpoint') == 'Ready', 'Run must end at Ready')
    sanitize = next((c for c in command['commands'] if c['command'] == 'Sanitize'), {})
    require(sanitize.get('explicit_only') is True and sanitize.get('included_in_run') is False
            and 'Sanitize' not in command['pipeline']
            and command.get('run_preflight', {}).get('excluded_commands') == ['Sanitize'],
            'Sanitize must be explicit-only, outside Run and exempt from production preflight')
    require(sanitize.get('instructions') == 'docs/MAINTENANCE.md'
            and sanitize.get('required_resources') == ['instructions_repository'],
            'Sanitize must reuse maintenance and allow repo-only work without private accounts')
    require(not {'Apply', 'Track'} & {c['command'] for c in command['commands']}, 'Removed commands cannot dispatch')
    removed = ['stages/apply.md','stages/track.md','scripts/submission_policy.py']
    require(all(not (root/p).exists() for p in removed), 'Retired tasks must stay absent')
    require(not {'mailbox','narrative_context'} & set(resources), 'Retired resources cannot be setup dependencies')
    submit = next((c for c in command['commands'] if c['command'] == 'Submit'), {})
    require(submit.get('explicit_only') is True and submit.get('included_in_run') is False and 'Submit' not in command['pipeline']
            and submit.get('instructions') == 'stages/submit.md', 'Submit must be explicit-only and outside Run')
    sub_policy = next((x['value'] for x in seed['policies'] if x['key'] == 'submission_policy'), {})
    require(sub_policy.get('enabled') is False, 'Submission must ship disabled')
    eval_cmd = next((c for c in command["commands"] if c["command"] == "Review eval"), {})
    capture_cmd = next((c for c in command["commands"] if c["command"] == "Capture feedback"), {})
    require(eval_cmd.get("instructions") == "DATA.md" and capture_cmd.get("instructions") == "DATA.md", "Feedback and eval need shared instructions")
    require(all("eval_registry" in c.get("required_resources", []) for c in (eval_cmd, capture_cmd)), "Feedback/eval commands need the private registry")
    from resume_guidelines import load_schema, render_markdown
    frame = load_schema()
    ids = [x['id'] for x in frame['sections']]
    require(len(ids) == len(set(ids)) and all(len({f['id'] for f in x['fields']}) == len(x['fields']) and x['fields'][-1]['id'] == 'instructions' for x in frame['sections']), 'Resume guidelines frame needs unique IDs and an Instructions field per section')
    require((root / 'templates/resume-guidelines.md').read_text() == render_markdown(schema=frame), 'templates/resume-guidelines.md is stale; run python scripts/resume_guidelines.py template')
    prepare = next(c for c in command["commands"] if c["command"] == "Prepare")
    require({"master_resume", "resume_guidelines", "base_resumes", "answer_bank"}.issubset(prepare["required_resources"]), "Prepare must resolve the master, resume guidelines and base library")
    controls = {x['key']: x['value'] for x in seed['controls']}
    require(controls.get('Stop all') is False and controls.get('Setup readiness') == 'Needs verification', 'Unsafe or unverified setup controls')
    policy = next(x["value"] for x in seed["policies"] if x["key"] == "role_policy")
    require(not policy.get('resume_fit_exclusions_source') and policy.get('candidate_evidence_source'), 'Candidate evidence must not be sourced from Career Goals')
    require(policy["recall_first"] is True and policy["title_only_admission"] is False and policy["career_screen_before_queue"] is True, "Missing recall/basic-semantic/queue safeguards")
    scan = next(c for c in command['commands'] if c['command'] == 'Scan')
    require('career_goals' in scan['required_resources'], 'Scan must resolve current goals-derived role criteria')
    require(policy.get('career_screen_stage') == 'Review' and policy.get('final_eligibility_stage') == 'Review' and policy.get('queue_owner') == 'Review', 'Review must own agent queue admission')
    require(policy.get('inventory_gate') == 'keywords_and_basic_semantics', 'Wrong inventory boundary')
    feedback = policy.get('feedback', {})
    require(feedback.get('protect_eligible_recall') is True and feedback.get('career_rejections_are_scan_negatives') is False, 'Unsafe feedback learning')
    app_fields = {f['name'] for f in lookup['Applications']['fields']}
    require('Role eligibility' not in app_fields, 'Queued authorizes preparation without a duplicate eligibility flag')
    from stage_state import CORE_FIELDS
    require('Feedback' in companies and {'Manual notes','Feedback'}.issubset(app_fields), 'Separate lasting notes and Feedback are required')
    linked = {l['field'] for l in core['links'] if l['from_table'] == 'Applications'} | {l['inverse_field'] for l in core['links'] if l['target_table'] == 'Applications' and l.get('inverse_field')}
    require(app_fields | linked == set(CORE_FIELDS) and len(CORE_FIELDS) == 24, 'Expected the 24-field Application profile')
    primary = lookup['Applications']['fields'][0]
    require(primary['name'] == 'Application ID' and primary['type'] == 'formula' and primary.get('options', {}).get('formula') == 'RECORD_ID()', 'Application ID must expose native record identity')
    require((root/'DATA.md').is_file() and (root/'contracts/policy-versions.json').is_file(), 'Missing durable stage-state/version contract')
    pref = seed.get('preference_contract', {})
    require(pref.get('instruction_authority') == 'GitHub' and pref.get('source_kind') == 'end_user_preferences', 'Wrong goals authority')
    require(pref.get('freeform_supported') is True and pref.get('embedded_commands_are_instructions') is False and pref.get('derived_values_require_source_version') is True, 'Unsafe preference interpretation')
    require(pref.get('uses') == ['scan_criteria', 'review_queue', 'company_curation'] and pref.get('source_revision_check_required') is True and pref.get('stage_readiness_required') is True, 'Missing Curate/Scan/Review preference readiness')
    require(pref.get('explicit_unrestricted_distinct_from_unspecified') is True, 'Blank preferences must not mean unrestricted')
    for key in ['template', 'instructions']:
        require((root / pref.get(key, '__missing__')).is_file(), 'Missing preference contract file')
    company = next(x["value"] for x in seed["policies"] if x["key"] == "company_policy")
    discovery = company["discovery"]
    require(discovery["admission"] == "Proposed" and discovery["auto_allow"] is False, "Discovered companies must stay Proposed")
    history = next(x["value"] for x in seed["policies"] if x["key"] == "history_policy")
    require(history["meaningful_changes"] is True and history["per_read_rows"] is False, "Unexpected history policy")
    require("MIT License" in (root / "LICENSE").read_text(), "Expected MIT license")
    errors.extend(personal_content_issues(root))
    return errors


PUBLIC_DOCS = ['AGENTS.md', 'WORKFLOW.md', 'DATA.md', 'README.md', 'SETUP.md', 'CAREER-GOALS.md', 'RESUME-FILES.md', 'CLAUDE.md']
ROLE_WORDS = re.compile(r'(?i:product[- ]manag)|\bPMs?\b|\bSeries [A-D]\+')
PRIVATE_IDS = [(re.compile(r'\bapp[A-Za-z0-9]{14}\b'), 'Airtable base ID'),
               (re.compile(r'(?:drive|docs)\.google\.com/(?:file/d|drive/folders|document/d|spreadsheets/d)/[A-Za-z0-9_-]{20,}'), 'Google Drive file link'),
               (re.compile(r'[A-Za-z0-9._%+-]+@(?!example\.|anthropic\.com|users\.noreply)[A-Za-z0-9.-]+\.[a-z]{2,}'), 'email address')]


def personal_content_issues(root):
    """The public repository must work for anyone: no user's role family, preferences or private IDs."""
    found = []
    texts = {path: (root / path).read_text(encoding='utf-8') for path in PUBLIC_DOCS if (root / path).is_file()}
    texts.update({str(p.relative_to(root)): p.read_text(encoding='utf-8') for p in sorted((root / 'stages').glob('*.md'))})
    texts.update({str(p.relative_to(root)): p.read_text(encoding='utf-8') for p in sorted((root / 'scripts').glob('*.py')) if p.name != 'check_repo.py'})
    for path, text in texts.items():
        if ROLE_WORDS.search(text):
            found.append('%s names a specific role family or funding minimum; keep it in private Settings' % path)
    for p in sorted(root.rglob('*')):
        if not p.is_file() or '.git' in p.parts or p.suffix not in {'.md', '.py', '.json', '.yml', '.yaml', '.txt'} or p.name == 'check_repo.py':
            continue
        text = p.read_text(encoding='utf-8', errors='ignore')
        for pattern, label in PRIVATE_IDS:
            if pattern.search(text):
                found.append('%s contains a private %s' % (p.relative_to(root), label))
    sys.path.insert(0, str(root / 'scripts'))
    import company_policy, inspect
    if inspect.signature(company_policy.funding_qualifies).parameters['minimum'].default is not inspect.Parameter.empty:
        found.append('funding_qualifies must not default a funding minimum')
    seed = json.loads((root / 'contracts/setup-seed.json').read_text())
    pol = {x['key']: x['value'] for x in seed['policies']}
    if pol.get('role_family') is not None or pol['role_policy'].get('role_family') is not None:
        found.append('Seeded role family must be empty; each user defines Settings role_family')
    if pol['company_policy']['discovery'].get('min_funding_stage') is not None:
        found.append('Seeded funding minimum must be empty')
    if (pol.get('preparation_notes') or {}).get('shortlist_estimate') is not False:
        found.append('Seeded shortlist estimate must default to off')
    return found


if __name__ == "__main__":
    issues = check(ROOT)
    if issues:
        for issue in issues:
            print("ERROR:", issue, file=sys.stderr)
        raise SystemExit(1)
    print("Public contracts, schema links, defaults, documentation links and identifier checks passed.")
    print("Not a live provisioning, harness, history-wide privacy or universal audit test.")
