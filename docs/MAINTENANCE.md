# Maintenance and releases

For deliberate maintenance only, not stage startup. README.md maps the repository; WORKFLOW.md, DATA.md and stages/ own runtime rules. Git history keeps removed files; do not restore them.

## Retiring live columns or choices

The target is 120 columns: Companies 25, Applications 29, Sources 13, Runs 21, Settings 6, History 13, Review eval 13, including reciprocal links (contracts/core-schema.json). Before deleting a live column, preserve its values (with record IDs and field IDs) in Audit trail content, record the manifest in History, confirm no reader, formula, view or automation depends on it, then delete only the verified list and read back. Deleting a reciprocal link removes the relationship itself. Connectors that cannot delete fields or manage select choices get an exact UI step instead; deployment readiness stays incomplete until readback confirms it.

## Release checks

Run `python scripts/check_repo.py`, `python scripts/build_schema.py` (the committed schema must not change) and `python -m unittest discover -s tests -v`. Review links, command routes, private-data patterns and the actual diff. CI checks public contracts only, not a live scan, browser or account.

Privately verify schema, options and links, human notes and outcomes, goals/master/output access, source coverage, one writer, durable handoff, attempt recovery, rendered PDFs, mailbox scope and live controls. Record Passed, Blocked or Not tested with evidence. Never call a deployment ready while UI, data or access steps remain.
