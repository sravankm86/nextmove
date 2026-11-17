# Data and recovery

The single reference for Airtable, evidence, history and stage handoff. contracts/core-schema.json is the machine-readable blueprint. Read only the section you need; keep bulk records and verification out of model context.

## Six tables

| Table | Purpose | Columns, including reciprocal links |
|---|---|---:|
| Companies | Curate-owned targeting, company fit, funding, employer policies and holds | 25 |
| Applications | Candidate, review, resume and application state | 29 |
| Sources | Official catalog/region, reader and pagination checkpoint | 13 |
| Runs | Frozen inputs, progress, ownership and handoff | 21 |
| Settings | Private references, policies, controls and verification | 6 |
| History | Field-level changes, decisions, business events and failures | 13 |

Native record IDs and createdTime replace metadata columns. Primary display fields are not uniqueness constraints: writers validate business keys, link cardinality and intended deltas. Columns outside this blueprint are not written; docs/MAINTENANCE.md covers retiring them.

**Companies.** Company, Company key, Search status, Manual notes, Agent notes, Origin, Company fit, Funding stage, Latest funding, Funding date, Company evidence, Policy confidence, Policy verified at, Max applications, Application window (days), Application window type, Rejection cooldown (days), Restriction scope, Apply blocked until, Application hold status, Restriction details / source, Restriction timezone, plus Applications, Sources and Curate run links. stages/curate.md owns every write; scripts/company_policy.py defines the choices and hold math.

- Search status: Proposed (agent-discovered, awaiting the user), Allow, Exclude. Only the human sets Allow/Exclude.
- Origin: Seed, User, Discovered. Company fit: High/Medium/Low/Unresolved against Career Goals company preferences only.
- Funding stage is ordered (Pre-seed / Seed, Series A–D, Series E+, Late private, Public, Unknown). Latest funding is compact (`Series C · $150M · lead`). Company evidence links the Drive capture.
- Policy confidence: Official, Recruiter, User (enforced); Community (recorded, not enforced); Not found (researched, no rule). Blank means Not assessed.
- Application hold status: Not assessed, No known hold, Held, Blocked (permanent), Needs clarification. Apply blocked until is Curate's UTC estimate; Apply recomputes before Submit.
- The personal limit in Settings `company_policy` (default 3 per company per rolling 30 days; Career Goals may override) applies on top of employer rules.

**Applications.** The 29 fields in scripts/stage_state.py:CORE_FIELDS, including Company, four stage Run links and History. The primary field Application ID is the formula RECORD_ID(); never write to it. Job key is the canonical employer posting identity for deduplication.

**Sources.** Source key (stable board identity), Company, Official careers URL, Catalog URL, Region, Reader, Reader version, Latest coverage, Checkpoint (JSON), Last error, Last scanned at, Last run, Archived at. The checkpoint holds cursor/end proof, counts, manifest identity and pagination details. Archived at disables a retired source; every other configured board/region stays in scope.

**Runs.** Run key, Run type, Status, Owner, Instruction revision, Input versions (JSON), Scope (JSON), Checkpoint (JSON), Expected/Completed/Blocked items, Started at, Finished at, Agent notes, plus Curate companies, History, Sources and the four Application stage links. Checkpoints keep per-stage progress, pending checks, next action and ownership release (`scripts/stage_state.py:run_progress` parses them). Input versions are frozen; progress updates never rewrite them. An expired heartbeat never proves another writer stopped.

**Settings.** Key, Value, Reference URL, Version, Verification, Notes. Private resource references, extracted preferences with their source revision, policies (`company_policy`, `submission_policy`) and live controls (`Pause applications`, `Stop all`). Procedures and command routing stay in Git.

**History.** Event key, Operation ID, Event type, Recorded at, Occurred at, Actor / channel, Table reference, Record reference, Field changes (JSON), Evidence URL, Notes, Application, Run. Use explicit event types (Review accepted, Field change, Submission intent, Confirmation received, Write failed, Write uncertain). Keep actual event time separate from recording time.

## Everyday view and notes

The Review view shows Company, Role, Lifecycle status, Manual notes, Agent notes, Starting salary, Max salary, Additional compensation, Location, Work arrangement, Job posted date, Career fit, Resume fit, Job description link and Resume link, with Manual notes beside status.

Manual notes belongs to the human: read it before processing a row and never overwrite it. Record a changed note or status you observe in the stage snapshot and History; it never authorizes submission or changes global criteria. Agent notes is one concise current handoff: the decision, its concrete evidence and any missing fact or next action, for example `Review: strong internal AI fit. Next: verify applicable US base range.` Previous values go to History. Neither notes field is an instruction source.

## Compact job facts

