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

Plausible PM candidates become Inventoried after basic semantics. Review owns full eligibility/career/resume acceptance before Queued. Needs eligibility and Shortlisted are legacy aliases only; preserve historical outcomes.

| Field | Type |
|---|---|
| Application | singleLineText |
| Job key | singleLineText |
| Company name | singleLineText |
| Role | singleLineText |
| Job description link | url |
| Lifecycle status | singleSelect: Needs eligibility, Inventoried, Not aligned, Queued, Shortlisted, Not a fit, Ready, Applied, Confirmed, In process, Offer, Accepted, Rejected, Withdrawn, Not pursuing, Closed, Needs review, Submission uncertain, Duplicate |
| Manual notes | multilineText |
| Record kind | singleSelect: Admitted role, Legacy revalidation, Application history |
| Scan evidence | multilineText |
| Scan policy version | singleLineText |
| Decision category | singleLineText |
| Decision reason | multilineText |
| Feedback versions (JSON) | multilineText |
| Role eligibility | singleSelect: Pending, Eligible, Excluded |
| Eligibility evidence | multilineText |
| Eligibility policy version | singleLineText |
| Career gate | singleSelect: Pending, Pass, Fail |
| Career evidence | multilineText |
| Career goals version | singleLineText |
| Description content (Drive) | url |
| Description status | singleSelect: Current, Captured, Historical, Missing, Unavailable |
| Availability | singleSelect: Open, Closed, Unknown |
| Posted salary range | singleLineText |
| Additional compensation | multipleSelects: Equity, Bonus, Commission, Bonus or commission, Not stated |
| Location | singleLineText |
| Work arrangement | singleSelect: Remote, Hybrid, On-site, Unspecified |
| Job posted date | date |
| First seen at | dateTime |
| Last seen at | dateTime |
| Career fit | singleSelect: High, Medium, Low, Unresolved |
| Resume fit | singleSelect: High, Medium, Low, Unresolved |
| Fit rationale - Career goals | multilineText |
| Fit rationale - Resume | multilineText |
| Resume link | url |
| Resume file name | singleLineText |
| Resume version | singleLineText |
| Resume verified at | dateTime |
| Resume notes | multilineText |
| Evidence versions (JSON) | multilineText |
| Submission attempt key | singleLineText |
| Submitted resume version | singleLineText |
| Confirmation reference | multilineText |
| Applied on | date |
| Confirmed on | date |
| Outcome on | date |
| Blocker | multilineText |
| Company | Link to Companies (0..1) |
| Sources | Link to Sources (many) |

Use [TRACKER.md](../TRACKER.md) for the 13-column everyday view, range-only salary formatting and human-owned Manual notes. Existing multiline salary/location or text work/status fields remain supported by ID; new installations use the compact types above. Do not force destructive field-type recreation.

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
- Record kind, migration notes, raw source records and old links are provenance, not new decision evidence. Do not delete them just to make a view smaller.
- Companies.Apply blocked until can be legacy text. Accept only a verified complete date/time with confirmed timezone; unclear text means held for clarification. Do not silently coerce or replace it.
- Existing URL fields stored as text can be read only after validating the exact URL. Existing Location/Work arrangement may be text or select; preserve detail, use only supported select options and record unmapped detail separately.
- Use exact permitted select names from the live schema. If a needed state/option cannot be written, stop that affected write and repair schema during authorized setup; never invent a similar status.
- Sources.Company must identify one allowed company. Applications may have one company and many Sources. History can link affected Applications and one Run. Verify links against existing records.
- System creation/modification fields and Record ID are computed. Event dates and recorded dates are separate. Unknown values stay blank with a reason.
- Evidence versions (JSON) contains the actual goals/master/JD/instruction/reader versions, review acceptance and PDF verification. Feedback versions (JSON) relates review reasons to the screen that produced the candidate. Store readable reasoning too.
- History records exact meaningful changes, actor, reason, event/recorded time and affected references. A native Record ID field in History may be a text reference to the affected row, not the computed ID of the History row; map by type and meaning, not label alone.

## Legacy retirement

Do not write new jobs to Job Inventory, Work Items, Task Attempts or Artifacts. Do not use Stage Config or Context Registry to override current Git/Settings. Copy useful references/state with exact verification before retirement. Preserve backups and replacement links; unresolved backup authorization blocks deletion. Extra legacy tables do not authorize bypassing a live migration pause.

See DATA-GOVERNANCE.md, LIFECYCLE.md, RESUME-FILES.md and SETUP.md.
