# Data and recovery

This is the single operational reference for Airtable, evidence, history and stage handoff. Read the relevant section rather than loading every record or document into model context. contracts/core-schema.json is the machine-readable blueprint; contracts/field-aliases.json maps older installations. docs/MAINTENANCE.md covers field retirement and releases. The schema target and a live migration's completion are separate facts.

## Six tables and minimal fields

| Table | Purpose | Target columns, including reciprocal links |
|---|---|---:|
| Companies | Explicit targeting and confirmed company application restrictions | 15 |
| Applications | Candidate, review, resume and application state | 29 |
| Sources | Official catalog/region, reader and complete pagination checkpoint | 13 |
| Runs | Frozen inputs, execution progress, ownership and concise handoff | 20 |
| Settings | Private references, versions, controls and verification | 6 |
| History | Field-level changes, decisions, business events and failures | 13 |

Native record IDs and createdTime are available without duplicate metadata columns. Do not add a common six-column metadata bundle to every table. Preserve useful historical actor/timestamp information before retiring redundant columns. Primary display fields are not SQL uniqueness constraints. Validate business keys, links/cardinality and intended deltas in the writer.

Companies keeps Company, Company key, Search status, Notes, Max applications, Application window (days), Application window type, Rejection cooldown (days), Restriction scope, Apply blocked until, Application hold status, Restriction details / source, Restriction timezone, plus the Applications and Sources reciprocal links. Optional company research belongs in registered content, not mandatory tracking columns. Rejection event time and actual rule verification belong in History; Apply recomputes restrictions immediately before submission.

Sources keeps Source key as its primary field, Company, Official careers URL, Catalog URL, Region, Reader, Reader version, Latest coverage, Checkpoint (JSON), Last error, Last scanned at, Last run and Archived at. Source key is a stable board identity, not a job identity. During migration merge the former source_id into the existing primary field before retiring its duplicate. Reader identifies a reusable reviewed script/feed reader; its version and durable location must be recoverable. The checkpoint holds cursor/end proof, counts, manifest identity, reader/pagination details and pending source evidence. Archived at disables an intentionally retired source; do not resurrect it just because other archive helpers retire. Every active configured official board/region remains in scope.

Runs keeps Run key, Run type, Status, Owner, Instruction revision, Input versions (JSON), Scope (JSON), Checkpoint (JSON), Expected items, Completed items, Blocked items, Started at, Finished at and Agent notes, plus six reciprocal relationships: History, Sources and the four Application stage contexts. In checkpoints retain stages, pending checks, next action, handoff/ownership release, mode and report references. Keep frozen input versions immutable; progress updates do not rewrite old accepted input pins. scripts/stage_state.py:run_progress supports older separate columns during migration. Agent notes is the concise human-readable handoff, not another procedure source. An expired heartbeat/lease never proves another writer stopped.

Settings keeps Key, Value, Reference URL, Version, Verification and Notes. Command routing and required resources belong in Git, not a Required by column or copied procedure text. Versioned extracted goals/readiness and live controls remain data. Verify the current source revision before reuse. Old setup/migration entries may remain historical data but cannot override Git. Do not delete settings rows merely because a column audit found redundant fields.

History keeps Event key, Operation ID, Event type, Recorded at, Occurred at, Actor / channel, Table reference, Record reference, Field changes (JSON), Evidence URL, Notes, Application and Run. Use explicit event types such as Review accepted, Field change, Submission intent, Confirmation received, Write failed or Write uncertain. Older Operation/Phase/Entity key/read-scope/error fields need exact preservation before retirement, not deletion on sight. A reference to an affected record is not the History record's own native ID. Run-level scope replaces routine per-read rows; actual event times stay distinct from recording times.

## Efficient execution

Parse/enumerate, normalize identities, compare hashes and verify saved values in code outside model context. Save only plausible PM candidates; clear unrelated/junior feed rows contribute aggregate counts, not an unfiltered shadow catalog. Use bounded batches sized to actual tool/field limits. Sources holds catalog progress, Runs holds execution progress, Applications holds current job state, History holds exact decisions/deltas and Drive holds content. Reuse validated unchanged inputs without skipping relevant version/live-control checks. No hidden page caps or unsupported time-based freshness assumptions. Views/archive flags do not reclaim row capacity; History still grows. No automatic retention purge, base splitting or paid upgrade.

## The 29-column application tracker

