# Six-table architecture

Default: one capable agent completes a thorough Run. Manual stage-by-stage harness switching uses identical criteria, evidence and checkpoints. No model API or automatic cross-harness launcher is required.

| Table | Purpose |
|---|---|
| Companies | Explicit choices, notes and confirmed restrictions |
| Applications | Admitted PM roles, career gate, fit, resume/submission state and preserved legacy history |
| Sources | One board/region, coverage and cursor |
| Runs | One full invocation by default, or one manual stage; scope, stage progress, pending checks, blockers and handoff |
| Settings | Private references, criteria, execution policy and live controls |
| History | Meaningful mutations/business events, failures and uncertainty |

Git owns instructions. Drive owns documents, admitted-role captures, PDFs and bounded reports. Unrelated catalog rows are transient inputs, not a second hidden inventory.

~~~mermaid
flowchart LR
    Human[Human scope and authorization] --> Agent[One active agent]
    Git[Versioned instructions] --> Agent
    Agent <--> State[Six Airtable tables]
    Agent <--> Drive[Private content]
    Agent --> Official[Official catalogs and supported sites]
    Agent --> Handoff[Verified stage checkpoint]
    Handoff --> Next[Same agent or manually selected next harness]
~~~

## Single-agent-first execution

Run resolves Settings and pins current inputs/instructions once. Reuse verified unchanged inputs within that invocation; recheck authoritative versions and live controls at relevant boundaries. Changed JD/master/goals invalidate only affected decisions. No unverified freshness TTL.

Keep stage scopes, counts, blocked identities, artifacts and next cursor in one Run. Applications hold job progress; Sources hold board progress. Continue independent useful work despite item-specific blockers. Missing global access, Stop all or uncertain writes stop affected work. Apply needs separate authorization; Track can independently lack mail access. Unresolved required work means Partial/Blocked.

Manual commands save the same shape and stop after one stage. The next harness reads state and appends ownership/attempt evidence in History; it needs no chat summary. One active writer owns mutations. A stale heartbeat does not prove a worker stopped; Airtable ownership fields are not atomic locks.

## Admission and queue boundaries

Complete catalog enumeration is transient. Broad title aliases find PM candidates for verification; they do not create records. Confirm actual PM function and experience above the configured threshold OR evidence-backed equivalent senior scope. Missing titles and ambiguous levels require targeted checks. Only verified roles become Inventoried.

After admission, check domain, industry, vertical, company stage/geography and other current goals. Pass → Queued; hard mismatch → Not aligned; unknown → hold. A positive resume match cannot waive a hard career exclusion. ROLE-ELIGIBILITY.md defines the boundary.

Pending checks store minimal source/posting identity, URL, reason, input version and retry checkpoint in Runs. Use bounded checkpoint segments if needed; never truncate or create a general work-item framework. Preserve pending cases without calling them admitted inventory.

## Relationships and recovery

A company has many sources/applications; a role may belong to multiple sources. Native IDs identify records, business keys support retries and matching. Historical unmatched applications retain provenance rather than guessed links.

Current resume/JD references, versions and verification stay on Applications; reusable readers on Sources/Settings. Prior values and business events stay in History. No general artifact registry. A submission attempt still gets a distinct identity, exact resume version and outcome before any retry.

Persist all operational state in Airtable and content in registered Drive locations. Local files/chat are accelerators only. Reconcile actual outputs before retrying an interrupted write. A finished batch is not a completed stage.

## History and migration

Use meaningful change/event history and run-level read scope instead of routine per-read rows. Airtable does not provide SQL uniqueness/foreign-key transactions or universal immutable logs through this design.

Migrate only with authorization and verified durable backup. Preserve outcomes, notes, restrictions, source identities and resource references. Legacy unreviewed Queued rows become a revalidation backlog, not certified inventory under new gates. Never erase submitted/terminal history because search criteria changed.

Old unfiltered catalogs/retired tables may remain one-off private recovery archives. They are not new inventory. Future clear rejects retain aggregate counts only, reducing post-closure re-filtering of excluded roles. Investigate ambiguity while postings are available; disclose that retention tradeoff.

core-schema.json is the active six-table blueprint. state-schema.json is a deprecated compatibility marker. Preserve/map existing fields rather than recreating IDs or dropping provenance.
