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

Before enabling auto-apply, configure a private answer bank, supported sites and submission cap, and connect an authorized browser runtime. Test one form, receipt capture, duplicate prevention, a simulated uncertain submission, and the live pause control. Use one submission worker.

## Existing inputs and new destinations

Ask for private links or local paths to existing inputs such as the master resume and target company list. A cloud link requires an authenticated connection; keep it outside Git.

During setup, reuse the tracker and resume output folder if supplied. Otherwise, with setup authorization and cloud write access, create only the missing destinations: a private **Nextmove — Application Tracker** seeded from the tracker template, and a private **Nextmove — Resumes** folder. Verify them, return their links, and record those links in private configuration when possible. Reuse known destinations on later runs. If a supplied link is inaccessible, report the issue instead of creating a replacement.

Creating empty destinations during setup does not authorize writing application records or saving resumes. Review mode still proposes changes. If cloud creation is unavailable, report what is missing and continue in review mode where possible.