Starting salary and Max salary are numeric endpoints of one verified advertised base-pay band, in the single currency and period registered in Settings.applications_schema.salary_display. Pick the highest advertised maximum in that currency with its paired minimum; leave both blank when no compatible verified band exists. Never mix currencies or periods, convert implicitly, use total compensation or write zero. Additional compensation: Equity, Bonus, Commission, Bonus or commission, Not stated. Location holds short places; Work arrangement is Remote/Hybrid/On-site/Unspecified. Use scripts/tracker_values.py for parsing. Job evidence preserves the exact JD with every band, condition and location; Review checks applicability there.

No availability column is kept and inventory is not monitored for closure. A saved exact official JD can support Review; Apply checks the live form. When Scan reobserves a role, record source membership, observation time and content fingerprint in History; a changed fingerprint triggers comparison and affected re-review.

## Stage metadata

Stage snapshots live in History `Field changes (JSON)`:

    {"schema":"nextmove.stage-state.v2","records":[{"record_id":"...","job_key":"...","stage_runs":{},"source":{},"review":{},"preparation":{},"submission":{},"feedback":{},"details":{}}]}

Each record is a complete snapshot for one application, so recovery never replays a delta chain. Build it with `merge_state` (or `merge_company_state` for Curate), wrap it with `payload`, link the History row to the affected Applications and the Run, and read it back before accepting the handoff. Read with `resolve` (newest complete snapshot wins) and `stage_versions`. Batch within tool limits and parse outside model context.

`stage_runs` names the Scan, Review, Preparation and Submission runs; each matches the Application's Run link (at most one current context per stage). One full Run can fill all four.

Runs `Input versions (JSON).stage_inputs` holds shared fixed inputs per stage (goals, master, policy, guidelines, instruction versions); per-job metadata holds the exact `jd_hash`, decision and review time, with `version_overrides` for per-job differences. Null means unknown, never an inherited current value. Review's policy identity is `review-sha256:<digest>` of stages/review.md, computed by `scripts/role_gate.py:review_frame_contract`; editing that file requires revalidating affected approvals. Other policy identifiers live in contracts/policy-versions.json. A manually set Queued or Ready status is never acceptance evidence.

Long content (full JD captures, assessment evidence, resume change notes, role-specific answers) lives in versioned Drive files; `details` holds the file ID, role selector and integrity hash.

## Drive destinations

Settings.resume_output is the Role specific folder; Settings.content_output is the Audit trail folder. Both record root_folder_id; verify parent and privacy. RESUME-FILES.md owns placement and naming. Run captures, reports and metadata go to Audit trail.

## Stage writes

- **Curate:** company snapshots use `merge_company_state` with the company record ID and link to the Run, never to Applications. Run checkpoint `stages.curate` keeps holds, policy_research and discovery parts separately; discovery feed cursors live in Settings.company_policy.discovery.checkpoints and advance only after verified complete coverage.
- **Scan:** freeze scope from current Companies (`scan_enabled`) and active Sources; recheck targeting at the write boundary. `application_write(creating=True)` needs current Companies records, a new canonical Job key, Inventoried and Role eligibility Pending. Save source memberships, requisition IDs, aliases, capture selectors, observation times and fingerprints in `source`.
- **Review:** save the three-step assessment (method, exact input identities, career and resume ratings, total, outcome, evidence, unresolved questions) before changing status, fit ratings, Review run and Agent notes. Record the decisive company evidence identity in `stage_inputs.review.company_evidence`; Company fit is advisory and never copied into Career fit.
- **Prepare:** save `path`, base, base_version, base_master, guidelines version, coverage, company_consistency and, for tailored versions, change notes, `grounding`, `guideline_check`, editable source, file hash and visual verification. Set Preparation run, Resume link, Resume version and Resume verified at only after `resume_ready` passes on the downloaded bytes.
- **Apply:** save the preflight record (application URL, ATS family, field map, unresolved items, screenshots) and the `submission_gate` decision. Before Submit, write and read back the attempt intent (role, application URL, resume file ID and hash, answer digest), Submission attempt key and Submission run. Save the result or uncertainty; an existing attempt blocks any retry.
- **Track:** save message identities, confirmation, rejection and engagement times in History; update Lifecycle status and Confirmation reference. Missing mail never proves non-submission.

## History and integrity

Log meaningful changes and business events plus run-level read scope, not every read. Each event records identity, actor/harness, affected table/record/field, before/after values, evidence, actual event time and recording time. Keep receipts, failures, uncertainty and corrections even without a status change.

Airtable writes are not atomic: reconcile persisted state before any retry, and stop dependent work after an uncertain write. Owners can edit records directly, so History is a journal, not tamper-proof auditing. No automatic purge or retention window.

## Preferences and candidate facts

Career Goals holds desired work and tradeoffs only (CAREER-GOALS.md). The editable master, plus any confirmed-facts artifact indexed by Settings.master_resume, is the only source of candidate facts. Record the goals revision and candidate-evidence identity in each Review Run. Goals never authorize submissions or supply qualifications.