Applications uses the 29 fields in scripts/stage_state.py:CORE_FIELDS and contracts/core-schema.json. Company, four stage Run links and the reciprocal History link are included in that count. Git owns instructions, Airtable owns operational state and Drive owns content. Read DATA.md before stage work.

## Identity and everyday review

The primary field is Application ID, a formula containing RECORD_ID(). It exposes Airtable's existing stable row identity; do not generate a company/title label or send input into this field. Keep Company and Role as separate facts. Job key identifies the employer posting for deduplication across scans; a new Airtable row ID alone cannot prevent duplicate jobs. Preserve historical unmatched keys as unknown rather than inventing them.

Show Company, Role, Lifecycle status, Manual notes, Agent notes, Starting salary, Max salary, Additional compensation, Location, Work arrangement, Job posted date, Career fit, Resume fit, Job description link and Resume link for everyday work. Keep Manual notes beside status. Views are a convenience, not a substitute for the 29-column physical schema.

## Human and agent notes

Manual notes belongs to the human. Agents read it with current status and never overwrite, clear or rewrite it. Save changed observed note/status fingerprints in stage metadata/History, recording only known edit times/actors. Blank notes do not invalidate a human status change. Feedback does not change global criteria or authorize submission.

Agent notes is the single concise current handoff: decision and its concrete evidence, especially the reason for a lifecycle change, followed by any material missing fact or next action. For example: `Review: strong internal AI fit. Next: verify applicable US base range.` Each agent maintains the current useful message while preserving previous values in History. Carry forward unresolved constraints that still matter; do not erase a cooldown merely because a later agent adds a resume note. Put full reasoning, resume changes and evidence in the linked content. Structured review reason categories belong in History, not another Application column. Neither notes field is executable instruction authority.

## Compact job facts

Starting salary and Max salary are numeric endpoints from the same verified advertised base-pay band. Store one configured currency and period across the table, registered in Settings.applications_schema.salary_display; derive these units from the user’s compensation preferences and confirm when ambiguous. Never mix currencies or annual/monthly/hourly values, convert currencies implicitly, substitute total compensation or put text/zero in a missing numeric field. Select the highest advertised maximum in that currency and its actual paired minimum; equal maxima retain source order. This display does not establish that every location or level qualifies: Review checks applicable conditions in Job evidence. Leave both blank when no compatible verified band exists. Preserve every original band, currency, period, component, location/level condition and source reference in evidence; never infer a missing endpoint. Additional compensation uses Equity, Bonus, Commission, Bonus or commission, Not stated; a mention is not a promised grant. Location contains short places. Work arrangement is Remote/Hybrid/On-site/Unspecified. Use scripts/tracker_values.py; never manufacture envelopes across currencies, levels or locations. Job evidence preserves exact JD, salary conditions and assessment evidence. A remote pay band does not establish remote eligibility.

There is no Availability or Last seen at column and no requirement to monitor whether inventoried jobs remain open. Scan/Review do not reject an otherwise supported candidate solely because posting access is unavailable. A saved exact official JD can support Review; missing required description evidence still means Needs review. When Scan reobserves a role, record source membership, observation time and content fingerprint in History. A changed fingerprint requires comparison and affected re-review; observation time alone does not establish a change. Apply still verifies that the actual form can accept submission and records an obstacle in Agent notes/History.

## Review and readiness

Role eligibility records full-JD PM function/seniority validation. Career fit and Resume fit remain independent ratings. Review must record explicit role eligibility and hard-career-requirement checks in its History snapshot before setting Queued; no Career gate column is needed. Current scores and routing follow stages/review.md. Queued alone is not approval: verify accepted checks, fixed rules and current goals/master/JD through review_ready. Ready alone is not verified PDF identity or submission authorization. An existing attempt requires reconciliation even after a manual status reset.

Sources remains the scanner's table of catalogs/regions/cursors; Applications has no Sources relationship. The official Job description link is the direct job link. Record all real source IDs, posting aliases and indexed captures in scan metadata so another harness can resume and audit coverage. Do not infer closure from absence or incomplete enumeration.

## Existing installations

Follow docs/MAINTENANCE.md before retiring fields. Reuse the existing Assessment summary field as Agent notes after consolidating its text with Blocker; preserve Decision category and all retired values in History. Rename the existing primary Application field to Application ID and convert it to formula RECORD_ID() through a supported tool or the Airtable UI. Rename is not formula conversion. Keep existing field/record/link identities.

