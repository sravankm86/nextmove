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

    for name in ["README.md", "LICENSE", "SETUP.md", "ARCHITECTURE.md", "CONNECTORS.md", "COMMANDS.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "HARNESS-BOOTSTRAP.md", "docs/SETUP-CHECKLIST.md"]:
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
    tables = core["tables"] + state["tables"]
    names = [t["name"] for t in tables]
    require(len(core["tables"]) == 11 and len(state["tables"]) == 6 and len(set(names)) == 17, "Expected eleven core and six distinct execution tables")
    supported_primary = {"singleLineText", "multilineText", "number", "date", "dateTime", "url", "email"}
    lookup = {t["name"]: t for t in tables}
    for table in tables:
        fields = table["fields"]
        field_names = [f["name"] for f in fields]
        require(len(field_names) == len(set(field_names)), "Duplicate fields: " + table["name"])
        require(bool(fields) and fields[0]["type"] in supported_primary, "Unsupported primary creation field: " + table["name"])
        for f in fields:
            if f["type"] == "singleSelect":
                choices = [x["name"] for x in f.get("options", {}).get("choices", [])]
                require(bool(choices) and len(choices) == len(set(choices)), "Invalid enum: " + table["name"] + "." + f["name"])
    for link in core["links"] + state["links"]:
        require(link["from_table"] in lookup and link["target_table"] in lookup, "Unknown linked table: " + str(link))
        if link["from_table"] in lookup:
            require(link["field"] not in [f["name"] for f in lookup[link["from_table"]]["fields"]], "Link conflicts with scalar field: " + link["field"])
    resources = [x["key"] for x in seed["resources"]]
    require(len(resources) == len(set(resources)), "Duplicate setup resource key")
    require(set(command["state_tables"]) == {x["name"] for x in state["tables"]}, "Command/state table mismatch")
    aliases = []
    for cmd in command["commands"]:
        require((root / cmd["instructions"]).is_file(), "Missing stage instructions: " + cmd["command"])
        require(set(cmd["required_resources"]).issubset(resources), "Unseeded resource: " + cmd["command"])
        require(set(cmd.get("submission_resources", [])).issubset(resources), "Unseeded submission resource: " + cmd["command"])
        aliases += cmd["aliases"]
    require(len(aliases) == len(set(aliases)), "Ambiguous command alias")
    require(command.get("application_submission_default") is False, "Unsafe default submission policy")
    require(next(x for x in command["commands"] if x["command"] == "Apply")["mode"] == "review", "Apply must default to preflight/review")
    require(seed["submission_defaults"]["daily_submission_cap"] == 0 and seed["submission_defaults"]["enabled"] is False, "Unsafe setup submission defaults")
    controls = {x["control"]: x["value"] for x in seed["controls"]}
    require(controls.get("Pause applications") is True and controls.get("Stop all") is False, "Invalid fresh-install pause/stop defaults")
    require(seed["scan_defaults"]["description_policy"] == "all" and seed["scan_defaults"]["recovery_budget"] is None, "Fidelity defaults changed without contract update")
    require(seed["scan_defaults"]["inventory_storage_profile"] == "full-airtable", "Unexpected storage-profile default")
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
