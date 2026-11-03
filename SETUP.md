# Before you start

| Capability | Provide | Minimum access | If missing |
|---|---|---|---|
| Search and verify openings | Target roles, locations, company list | Public web search and employer posting retrieval | Review supplied descriptions; label live status unverified |
| Check duplicates | Live tracker or current CSV export | Read | Label results provisional; do not add Pending rows |
| Reconcile recruiting mail | Gmail, Outlook, or selected messages | Read only | Skip reconciliation |
| Tailor a resume | Latest master resume | Read | Skip tailoring; never infer facts |
| Save approved results | Tracker and resume destination | Write to those destinations only | Return a proposed patch and files for manual use |

Copy `config.example.yaml` into a private folder outside the repo. Use local paths or private links your tool can open. Connect accounts through the tool you chose; do not paste passwords or tokens into config. The templates are CSVs and work with a local spreadsheet or an imported table. No connector is installed by this repository.

For scheduling, first confirm an interactive run works, then give your scheduler the same versioned instructions and private inputs. Start in review mode.

## Existing inputs and new destinations

Ask for private links or local paths to existing inputs such as the master resume and target company list. A cloud link requires an authenticated connection; keep it outside Git.

During setup, reuse the tracker and resume output folder if supplied. Otherwise, with setup authorization and cloud write access, create only the missing destinations: a private **Nextmove — Application Tracker** seeded from the tracker template, and a private **Nextmove — Resumes** folder. Verify them, return their links, and record those links in private configuration when possible. Reuse known destinations on later runs. If a supplied link is inaccessible, report the issue instead of creating a replacement.

Creating empty destinations during setup does not authorize writing application records or saving resumes. Review mode still proposes changes. If cloud creation is unavailable, report what is missing and continue in review mode where possible.