Record kind retires after a one-time normalization: unreviewed legacy candidates use Inventoried; assessed unresolved candidates use Need review and actual evidence; preserve historical/submitted/terminal outcomes and unmatched identities. Never approve, drop or reset a role merely to remove its legacy marker. All new candidates require checked identity, one explicitly allowed company, Inventoried and eligibility Pending.

Retired columns may remain during cutover, but writers never use or recreate them. Stop affected work if required snapshot migration is missing; do not infer approval from status or silently discard facts. Current evidence/PDF identity, resume verification, unique attempt identity, four stage Run links and the true History relationship remain required. The same state supports one complete agent Run or separate manually initiated harness stages.

## Stage metadata and the 29-field tracker

Applications holds current job facts, status/manual notes, role eligibility, independent fit ratings, human/agent notes, the current PDF reference/hash/verification, attempt identity and four stage Run links. `scripts/stage_state.py` defines its 29-field allowlist and pure metadata readers/guards. It rejects writes to retired fields; do not recreate them to resume an old plan. Resolve live field IDs and aliases first. Every new candidate has a unique canonical Job key and one allowed Company. Preserve unmatched legacy history by native record identity rather than inventing employer IDs.

Duplicate prevention uses the company-scoped employer role ID or canonical job link, with exact identifiers recovered from source metadata. Distinct regional posting IDs are not automatically compared or merged. Migration rows missing both identities remain a documented one-time gap. Preserve actual application history; title similarity alone never proves a duplicate.

## Persistent metadata

Use the existing History `Field changes (JSON)` field for records with this bounded schema:

    {"schema":"nextmove.stage-state.v2","records":[{"record_id":"...","job_key":"...","stage_runs":{},"source":{},"review":{},"preparation":{},"submission":{},"feedback":{},"details":{}}]}

This is stage metadata in the audit table, not another current-job JSON field. Batch within actual field/tool limits; keep the full metadata snapshot per affected application so recovery does not require replaying an unbounded delta chain. Link each History row to its affected Applications and execution Run. Retain actor/channel, recorded time and actual event time when known. A successful metadata write must be read back before its Application handoff is accepted.

Read the application's History links and relevant Runs in bounded batches, parse outside model context, then use `resolve` and `stage_versions`. Do not concatenate all evidence into prompts. The newest complete snapshot for an application supersedes its earlier snapshot. Version 1 snapshots remain readable for recovery, but approvals require the explicit version 2 review checks; follow docs/MAINTENANCE.md. Unknown legacy information stays unknown. Current records must have a snapshot before retired fields are removed. A migration snapshot can preserve original context Run IDs even though its audit event belongs to the migration Run.

`stage_runs` identifies Scan run, Review run, Preparation run and Submission run. Each is a real Runs relationship on Applications, at most one current context per stage. One full invocation can use the same Run for all four; separate harness commands use their own Runs. Keep prior contexts/events in History. A historical source admission and a later semantic revalidation must retain their actual provenance; a Scan link is not proof that every catalog was complete.

Migration may create immutable context-only Runs instead of altering old execution metadata. These have type Migration, explicitly declare that no new job stage was executed, and preserve the original execution Run ID. Snapshot `original_execution_runs` retains those identities. Such a context can back a migrated acceptance only when the original per-job explicit acceptance and exact input identities were preserved and verified; migration itself never approves a job.

## Registered Drive destinations

Use Settings.resume_output for the Role specific child folder and Settings.content_output for the Audit trail child folder. Both values retain root_folder_id; verify their actual parent and privacy. RESUME-FILES.md owns placement and safe cleanup rules. Reuse existing folders and current file IDs; the master/goals/base retain their independently registered locations. Store run captures, reports and metadata in Audit trail, not the main folder or resume destination.

## Input versions and evidence

Runs `Input versions (JSON).stage_inputs` holds shared fixed inputs by stage: goals/master/policy/instruction versions as applicable. Per-job review metadata holds its exact `jd_hash`, explicit `decision`, current-description provenance and review time. Rare mixed/legacy contexts use explicit `version_overrides`; null means unknown, not permission to inherit a current value. Freeze accepted input identities. A changed input scope creates a new stage segment/snapshot identity; never rewrite the pins underlying older approvals.

