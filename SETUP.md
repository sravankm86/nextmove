# Before you start

| Capability | Provide | Minimum access | If missing |
|---|---|---|---|
| Search and verify openings | Target roles, locations, company list | Official catalogs and a reader that can enumerate their pages | Review supplied descriptions; label live status unverified |
| Check duplicates | Live tracker or current CSV export | Read | Label results provisional; do not add Pending rows |
| Reconcile recruiting mail | Gmail, Outlook, or selected messages | Read only | Skip reconciliation |
| Tailor a resume | Latest master resume | Read | Skip tailoring; never infer facts |
| Save approved results | Tracker and resume destination | Write to those destinations only | Return a proposed patch and files for manual use |

Copy `config.example.yaml` into a private folder outside the repo. Use local paths or private links your tool can open. Connect accounts through the tool you chose; do not paste passwords or tokens into config. The templates are CSVs and work with a local spreadsheet or an imported table. No connector is installed by this repository.

For scheduling, first confirm an interactive run works, then give your scheduler the same versioned instructions and private inputs. Start in review mode.

Follow [STORAGE.md](STORAGE.md). Discover the configured Airtable base and map existing Applications and Target Companies fields to the templates. Add missing Job Inventory, Catalog Sources, Scan Audit, Runs and Controls tables during authorized setup using the logical CSV headers in [templates](templates/). Keep existing tracker rows and statuses. When configured and authorized, map the lifecycle-events and mail-audit templates into the existing private store; do not create new destinations or silently migrate statuses. For companies with several boards, use a source row per board with a shared company ID. Set up a catalog reader for each source and verify coverage against the live employer site.

Configure the scan's private source registry, durable runner state and reusable reader locations. Persist hashes, source/version evidence, pagination checkpoints and criteria/filter versions in Airtable; keep full descriptions and reusable content in Drive with accessible references; map optional fields without replacing the user's schema. A temporary workspace is not durable storage. Test baseline enumeration, source-manifest revalidation, description-only edits, additions/removals, expired cursors and interrupted write readback before relying on incremental results. These instructions and configuration fields do not install an incremental scanner; the chosen runtime must implement them. If state or readers are missing, report that and perform baseline/setup work.

Keep the default description policy all and recovery budgets unset unless the user chooses otherwise. Candidate-only description retrieval reduces archival depth and post-closure reassessment; a recovery cutoff limits the effort spent recovering sources and can leave current coverage incomplete. Record the user's choice privately and in the run audit. Do not silently add cache freshness windows, sampling-only verification or page caps.


## Company application restrictions

Store per-company limits and cooldowns in Target Companies, separately from Search status and Pool. A temporary hold does not exclude a company from scanning. Map the optional fields in templates/companies.csv to live headers; extend the existing table during authorized setup without replacing company data. Blank policy values mean unrecorded, not zero or unlimited. New rows start with Application hold status “Not assessed”.

| Live header | Template field | Meaning |
|---|---|---|
| Max applications | max_applications | Confirmed positive whole-number limit within the specified window. |
| Application window (days) | application_window_days | Day-based window length; use details for calendar/fixed reset boundaries. |
| Application window type | application_window_type | Rolling / Calendar / Fixed / Unconfirmed. |
| Rejection cooldown (days) | rejection_cooldown_days | Confirmed wait after a qualifying rejection; details specify elapsed/calendar days and trigger. |
| Restriction scope | restriction_scope | Company / Role family / Exact role / Mixed / Unconfirmed. Mixed rules need separate scopes in details. |
| Last rejection date | last_rejection_at | Actual qualifying event date/time and evidence; not itself a company-wide ban. |
| Apply blocked until | apply_blocked_until | Earliest date/time after all applicable restrictions; prefer ISO8601 with an explicit offset. |
| Application hold status | application_hold_status | Not assessed / No known hold / Held / Needs clarification; separate from role fit and lifecycle status. |
| Restriction details / source | restriction_details_or_source | Published rule or explicit user instruction, evidence/date, duration basis, exceptions, affected roles, reset times and additional limits. |
| Restriction last verified | restriction_last_verified_at | When the rule/evidence was actually reviewed. |
| Restriction timezone | restriction_timezone | Confirmed IANA timezone for boundaries/date-only inputs; do not assume the Sheet's timezone. |

Do not infer a company cooldown from a generic rejection or invent a waiting period. Preserve exact-role dispositions. Confirm scope, duration, trigger and rolling/calendar/fixed semantics. If multiple constraints apply, all must allow the submission; a future date is only an estimate until the quota is recomputed. Multiple windows or mixed scopes must be recorded in details and not silently collapsed to one rule.

Count distinct human/agent-reported or evidenced submission events in the applicable window (including Applied without a receipt), including applications subsequently rejected or withdrawn unless the rule explicitly restores capacity. Deduplicate duplicate tracker rows and receipts; include known external/manual applications. Uncertain attempts may occupy capacity but must not be marked Applied. If allowance cannot be proven, reconcile before submitting. Determine the next rolling-window opening when enough events expire, not necessarily when only the oldest event expires.

Keep scanning and saving qualifying Queued jobs while an application hold applies. Record the hold separately; do not lower relevance because of a temporary restriction. Recheck the live company rule, current submission history, scope, timezone and all pause/stop controls immediately before Submit, using one submission worker. An elapsed date does not authorize auto-apply, prove role eligibility, or override any remaining limit. Known restrictions with unresolved dates/scope remain held for clarification.

