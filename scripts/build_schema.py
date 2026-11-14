"""Build the public fresh-install blueprint from the logical CSV templates.

This builds JSON only. It never authenticates, provisions services, or reads user data.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def field(name, kind="singleLineText", choices=None):
    value = {"name": name, "type": kind}
    if choices:
        value["options"] = {"choices": [{"name": choice} for choice in choices]}
    elif kind == "number":
        value["options"] = {"precision": 0}
    elif kind == "dateTime":
        value["options"] = {"dateFormat": {"name": "iso"}, "timeFormat": {"name": "24hour"}, "timeZone": "utc"}
    elif kind == "date":
        value["options"] = {"dateFormat": {"name": "iso"}}
    elif kind == "checkbox":
        value["options"] = {"icon": "check", "color": "greenBright"}
    return value


def header(name):
    with (ROOT / "templates" / name).open(newline="") as stream:
        return next(csv.reader(stream))


def main():
    lifecycle = ["Queued", "Shortlisted", "Not a fit", "Ready", "Applied", "Confirmed", "In process", "Offer", "Accepted", "Rejected", "Withdrawn", "Not pursuing", "Closed", "Needs review", "Submission uncertain", "Duplicate"]
    tables = []
    links = []

    def table(name, fields, key, purpose):
        tables.append({"name": name, "description": purpose, "business_key": key, "fields": fields})

    def link(source, name, target, cardinality="0..1"):
        links.append({"from_table": source, "field": name, "target_table": target, "cardinality": cardinality})

    company = [field("Company"), field("Company key"), field("Search status", "singleSelect", ["Allow", "Exclude"]), field("Pool"), field("Careers URL", "url"), field("Notes", "multilineText")]
    company += [field(x, "number") for x in ["Max applications", "Application window (days)", "Rejection cooldown (days)"]]
    company += [field("Application window type", "singleSelect", ["Rolling", "Calendar", "Fixed", "Unconfirmed"]), field("Restriction scope", "singleSelect", ["Company", "Role family", "Exact role", "Mixed", "Unconfirmed"]), field("Last rejection date", "date"), field("Apply blocked until", "dateTime"), field("Application hold status", "singleSelect", ["Not assessed", "No known hold", "Held", "Needs clarification"]), field("Restriction details / source", "multilineText"), field("Restriction last verified", "dateTime"), field("Restriction timezone")]
    table("Target Companies", company, "Company key", "One current company choice. Allow/Exclude and Pool belong to the user; no default Allow.")

    aliases = {"company": "Company name", "role": "Role", "requisition_id": "Requisition ID", "lifecycle_status": "Lifecycle status", "job_url": "Job description link", "resume_url": "Resume link", "resume_notes": "Resume notes", "posted_salary": "Posted salary range", "job_key": "Job key", "source_date": "Observed at", "date_found": "Date found", "job_posted_at": "Job posted date", "review_criteria_version": "Review criteria version", "review_master_version": "Review master version", "review_description_hash": "Review description hash", "resume_master_version": "Resume master version", "resume_claims_ref": "Resume claims reference", "next_owner": "Next owner"}
    url_fields = {"job_url", "resume_url", "source_url", "resume_claims_ref"}
    date_fields = {"applied_on", "confirmed_on", "outcome_on", "job_posted_at"}
    times = {"date_found", "source_date", "submitted_at", "status_recorded_at", "reviewed_at", "resume_verified_at", "fit_evaluated_at"}
    enums = {"lifecycle_status": lifecycle, "career_fit": ["High", "Medium", "Low", "Unresolved"], "resume_fit": ["High", "Medium", "Low", "Unresolved"], "work_arrangement": ["Remote", "Hybrid", "On-site", "Unspecified"], "resume_type": ["Base", "Tailored"], "next_owner": ["Reviewer", "Preparer", "Applier", "Tracker", "Human"]}
    app = [field("Application")]
    for name in header("applications.csv"):
        label = aliases.get(name, name.replace("_", " ").capitalize())
        kind = "url" if name in url_fields else "date" if name in date_fields else "dateTime" if name in times else "checkbox" if name == "review_pending" else "singleSelect" if name in enums else "multilineText"
        if name in {"company", "role", "job_key", "requisition_id", "run_id", "attempt_id"}:
            kind = "singleLineText"
        app.append(field(label, kind, enums.get(name)))
    app += [field("Fit rationale - Career goals", "multilineText"), field("Fit rationale - Resume", "multilineText"), field("Description content (Drive)", "url"), field("Imported lifecycle status"), field("Submission attempt key"), field("Submission recorded at", "dateTime")]
    table("Applications", app, "Record ID; scoped Job key for canonical role matching", "Current application lifecycle and fit/resume evidence. Preserve legacy fields during migration.")
    link("Applications", "Target company", "Target Companies")
    link("Applications", "Inventory job", "Job Inventory")

    inventory = []
    for name in header("job-inventory.csv"):
        label = "description_content_drive" if name == "description_or_private_ref" else name
        kind = "url" if name in {"job_url", "description_or_private_ref"} else "dateTime" if name in {"first_seen_at", "last_seen_at"} else "date" if name == "job_posted_at" else "multilineText"
        if name in {"job_key", "company_id", "source_id", "requisition_id", "source_posting_id", "run_id"}:
            kind = "singleLineText"
        inventory.append(field(label, kind))
    for name in ["Metadata hash", "Description hash", "Reader version", "Criteria version", "Filter version"]:
        inventory.append(field(name))
    inventory += [field("Description verified at", "dateTime"), field("Source memberships (JSON)", "multilineText"), field("Change version evidence (JSON)", "multilineText"), field("Field provenance (JSON)", "multilineText")]
    table("Job Inventory", inventory, "job_key", "Canonical posting metadata and capture references; default full inventory, with optional explicitly selected storage profiles.")
    link("Job Inventory", "Target company", "Target Companies")

    table("Catalog Sources", [field("Source record name"), field("source_id"), field("company_id"), field("company"), field("official_careers_url", "url"), field("catalog_url", "url"), field("reader"), field("region"), field("source_verification", "multilineText"), field("coverage_gap", "multilineText"), field("snapshot_at", "dateTime"), field("run_id"), field("Reader version"), field("Manifest version"), field("Pagination contract (JSON)", "multilineText"), field("Checkpoint (JSON)", "multilineText")], "source_id", "One current configured official board/region; preserve its change history in Audit Events.")
    link("Catalog Sources", "Target company", "Target Companies")

    table("Company Policies", [field("Policy"), field("Policy key"), field("Type", "singleSelect", ["Application limit", "Rejection cooldown", "Manual hold"]), field("Rule details", "multilineText"), field("Blocked until", "dateTime"), field("Evidence (Drive)", "url")], "Policy key", "Separate confirmed constraints where a company has multiple scopes/windows; do not invent a policy.")
    link("Company Policies", "Target company", "Target Companies")

    for name, template, primary in [("Runs", "runs.csv", "Run record"), ("Scan Audit", "scan-audit.csv", "Audit record"), ("Lifecycle Events", "lifecycle-events.csv", "Event"), ("Mail Audit", "mail-audit.csv", "Audit")]:
        fields = [field(primary)]
        for key in header(template):
            number = key in {"pages_read", "messages_read", "advertised_count", "observed_count", "description_failures", "matched_events", "unmatched_events", "ambiguous_events", "duplicate_events", "transitions_saved"}
            stamp = key.endswith("_at") or key in {"window_start", "window_end", "last_successful_checkpoint"}
            kind = "number" if number else "dateTime" if stamp else "checkbox" if key == "end_verified" else "multilineText"
            fields.append(field(key, kind))
        table(name, fields, "event_id" if name == "Lifecycle Events" else "run_id" if name == "Runs" else "Record ID; run/source/scope/attempt identity", "Domain evidence; not a replacement for the general CRUD journal.")
    link("Scan Audit", "Target company", "Target Companies")
    link("Lifecycle Events", "Application", "Applications")
    link("Mail Audit", "Stage run", "Stage Runs")

    audit = [field("Event key"), field("Operation ID"), field("Operation", "singleSelect", ["Create", "Read", "Update", "Archive", "Delete", "Schema", "Baseline", "Access review"]), field("Phase", "singleSelect", ["Intent", "Succeeded", "Failed", "Uncertain", "Baseline"]), field("Recorded at", "dateTime"), field("Occurred at", "dateTime")]
    audit += [field(name) for name in ["Actor / channel", "Table ID", "Record ID reference", "Entity key", "Run ID"]]
    audit += [field(name, "multilineText") for name in ["Field changes (JSON)", "Read scope (JSON)", "Reason / source", "Coverage / errors"]]
    audit.append(field("Evidence (Drive)", "url"))
    table("Audit Events", audit, "Event key", "Policy-based append-only operation journal; not immutable or a native all-path interceptor.")
    link("Audit Events", "Application", "Applications")
    table("Controls", [field("Control"), field("Value", "multilineText"), field("Notes", "multilineText")], "Control", "Private live configuration/stop controls; values must be parsed explicitly, never by truthiness of a string.")

    common = [field("Record ID", "formula"), field("System created at", "createdTime"), field("System updated at", "lastModifiedTime"), field("Created by", "createdBy"), field("Updated by", "lastModifiedBy"), field("Archived at", "dateTime")]
    common[0]["options"] = {"formula": "RECORD_ID()"}
    payload = {"version": 1, "description": "Logical fresh-install core blueprint, not a connector request body. Resolve live IDs and field options with the selected tools; preserve existing mappings and provenance.", "tables": tables, "links": links, "common_fields": common, "identity_note": "Audit Events uses Record ID reference for the affected row, while its own Record ID is computed. Existing deployments may map the affected-row field named Record ID as a legacy alias; do not change its meaning.", "creation_order": ["Create scalar tables with supported primary display fields", "Create orchestration tables from state-schema.json", "Resolve all returned table IDs", "Create links with resolved IDs and validate inverse fields", "Add common/computed metadata with field-creation tools where table creation does not support it", "Map logical names, seed private context/controls, and verify readback"]}
    (ROOT / "contracts" / "core-schema.json").write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