Use `contracts/policy-versions.json` for decision-policy versions. A schema-only repository release retains existing policy versions; audit the deployment revision separately. Changed goals, master, decision rules, JD or PDF still requires the affected checks. A manually selected Queued or Ready status is not acceptance evidence.

Detailed source/assessment content lives in exact versioned Drive captures. `details` contains its file URL/ID, role selector and integrity reference. It preserves original salary/location conditions, employer posting aliases, full assessment evidence, resume change/claim notes and role-specific answers. A shared file URL without a role selector is insufficient. Never discard those facts because the display columns are shorter. Current job evidence remains directly accessible on Applications.

## Stage writes

Current Review metadata records assessment_method three_step_v1, exact JD/input versions, career and resume ratings/scores, total, outcome, criterion/qualification evidence and unresolved questions. Store numbers and duplicate_of in History, not extra tracker columns. Older approval metadata remains historical evidence, not current scored approval.

- Scan: save basic-semantic/source metadata and policy context, update Scan run, current job facts and Agent notes. Preserve outcomes/manual notes. Unknown identity stays in Runs; ambiguity in eligible scope can stay inventoried. `source` keeps real source-record memberships, requisition IDs, verified aliases, capture selectors, observation times and content fingerprints; do not derive employer identity from a title or a URL hash.
- Review: save the three-step assessment and exact source/input identities before changing status, fit ratings, Review run and Agent notes. Use scores and thresholds in contracts/policy-versions.json; missing decisive evidence means Need review. Current scored acceptance is required before Queued. A migration does not invent scores or overwrite old accepted input pins.
- Prepare: save grounded change notes, claims evidence, input references, editable source/base reuse, exact file hash and visual verification in the preparation result. Set Preparation run, Resume link, Resume version and Resume verified at only after verification. Preserve submitted files. Use `resume_ready` with the actual downloaded bytes and current inputs; hashes must not come from filenames.
- Apply: before Submit, persist/read back the distinct attempt intent with role, exact submitted PDF ID/version, answer/evidence references and context. Persist/read back Submission attempt key and Submission run on Applications. Only then may an authorized supported browser click Submit. Save the actual result/receipt or uncertainty in History/checkpoint; set current state accordingly. An existing attempt blocks blind retry even if a UI status was changed back to Ready. Never reconstruct submitted bytes later from a changed current resume.
- Track: preserve receipt/message identities, confirmation/outcome dates, actual occurrence time and recorded time in History. Keep current lifecycle and compact Confirmation reference on Applications. Applied on remains an actual date; precise rolling restrictions use known event times where required. Missing mail does not establish non-submission.

Keep history and stage state when current job/resume versions change. A job-specific answer belongs to that attempt/result; reusable candidate facts belong in the registered answer source. Resume requirements are not evidence of experience.

## Manual edits and migration compatibility

Manual notes is human-owned. On changed observed note/status, save the exact observation/fingerprint in `feedback` and a meaningful History event; do not clear or rewrite the note. The editor and actual edit time may be unknown. Never use that feedback as implicit submission authorization or an untested global scan exclusion.

Current writers use current fields only, even while retired fields remain physically present. Archived pre-migration write plans are incompatible and must be rebuilt against the live schema. Current operational gates and submission controls stay in Airtable; detailed source content stays in Drive. No chat/local file is sole memory. `Settings` stores the schema release and migration manifest reference; instructions stay in Git.

## Current notes and removed monitoring

Agent notes is the concise current handoff; preserve older notes and unresolved material issues in History. Manual notes remains human-owned. Keep structured categories/checks in review metadata, never infer them from prose. Source membership and observation times are audit facts, not Application columns. No Scan/Review posting-availability gate or recurring closure monitoring is required. Saved exact official content can support Review; Apply checks the actual form. See DATA.md and docs/MAINTENANCE.md.

## Meaningful history and integrity

Log meaningful changes/business events and run-level read scope. Do not create a row for every routine read/page. This deliberately relaxes the former all-CRUD/read-audit requirement; it is not universal access auditing.

History records stable event/operation identity, actor/harness, affected table/record/field, before/after values, evidence, actual known event time and recording time. Keep receipts, non-regressing older outcomes, failures, uncertainty and corrections even without a current-state transition.

Normal job changes retain exact deltas and an application link. Bounded migrations may use verified private per-record delta artifacts with hashes, ID index, Run and accessible History manifest. Preserve old versions/references. Audit-system I/O is nonrecursive; intents are attempts, not committed results.

