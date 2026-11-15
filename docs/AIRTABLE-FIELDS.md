# Airtable field guide

The active workflow uses six tables. An older base may also contain legacy tables. Their presence is not proof of completed migration. Read contracts/core-schema.json and contracts/field-aliases.json, discover actual field IDs/types, and save the mapping privately in Settings before work.

Inventory and the approved queue are states in Applications. Do not copy a candidate into another tracker when Review approves it. Job key is the business identity; Airtable record ID is the storage identity. Verify uniqueness before create/update. Keep historical records lacking a trustworthy key separate rather than guessing a match.

## Active fields

### Companies

Explicit company choices and confirmed simple quota/cooldown rules. Complex unclear rules block submission; no automatic Allow.

| Field | Type |
|---|---|
| Company | singleLineText |
| Company key | singleLineText |
| Search status | singleSelect: Allow, Exclude |
| Pool | singleLineText |
| Notes | multilineText |
| Max applications | number |
| Application window (days) | number |
| Application window type | singleLineText |
| Rejection cooldown (days) | number |
| Restriction scope | singleLineText |
| Apply blocked until | dateTime |
| Application hold status | singleSelect: Not assessed, No known hold, Held, Needs clarification |
| Restriction details / source | multilineText |
| Last rejection date | date |
| Restriction last verified | date |
| Restriction timezone | singleLineText |

### Applications

28 physical fields including five outward relationships and the History reciprocal link. Application ID is the primary formula RECORD_ID(); do not write values into it. Current handoff text belongs in Agent notes. Explicit review checks, structured feedback and source provenance live in History under STAGE-STATE.md.

| Field | Type |
|---|---|
| Application ID | formula: RECORD_ID() |
| Role | singleLineText |
| Job key | singleLineText |
| Job description link | url |
| Lifecycle status | singleSelect: Needs eligibility, Inventoried, Not aligned, Queued, Shortlisted, Not a fit, Ready, Applied, Confirmed, In process, Offer, Accepted, Rejected, Withdrawn, Not pursuing, Closed, Needs review, Submission uncertain, Duplicate |
| Manual notes | multilineText |
| Posted salary range | singleLineText |
| Additional compensation | multipleSelects: Equity, Bonus, Commission, Bonus or commission, Not stated |
| Location | singleLineText |
| Work arrangement | singleSelect: Remote, Hybrid, On-site, Unspecified |
| Job posted date | date |
| Role eligibility | singleSelect: Pending, Eligible, Excluded |
| Career fit | singleSelect: High, Medium, Low, Unresolved |
| Resume fit | singleSelect: High, Medium, Low, Unresolved |
| Agent notes | multilineText |
| Job evidence | url |
| Resume link | url |
| Resume version | singleLineText |
| Resume verified at | dateTime |
| Submission attempt key | singleLineText |
| Applied on | date |
| Confirmation reference | multilineText |
| Company | Link to Companies (0..1) |
| Scan run | Link to Runs (0..1) |
| Review run | Link to Runs (0..1) |
| Preparation run | Link to Runs (0..1) |
| Submission run | Link to Runs (0..1) |
| History | Reciprocal link of History.Application |

Follow [STAGE-STATE.md](../STAGE-STATE.md) for complete metadata and [the migration guide](TRACKER-MIGRATION.md) before retirement. Reuse Assessment summary as Agent notes after consolidation; convert the existing primary field rather than creating another ID column. Existing extra fields may remain during cutover; current writers ignore them.

### Sources

One official board/region. Enumerate all pages transiently; preserve coverage and minimal source/identity checks; plausible role/scope ambiguities are inventoried for Review.

| Field | Type |
|---|---|
| Source | singleLineText |
| Source key | singleLineText |
| Official careers URL | url |
| Catalog URL | url |
| Region | singleLineText |
| Reader reference | url |
| Reader version | singleLineText |
| Latest coverage | singleSelect: Complete, Partial, Failed, Unverified |
| Checkpoint (JSON) | multilineText |
| Last error | multilineText |
| Last scanned at | dateTime |
| Company | Link to Companies (1) |
| Last run | Link to Runs (0..1) |

