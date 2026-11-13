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

Map existing Applications and Target Companies headers to the templates. Add Job Inventory, Scan Audit, Runs and Controls tabs using the CSV headers in [templates](templates/). Keep existing tracker rows and statuses. For companies with several boards, use a source row per board with a shared company ID. Set up a catalog reader for each source and verify coverage against the live employer site.

Configure the scan's private source registry, durable runner state and reusable reader locations. Persist hashes, source/version evidence, pagination checkpoints, criteria/filter versions and descriptions in the existing authorized store; map optional fields without replacing the user's schema. A temporary workspace is not durable storage. Test baseline enumeration, source-manifest revalidation, description-only edits, additions/removals, expired cursors and interrupted write readback before relying on incremental results. These instructions and configuration fields do not install an incremental scanner; the chosen runtime must implement them. If state or readers are missing, report that and perform baseline/setup work.

Keep the default description policy all and recovery budgets unset unless the user chooses otherwise. Candidate-only description retrieval reduces archival depth and post-closure reassessment; a recovery cutoff limits the effort spent recovering sources and can leave current coverage incomplete. Record the user's choice privately and in the run audit. Do not silently add cache freshness windows, sampling-only verification or page caps.


## Company application restrictions

Store per-company limits and cooldowns in Target Companies, separately from Search status and Pool. A temporary hold does not exclude a company from scanning. Map the optional fields in templates/companies.csv to live headers; extend the existing tab during authorized setup without replacing company data. Blank policy values mean unrecorded, not zero or unlimited. New rows start with Application hold status “Not assessed”.

| Live header | Template field | Meaning |
|---|---|---|
| Max applications | max_applications | Confirmed positive whole-number limit within the specified window. |
| Application window (days) | application_window_days | Day-based window length; use details for calendar/fixed reset boundaries. |
| Application window type | application_window_type | Rolling / Calendar / Fixed / Unconfirmed. |
| Rejection cooldown (days) | rejection_cooldown_days | Confirmed wait after a qualifying rejection; details specify elapsed/calendar days and trigger. |
| Restriction scope | restriction_scope | Company / Role family / Exact role / Mixed / Unconfirmed. Mixed rules need separate scopes in details. |
| Last rejection date | last_rejection_at | Actual qualifying event date/time and evidence; not itself a company-wide ban. |
| Apply blocked until | apply_blocked_until | Earliest date/time after all applicable restrictions; prefer ISO8601 with an explicit offset. |
| Application hold status | application_hold_status | Not assessed / No known hold / Held / Needs clarification; separate from role fit and pipeline stage. |
| Restriction details / source | restriction_details_or_source | Published rule or explicit user instruction, evidence/date, duration basis, exceptions, affected roles, reset times and additional limits. |
| Restriction last verified | restriction_last_verified_at | When the rule/evidence was actually reviewed. |
| Restriction timezone | restriction_timezone | Confirmed IANA timezone for boundaries/date-only inputs; do not assume the Sheet's timezone. |

Do not infer a company cooldown from a generic rejection or invent a waiting period. Preserve exact-role dispositions. Confirm scope, duration, trigger and rolling/calendar/fixed semantics. If multiple constraints apply, all must allow the submission; a future date is only an estimate until the quota is recomputed. Multiple windows or mixed scopes must be recorded in details and not silently collapsed to one rule.

Count distinct confirmed submission events in the applicable window, including applications subsequently rejected or withdrawn unless the rule explicitly restores capacity. Deduplicate duplicate tracker rows and receipts; include known external/manual applications. Uncertain attempts may occupy capacity but must not be marked Applied. If allowance cannot be proven, reconcile before submitting. Determine the next rolling-window opening when enough events expire, not necessarily when only the oldest event expires.

Keep scanning and saving qualifying Discovered jobs while an application hold applies. Record the hold separately; do not lower relevance because of a temporary restriction. Recheck the live company rule, current submission history, scope, timezone and all pause/stop controls immediately before Submit, using one submission worker. An elapsed date does not authorize auto-apply, prove role eligibility, or override any remaining limit. Known restrictions with unresolved dates/scope remain held for clarification.

Before enabling auto-apply, configure a private answer bank, supported sites and submission cap, and connect an authorized browser runtime. Test one form, receipt capture, duplicate prevention, a simulated uncertain submission, and the live pause control. Use one submission worker.

## Existing inputs and new destinations

Ask for private links or local paths to existing inputs such as the master resume and target company list. A cloud link requires an authenticated connection; keep it outside Git.

During setup, reuse the tracker and resume output folder if supplied. Otherwise, with setup authorization and cloud write access, create only the missing destinations: a private **Nextmove — Application Tracker** seeded from the tracker template, and a private **Nextmove — Resumes** folder. Verify them, return their links, and record those links in private configuration when possible. Reuse known destinations on later runs. If a supplied link is inaccessible, report the issue instead of creating a replacement.

Creating empty destinations during setup does not authorize writing application records or saving resumes. Review mode still proposes changes. If cloud creation is unavailable, report what is missing and continue in review mode where possible.