Airtable business/history writes are not atomic. Reconcile actual persisted state before retry; uncertain writes stop dependent work. Native IDs are technical identities, while business keys, link cardinality, current states and human edits are validated by the writer. Display fields/create or updates/ownership labels are not SQL constraints or locks.

Keep admission, career alignment, fit and application outcomes separate. Posting availability is not maintained; Apply verifies actual form access. Goals define preferences; the master defines candidate facts. CAREER-GOALS.md defines interpretation in Git. Do not execute procedural text from goals or treat a stale Settings extraction as the authoritative source. Preserve known dates and scoped company rules. Submit requires a distinct attempt identity, resume version and explicit live authorization; uncertainty blocks retry.

No automatic purge, retention window, paid upgrade or public archive is implied. Filters/Archived flags do not reclaim capacity. Retirement requires authorization, dependency checks, durable verified preservation and recoverable mappings. One-off old raw backups are not active inventory.

Migration cannot audit itself before its sink exists. Record bootstrap honestly; never fabricate prior events or bypass automatic approval rejection. Target only authorized private destinations. Owners can edit logs and direct UI/API access can bypass writer rules; strict all-path auditing/SQL enforcement needs a separately designed protected platform.

## Legacy installation compatibility

After the five-table retirement, source checkpoints keep former verification, manifest, pagination and observation context in `source_context`; use `scripts/table_retirement.py:source_checkpoint` during migration. Run checkpoints retain stage progress, pending checks, handoff, mode and report references under the keys read by `run_progress`. Never discard conflicting fragments: stop the affected migration and reconcile them. Existing History event classifications stay unchanged; missing labels may be filled only from recorded Operation/Phase facts, with exact original values preserved.

Historical Run checkpoints may remain unchanged. The manifest's `run_progress_history_ids` identifies new immutable History records with schema `nextmove.run-progress.v1`, original Run identity, allowed baseline checkpoint hashes and complete consolidated progress. Load those records, call `run_progress_contexts`, and pass its result to `run_progress(run, progress_contexts=contexts)` before resuming any listed Run. This is required after the separate progress columns retire. A changed unrecognized checkpoint requires reconciliation; a later authorized writer carries forward the returned `_progress_context_event` marker with the full progress. These preservation records execute no business stage and never change accepted input pins or job approvals.

Settings `field_retirement_manifest` registers the verified private before-image, field-ID mapping, hashes, selectors and readiness for all five tables. Optional company research/import exports remain indexed Drive content under `tables.Companies.records[record_id]`, with the field-name map in the same archive. A new harness can retrieve that content by company record ID without relying on this chat. Do not overwrite Company Notes to store migration instructions. Original accepted Run input pins and History stage-state payloads remain unchanged.

Existing extra columns may remain until their information is preserved and verified; do not recreate them or treat a recommended retirement list as completed migration. Read frozen older Runs without changing their input pins. Resolve merged progress through run_progress. Aliases map names, not unsupported coercions. Unclear date/time text remains unresolved; computed fields never receive input. New installs use the minimal blueprint. Existing installs save exact field-ID mappings and a per-table migration manifest in Settings/History before any deletion. Include native reciprocal links in column counts; deleting them can remove the real relationship.

The lifecycle has nine states under WORKFLOW.md. Inventoried means awaiting first review; Need review means unresolved or middle-band assessment. Duplicate means Run has verified a redundant row with objective identity evidence and a canonical reference. Preserve original statuses, candidate/application history, source links and manual notes before migration. Existing queued approvals need new scored acceptance before advancing; old ratings cannot be silently reinterpreted. No availability monitoring or extra duplicate/score columns are introduced.

## Salary column migration

Preserve the exact Posted salary range values and all source conditions in a verified private per-record artifact before retirement. Create Starting salary and Max salary as Number fields; parse verified official bands with scripts/tracker_values.py:salary_endpoints. Reread live inputs, write only intended numeric values, audit before/after by native record ID and verify all rows and protected human/application state. Do not rerun Review or change decisions for a display-only migration. Register units, field IDs, evidence, blanks/reasons and retirement readiness in Settings.applications_schema and the migration Run. Retire Posted salary range only after preservation and readback; writers must not depend on it. If deletion is unsupported, give the exact remaining UI action.