Before enabling auto-apply, configure a private answer bank, supported sites and submission cap, and connect an authorized browser runtime. Test one form, receipt capture, duplicate prevention, a simulated uncertain submission, and the live pause control. Use one submission worker.

## Worker fields and handoff setup

Map the optional Applications fields for job_posted_at/job_posted_text, work_arrangement/location_details, posted_salary/salary_details, independent career_fit/resume_fit, review versions/time/hash, review_pending, resume_type/master version/verification/claim reference and next_owner. Keep axis-specific rationale in fit_rationale and changes in resume_notes. Preserve legacy fields and hide technical columns if useful; do not force every optional field into the main visible view. Unknown salary, location or posted date is not date found or an estimate.

Configure five logical responsibilities and their queues from WORKFLOW.md. Keep bulk readers/writes in code and a single shared-state writer. For Tracker, configure read-only mailbox scope, pagination, event deduplication and a durable successful checkpoint with overlapping lookback. Test a generic acknowledgement, duplicate receipt, older acknowledgement after rejection, ambiguous role match and uncertain submission. Missing mail access must be visible and must not be reported as reconciled.

These schemas and instructions do not install workers, email automations or a live tracker migration. Old Reviewed/Rated means “assessed”, not necessarily positive: reclassify only from supporting two-axis evidence or send to review-owned Needs review. Preserve historical outcomes, dates and user edits.

## Applications lifecycle format

Map Applications to [LIFECYCLE.md](LIFECYCLE.md). Use one Lifecycle status dropdown. Separate Applied on, Confirmed on, Outcome on, Status source, Status notes and Status recorded at. Preserve the old combined status/date text and pipeline values in read-only legacy fields when migrating; do not drop notes, dispositions or fit assessments. Maintain dropdown and filter coverage when appending rows. Unknown historical dates stay blank. A resume link alone does not make a row Ready. Manual dropdown edits require date/source updates unless an explicit runtime supplies them.

## Existing inputs and new destinations

Ask for private links or local paths to existing inputs such as the master resume and target company list. A cloud link requires an authenticated connection; keep it outside Git.

During setup, reuse the tracker and resume output folder if supplied. Otherwise, with setup authorization and cloud write access, create only the missing destinations: a private **Nextmove** Airtable base with mapped tracker tables, and a private **Nextmove — Resumes** folder. Verify them, return their links, and record those links in private configuration when possible. Reuse known destinations on later runs. If a supplied link is inaccessible, report the issue instead of creating a replacement.

Creating empty destinations during setup does not authorize writing application records or saving resumes. Review mode still proposes changes. If cloud creation is unavailable, report what is missing and continue in review mode where possible.


## Airtable migration and capacity

A workspace is a container; it still needs a base and tables. Use the existing configured Nextmove base and read STORAGE.md before setup or migration. Keep Drive authoritative for content. Import companies and applications first, then catalogs/audits and inventory metadata. Preserve raw legacy records, actual dates and stable keys; do not invent missing facts or silently promote Reviewed to Shortlisted. Verify every changed value and relationship by readback, then verify table totals and record a durable migration checkpoint. Retain the original Sheets as a backup/content source; after cutover do not dual-write trackers. Never infer that an imported historical audit proves a new scan completed.

Check actual service errors and available plan information; do not assume a plan's capacity or purchase an upgrade. At a capacity/quota error, stop affected writes, reconcile uncertain batches, retain verified progress and report the precise limit and remaining counts. Resume idempotently after capacity is available. Migration does not enable workers, scheduling, mailbox access or submission authorization.


## Audit and integrity readiness

Follow [DATA-GOVERNANCE.md](DATA-GOVERNANCE.md). Set up Audit Events separately from scan/mail/lifecycle logs. Expose immutable Record ID, Created at/by, Updated at/by and Archived at fields without confusing system times with historical event dates. Test controlled read logging, create/update before/after values, archive, idempotent retry, stale human edits and a failed audit sink before enabling a worker. Record the verified audit scope and unimplemented coverage in private Controls. Do not label a table, policy document, draft automation or latest-modified timestamp as a functioning universal audit system. A direct UI/API bypass, inaccessible permissions or missing gateway is an explicit coverage gap. Retention, access controls and relational enforcement require a deliberate architecture decision; do not buy a plan or move platforms implicitly.


## Register a manually chosen harness once

Save HARNESS-BOOTSTRAP.md in the harness's supported persistent instructions or reusable task template, with the existing private base reference supplied outside Git. Connect Airtable, Google Drive and stage-specific tools there. Register the current goals document, designated editable master, resume destination, captured-description content and optional base resume in Context Registry. Keep unknown answer banks, mailbox scope and submission authorization explicitly unresolved. Use the six state tables in COMMANDS.md for run scope, attempts, artifacts and handoffs. Setup does not invoke a stage.

Test Scan, Review, Prepare, Apply preflight and Track only when explicitly requested and supported. Verify a fresh session can recover the same inputs, persist audited state, resume released unfinished work, reconcile an uncertain write and stop without launching the next command. A dry contract check or new schema is not a live provider test. Bare Apply remains subject to explicit authorization, answer/cooldown checks and live Pause applications.
