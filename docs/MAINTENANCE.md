# Maintenance and releases

For deliberate maintenance only, not stage startup. README.md maps the repository; WORKFLOW.md, DATA.md and stages/ own runtime rules. Git history keeps removed files; do not restore them.

## Retiring live columns or choices

The active new-install target is 100 fields: Companies 10, Applications 25, Sources 13, Runs 20, Settings 6, History 13 and Review eval 13, including reciprocal links (contracts/core-schema.json). Existing retired-stage tables, fields, status choices and controls remain inactive history; reducing scope does not authorize deleting them. Before deleting a live column, preserve its values (with record IDs and field IDs) in Audit trail content, record the manifest in History, confirm no reader, formula, view or automation depends on it, then delete only the verified list and read back. Deleting a reciprocal link removes the relationship itself. Connectors that cannot delete fields or manage select choices get an exact UI step instead; deployment readiness stays incomplete until readback confirms it.

## Release checks

Run `python scripts/check_repo.py`, `python scripts/build_schema.py` (the committed schema must not change) and `python -m unittest discover -s tests -v`. Review links, command routes, private-data patterns and the actual diff. CI checks public contracts only, not a live scan or account.

Privately verify schema, options and links, human notes and outcomes, goals/master/output access, source coverage, one writer, durable handoff, protected historical outcomes, rendered PDFs and Stop all. Record Passed, Blocked or Not tested with evidence. Never call a deployment ready while UI, data or access steps remain.
