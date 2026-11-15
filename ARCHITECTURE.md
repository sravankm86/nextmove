# Six-table architecture

Default: one capable agent completes a thorough Run. Manual stage-by-stage harness switching uses identical criteria, evidence and checkpoints. No model API or automatic cross-harness launcher is required.

| Table | Purpose |
|---|---|
| Companies | Explicit choices, notes and confirmed restrictions |
| Applications | Plausible PM candidates, review/eligibility, fit, notes, resume/submission state and preserved legacy history |
| Sources | One board/region, coverage and cursor |
| Runs | One full invocation by default, or one manual stage; scope, stage progress, pending checks, blockers and handoff |
| Settings | Private references, criteria, execution policy and live controls |
| History | Meaningful mutations/business events, failures and uncertainty |

Git owns instructions. Career Goals is preference-only input interpreted under CAREER-GOALS.md; Settings may cache extracted values with source versions, not redefine workflow logic. Drive owns documents, candidate-role captures, PDFs and bounded reports. Unrelated catalog rows are transient inputs, not a second hidden inventory.

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

Run resolves Settings and pins current inputs/instructions once. Reuse verified unchanged inputs within that invocation; recheck authoritative versions and live controls at relevant boundaries. Changed JD/master/goals invalidate only affected decisions. No unverified time-based freshness assumption.

Keep stage scopes, counts, blocked identities, artifacts and next cursor in one Run. Applications hold job progress; Sources hold board progress. Continue independent useful work despite item-specific blockers. Missing global access, Stop all or uncertain writes stop affected work. Apply needs separate authorization; Track can independently lack mail access. Unresolved required work means Partial/Blocked.

Manual commands save the same shape and stop after one stage. The next harness reads state and appends ownership/attempt evidence in History; it needs no chat summary. One active writer owns writes. A stale heartbeat does not prove a worker stopped; Airtable ownership fields are not atomic locks.

## Candidate inventory and review boundary

Scan first derives broad function/designation/seniority criteria from the current Career Goals revision (or verifies its current extracted snapshot), then enumerates all catalogs without storing unrelated rows and uses broad PM aliases with basic semantic checks. Plausible senior PM candidates become Inventoried with eligibility Pending; ambiguous level is resolved by Review. Clear unrelated/junior roles contribute aggregate rejects. Unknown identity or insufficient evidence of plausibility remains a minimal Run pending check. No career-goal filtering or Queued approvals during Scan.

Review owns full-JD function/experience-or-equivalent-scope verification, current career goals and resume fit. Eligible aligned candidates with High career fit OR High resume fit become Queued for Prepare. Hard career mismatch → Not aligned; clear role/scope failure or both fit axes Low → Not a fit; unresolved → Needs review. Shortlisted is legacy only. See ROLE-ELIGIBILITY.md.

Review dispositions use versioned reason categories. SCAN-OPTIMIZATION.md improves clear basic-screen errors while preserving eligible positives and testing sampled rejects. Career mismatches, missing evidence and closures are not automatically scanner negatives. This deliberately permits more candidate rows than verified-only inventory to protect recall.

Runs holds bounded unresolved source/identity checkpoints; Applications holds plausible candidates and their review outcomes. Never truncate pending state or build a general work-item framework.

## Relationships and recovery

A company has many sources/applications; a role may be observed on multiple sources, recorded in its scan History metadata rather than an Applications relationship. Native IDs identify records, business keys support retries and matching. Historical unmatched applications retain provenance rather than guessed links.

The 28-field Applications profile retains current evidence/PDF references, PDF version/verification and four stage Run links. Exact metadata lives in bounded History snapshots and shared fixed inputs in Runs under STAGE-STATE.md; reusable readers stay on Sources/Settings. Prior values and business events stay in History. No general artifact registry. A submission attempt still gets a distinct identity, exact resume version and outcome before any retry.

Persist all operational state in Airtable and content in registered Drive locations. Local files/chat are accelerators only. Reconcile actual outputs before retrying an interrupted write. A finished batch is not a completed stage.

## History and migration

Use meaningful change/event history and run-level read scope instead of routine per-read rows. Airtable does not provide SQL uniqueness/foreign-key transactions or universal unchangeable logs through this design.

Migrate only with authorization and verified durable backup. Preserve outcomes, notes, restrictions, source identities and resource references. Legacy unreviewed Queued rows become a revalidation backlog, not certified review approval under new gates. Never erase submitted/terminal history because search criteria changed.

Old unfiltered catalogs/retired tables may remain one-off private recovery archives. They are not new inventory. Future clear rejects retain aggregate counts only, reducing post-closure re-filtering of excluded roles. Investigate ambiguity while postings are available; disclose that retention tradeoff.

core-schema.json is the active six-table blueprint. state-schema.json is a deprecated compatibility marker. Preserve/map existing fields rather than recreating IDs or dropping provenance.
