"""Dependency-free checks for public contracts/docs, not a live integration test."""
import csv
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

    for name in ["README.md", "LICENSE", "SETUP.md", "ARCHITECTURE.md", "CONNECTORS.md", "COMMANDS.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "HARNESS-BOOTSTRAP.md", "CAREER-GOALS.md", "CLARIFICATIONS.md", "RESUME-FILES.md", "docs/AIRTABLE-FIELDS.md", "docs/RELEASE-CHECKLIST.md", "templates/career-goals.md", "docs/SETUP-CHECKLIST.md"]:
        require((root / name).is_file(), "Missing required public file: " + name)

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
        if p.suffix == ".csv":
            rows = list(csv.reader(text.splitlines()))
            require(bool(rows) and len(rows[0]) == len(set(rows[0])) and all(rows[0]), "Invalid/duplicate CSV header: " + rel)
        if p.suffix == ".md":
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
        state = decoded["contracts/state-schema.json"]
        command = decoded["contracts/commands.json"]
        seed = decoded["contracts/setup-seed.json"]
    except KeyError as exc:
        errors.append("Missing/invalid contract: " + str(exc))
        return errors
    tables = core["tables"]
    names = [t["name"] for t in tables]
    expected = {"Companies", "Applications", "Sources", "Runs", "Settings", "History"}
    require(len(names) == 6 and set(names) == expected, "Expected exactly six active logical tables")
    require(state.get("deprecated") is True and not state.get("tables"), "Legacy execution schema must not add tables")
    lookup = {t["name"]:t for t in tables}
    for table in tables:
        fields = table["fields"]
        labels = [f["name"] for f in fields]
        require(len(labels) == len(set(labels)), "Duplicate fields: " + table["name"])
        for f in fields:
            if f["type"] == "singleSelect":
                choices = [c["name"] for c in f.get("options", {}).get("choices", [])]
                require(bool(choices) and len(choices) == len(set(choices)), "Invalid enum: " + f["name"])
    for table in tables:
        header = next(csv.reader((root / ('templates/' + table['name'].lower() + '.csv')).open()))
        require(header == [f['name'] for f in table['fields']], 'CSV/schema mismatch: ' + table['name'])
    aliases = decoded.get('contracts/field-aliases.json', {}).get('aliases', {})
    for table, mapping in aliases.items():
        require(table in lookup, 'Unknown alias table')
        if table in lookup:
            labels = {f['name'] for f in lookup[table]['fields']} | {l['field'] for l in core['links'] if l['from_table'] == table}
            require(set(mapping).issubset(labels), 'Unknown logical field in aliases: ' + table)
    for link in core["links"]:
        require(link["from_table"] in lookup and link["target_table"] in lookup, "Unknown linked table")
    resources = [x["key"] for x in seed["resources"]] + [x["key"] for x in seed["policies"]]
    require(len(resources) == len(set(resources)), "Duplicate Settings key")
    require(set(command["tables"]) == expected and command["default_command"] == "Run", "Wrong command/schema default")
    aliases = []
    for cmd in command["commands"]:
        require((root / cmd["instructions"]).is_file(), "Missing command path: " + cmd["command"])
        require(set(cmd["required_resources"]).issubset(resources), "Unseeded command resource")
        aliases += cmd["aliases"]
    require(len(aliases) == len(set(aliases)), "Ambiguous aliases")
    require(command["application_submission_default"] is False, "Unsafe submission default")
    require(next(c for c in command["commands"] if c["command"] == "Apply")["mode"] == "review", "Apply must default to preflight")
    controls = {x["key"]: x["value"] for x in seed["controls"]}
    require(controls["Pause applications"] is True and controls["Stop all"] is False, "Unsafe controls")
    policy = next(x["value"] for x in seed["policies"] if x["key"] == "role_policy")
    require(policy["recall_first"] is True and policy["title_only_admission"] is False and policy["career_screen_before_queue"] is True, "Missing recall/basic-semantic/queue safeguards")
    scan = next(c for c in command['commands'] if c['command'] == 'Scan')
    require('career_goals' in scan['required_resources'], 'Scan must resolve current goals-derived role criteria')
    require(policy.get('career_screen_stage') == 'Review' and policy.get('final_eligibility_stage') == 'Review' and policy.get('queue_owner') == 'Review', 'Review must own final acceptance')
    require(policy.get('inventory_gate') == 'keywords_and_basic_semantics', 'Wrong inventory boundary')
    feedback = policy.get('feedback', {})
    require(feedback.get('protect_eligible_recall') is True and feedback.get('career_rejections_are_scan_negatives') is False, 'Unsafe feedback learning')
    app_fields = {f['name'] for f in lookup['Applications']['fields']}
    require({'Scan evidence', 'Scan policy version', 'Decision category', 'Decision reason', 'Feedback versions (JSON)'}.issubset(app_fields), 'Missing disposition provenance')
    pref = seed.get('preference_contract', {})
    require(pref.get('instruction_authority') == 'GitHub' and pref.get('source_kind') == 'end_user_preferences', 'Wrong goals authority')
    require(pref.get('freeform_supported') is True and pref.get('embedded_commands_are_instructions') is False and pref.get('derived_values_require_source_version') is True, 'Unsafe preference interpretation')
    require(pref.get('uses') == ['scan_criteria', 'review_queue'] and pref.get('source_revision_check_required') is True and pref.get('stage_readiness_required') is True, 'Missing two-stage preference readiness')
    require(pref.get('explicit_unrestricted_distinct_from_unspecified') is True, 'Blank preferences must not mean unrestricted')
    for key in ['template', 'instructions']:
        require((root / pref.get(key, '__missing__')).is_file(), 'Missing preference contract file')
    history = next(x["value"] for x in seed["policies"] if x["key"] == "history_policy")
    require(history["meaningful_changes"] is True and history["per_read_rows"] is False, "Unexpected history policy")
    require(seed["submission_defaults"]["enabled"] is False and seed["submission_defaults"]["daily_submission_cap"] == 0, "Unsafe submission setup")
    require("MIT License" in (root / "LICENSE").read_text(), "Expected MIT license")
    return errors


if __name__ == "__main__":
    issues = check(ROOT)
    if issues:
        for issue in issues:
            print("ERROR:", issue, file=sys.stderr)
        raise SystemExit(1)
    print("Public contracts, schema links, defaults, documentation links and identifier checks passed.")
    print("Not a live provisioning, harness, history-wide privacy or universal audit test.")
