# Changelog

## Current instruction release

- Six active tables, one Applications table for Inventoried candidates and the reviewed Queued list.
- Single-agent full runs by default; the same saved state and checks support manually switched stages.
- Career Goals contains preferences only. Scan derives broad role criteria; Review owns full eligibility, career/resume assessment and Queued approval.
- Review reasons support tested scanner improvements that protect recall. Career mismatches are not automatic scanner errors.
- Exact compensation interpretation, IC/manager preferences, evidence versions, truthful resume preparation and explicit submission controls.
- Clear resume filenames, retained versions and PDF verification; no blanket one-page requirement.
- Shared clarification rules, complete setup/user responsibilities, field aliases, release checks and meaningful change history.
- Schema version 4 adds scan/review feedback and resume file/version fields; CSV templates match the generated schema.

## Earlier designs

Previous revisions used a full raw job catalog and separate task, attempt, artifact and configuration tables. Those are legacy migration sources, not the current workflow. Earlier status meanings, scanner career filters, manual-only execution and routine per-read journal requirements have been superseded.

Existing installations require a verified migration. Publishing these instructions does not certify account readiness, delete legacy data, install a scheduler or authorize submissions. MIT licensing and private-data boundaries remain in force.
