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