### Runs

One row per full run by default; manual stage invocations use the identical checkpoint/handoff shape. No per-job work-item or general attempt tables.

| Field | Type |
|---|---|
| Run key | singleLineText |
| Run type | singleSelect: Full run, Scan, Review, Prepare, Apply, Track, Migration, Experiment |
| Status | singleSelect: Pending, Running, Complete, Partial, Blocked, Failed, Interrupted, Cancelled, No work |
| Mode | singleSelect: review, prepare, auto-apply |
| Owner | singleLineText |
| Instruction revision | singleLineText |
| Input versions (JSON) | multilineText |
| Scope (JSON) | multilineText |
| Stages (JSON) | multilineText |
| Checkpoint (JSON) | multilineText |
| Pending checks (JSON) | multilineText |
| Expected items | number |
| Completed items | number |
| Blocked items | number |
| Started at | dateTime |
| Finished at | dateTime |
| Handoff (JSON) | multilineText |
| Backup/report URL | url |
| Blockers | multilineText |

### Settings

Private resource references, criteria, scope and live controls. Instructions/command routes stay in Git.

| Field | Type |
|---|---|
| Key | singleLineText |
| Value | multilineText |
| Reference URL | url |
| Version | singleLineText |
| Verification | singleSelect: Located, Verified, Missing, Needs verification, Inaccessible |
| Required by | singleLineText |
| Notes | multilineText |

### History

Meaningful mutations and business events; failed/uncertain operations retain evidence. No routine per-read/per-row access logging. Not a universal immutable audit system.

| Field | Type |
|---|---|
| Event key | singleLineText |
| Operation ID | singleLineText |
| Event type | singleLineText |
| Recorded at | dateTime |
| Occurred at | dateTime |
| Actor / channel | singleLineText |
| Table reference | singleLineText |
| Record reference | singleLineText |
| Field changes (JSON) | multilineText |
| Evidence URL | url |
| Notes | multilineText |
| Application | Link to Applications (many) |
| Run | Link to Runs (0..1) |

## Existing data and safe mappings

- Legacy lifecycle status preserves old values. Only Lifecycle status drives current work. Old Queued/Shortlisted rows need current evidence before Queued approval; preserve submitted/terminal outcomes.
- Needs eligibility and Shortlisted remain accepted legacy values for reading/migration; new stages do not emit them.
- Record kind retires after operational-state normalization and exact provenance preservation under TRACKER-MIGRATION.md. Keep historical outcomes and unmatched identities; do not blanket-delete or certify legacy roles.
- Companies.Apply blocked until can be legacy text. Accept only a verified complete date/time with confirmed timezone; unclear text means held for clarification. Do not silently coerce or replace it.
- Existing URL fields stored as text can be read only after validating the exact URL. Existing Location/Work arrangement may be text or select; preserve detail, use only supported select options and record unmapped detail separately.
- Use exact permitted select names from the live schema. If a needed state/option cannot be written, stop that affected write and repair schema during authorized setup; never invent a similar status.
- Sources.Company must identify one allowed company. Applications may have one company; source memberships are recorded in History rather than an Application relationship. History can link affected Applications and one Run. Verify links against existing records.
- System creation/modification fields and Record ID are computed. Event dates and recorded dates are separate. Unknown values stay blank with a reason.
- Stage state snapshots in History and fixed stage inputs on Runs preserve exact versions, decisions, feedback and verification. Four typed context links replace the retired per-Application version fields. Source details remain in indexed Drive evidence.
- History records exact meaningful changes, actor, reason, event/recorded time and affected references. A native Record ID field in History may be a text reference to the affected row, not the computed ID of the History row; map by type and meaning, not label alone.

## Legacy retirement

Do not write new jobs to Job Inventory, Work Items, Task Attempts or Artifacts. Do not use Stage Config or Context Registry to override current Git/Settings. Copy useful references/state with exact verification before retirement. Preserve backups and replacement links; unresolved backup authorization blocks deletion. Extra legacy tables do not authorize bypassing a live migration pause.

See DATA-GOVERNANCE.md, LIFECYCLE.md, RESUME-FILES.md and SETUP.md.
