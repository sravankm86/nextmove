# Workflow and lifecycle

Read AGENTS.md and the requested stage. Load reference docs only when needed, and keep bulk catalogs/verification of saved values outside model context.

| Command | Scope |
|---|---|
| Run / Run Nextmove | Default single agent: Curate → Scan → Review → Prepare → Apply → Track (ends at Interviewing) |
| Curate / Companies | Recompute every company application hold; research employer limits/cooldowns; on cadence propose Series C+ funded companies as Proposed. Never sets Allow/Exclude |
| Scan | Derive broad role criteria from current goals; complete source coverage and basic semantics → Inventoried; no career-fit assessment |
| Review / Assess / Shortlist | Inventoried/Need review → JD extraction, career fit and resume fit scores → Queued, Need review or Not pursuing |
| Prepare | Current review-approved Queued roles |
| Apply | Ready roles without unresolved attempts; preflight unless separately authorized |
| Track | Exact-role mail/receipt reconciliation from checkpoint |

Quoted examples/setup discussions do not dispatch production work. A single stage stops after handoff. Run advances authorized useful stages without asking to continue, but cannot infer submission permission or launch another harness.

## Startup and ownership

Discover/map the six tables, Settings and live controls. Curate runs first in a Run so Scan reads the current Allow list and Apply sees current holds; a Partial Curate does not block Scan/Review/Prepare, but Apply needs its hold recompute. For Scan/Review resolve the current Career Goals revision and validate the corresponding preference set of extracted preferences/readiness under CAREER-GOALS.md; reuse one verified extraction within a full Run and refresh affected values if it changes. Record run-level read scope, not routine per-read events. Resolve goals/master/content as required and verify this harness's access/capabilities. Connections and local files are not inherited.

Resume one compatible released unfinished Run or create one. Pin instruction/input versions, owner and frozen scope. A full run uses one row with stage checkpoints; manual invocations use the same checkpoint format. Sources hold board cursors and Applications hold job state. Bounded Run segments handle oversized pending lists without truncation.

One active writer. Never seize an owner solely on timeout. Missing global access, Stop all or uncertain writes block affected work; item problems need not stop independent work. Submission pause affects Apply, not useful Scan/Review/Prepare/Track work.

## Run checks: objective duplicate discovery

Every invocation, including a single stage command, starts with Run checks. Build one company-scoped identity index from live role IDs, official job links, role names and posted dates. Refresh this index when Scan encounters new postings. Run owns discovery; Review and later stages consume its result rather than repeating duplicate searches.

An exact verified employer role ID or verified posting-specific canonical link confirms identity. Role name and posted date corroborate it; they cannot alone prove identity. Preserve meaningful URL parameters. Different verified role IDs, regional postings or conflicting evidence need reconciliation rather than a title-based merge. Use scripts/stage_state.py:run_duplicate_match.

Reobserving an existing posting does not create another row or turn the canonical record into Duplicate. For confirmed redundant rows, retain the record with actual application history or authoritative human state as canonical; preserve submitted/rejected/interview outcomes. Mark only the verified redundant record Duplicate, save duplicate_of, objective evidence and original values in History, and retain all notes and artifacts. Historical mirror copies require evidence that they describe the same application. An unresolved identity stays a Run question and cannot advance automatically. Do not delete or merge distinct submissions.

Use Duplicate evidence to improve reader identity/canonicalization and prevent repeated inserts. Do not learn career exclusions or title blacklists from it. Record checked counts, confirmed pairs, canonical IDs and unresolved cases in the Run checkpoint. DATA.md defines preservation and verification.

## Execute and persist

Use code for enumeration, normalization, identity, candidate filters, hashes and verification. Reuse verified unchanged inputs, but recheck authoritative versions and live gates at relevant boundaries. No unverified time-based freshness assumption, hidden page/item/time cap or false completion after one batch.

Scan inventories plausible PM candidates after keywords/basic semantics, including uncertain seniority for Review. Unknown identity remains a Run checkpoint; clear unrelated/junior failures produce aggregate counts. Review uses the three-step scoring frame in stages/review.md. Personal requirements come from current Career Goals; candidate facts come from the editable master. Career fit measures desired work; resume fit measures demonstrated suitability for the whole JD. Follow the numeric routing in stages/review.md, including Unresolved at zero; only a current qualifying score can advance to Prepare. Record review reason categories and follow stages/scan.md for validated improvements; do not learn career exclusions into Scan.

Preserve human outcomes/notes. Read Manual notes and current status under DATA.md before processing and writing a job; record newly observed feedback in the stage snapshot/History without rewriting the notes. Legacy Queued rows require explicit current review evidence, not automatic certification. Do not reopen submitted/terminal roles when fit inputs change.

Reread affected state, reconcile human edits, write permitted deltas and verify actual persisted values/artifacts. Save meaningful changes/events and failed/uncertain writes in History under the run. For bounded migration batches, exact per-record private delta artifacts can be indexed by a verified History manifest; never hide unverified changes.

Applications retains current evidence/PDF references, current PDF version/verification and stage Run links. DATA.md stores exact stage metadata in History and fixed shared inputs in Runs. Content lives in registered Drive locations. Schema-only releases retain decision-policy versions; changed decision inputs still require revalidation. A vanished local reader is a recovery gap, not evidence of incremental support.

Review owns final eligibility/hard career checks and approves Queued; Prepare requires its current acceptance evidence. A base PDF requires factual/current/visual verification; a URL does not mean Ready. Before Submit persist unique attempt identity and exact resume version. Require explicit scope, answers, an accessible actual application form, restrictions and live controls; capture receipt or uncertainty. Never blind-retry, and never infer non-submission from missing mail.

## Stage boundaries and exit

Save accepted stage outputs before advancing. Continue independent useful work safely, but blocked required stages/items mean Partial/Blocked. Verify every planned item and count before Complete. No work means verified empty eligible scope, not invented coverage.

Persist versions, outputs, pending identities/reasons, errors, next action and ownership release. Report Curate results (holds by status, policies researched by confidence, discovery feed coverage, Proposed companies awaiting the user), source coverage, transient rejects, plausible inventory, review-pending, verified eligible, approved queue and later outcomes separately. A new harness must recover this without prior chat/local state.

Use the 29-column tracker under DATA.md. Write concise current context and next action in Agent notes; never overwrite Manual notes. Resolve explicit review checks and structured feedback from History. Sources remains board-level scanner state, not an Applications field. Do not require posting availability during Scan/Review or maintain Last seen at; check the real form during Apply.

## Clarification rules

Every harness must ask concise, targeted questions when essential information is missing or contradictory. Users do not need to write agent instructions.

Before each stage check the requested scope, required tools, current source references and relevant preferences. Ask when ambiguity changes which roles are eligible, a hard career requirement, the resume's factual content, application answers, submission authorization or a company restriction. State the uncertain fact, why it matters and which work can continue. Group related questions and do not ask again for an answer already provided.

Save the question, affected records, reason and next action in the Run. Wait for an answer before dependent work. Continue independent useful work. Do not treat elapsed time, silence, a missing salary or a blank preference as an answer. Unknown soft preferences can remain disclosed without blocking unrelated work. Use reasonable implementation choices for reversible details already within scope; do not ask permission for every step.

When the answer arrives, save the authorized preference/control change in its proper source, record History, refresh affected decisions and resume. If a goal changes, update preference data; if workflow behavior changes, update Git. Never silently write executable instructions into Career Goals.

If a tool or automatic approval review blocks an action, identify the exact action and stated reason. Finish independent work and present the concrete remaining approval or access requirement. Never call an incomplete stage Complete.

A stage handoff reports completed work, counts, unresolved questions, affected identities, next action and whether ownership was released. Missing global access/Stop all blocks affected work. A company-specific issue need not stop all companies. See WORKFLOW.md and DATA.md.

## Nine lifecycle states

| State | Meaning |
|---|---|
| Inventoried | Newly admitted candidate awaiting its first review. |
| Need review | Review is unresolved, the score is in the middle band, or current evidence needs reassessment. Agent notes identifies why. |
| Queued | A current, evidence-backed Review score reaches the queue threshold. |
| Ready | The grounded resume/PDF is verified; submission needs separate authorization. |
| Applied | Submission is established; confirmation is additional evidence. |
| Interviewing | Active recruiter engagement, screening, assessment or interview. Recruiting endpoint. |
| Not pursuing | Review score is below the threshold, or the human chose to stop. |
| Rejected | Actual employer rejection. |
| Duplicate | Run confirmed a redundant record and saved its canonical record and objective evidence. |

The successful path is Inventoried → Queued → Ready → Applied → Interviewing, with Need review available before approval. Need review is retried when its missing facts change or the user requests it. A company cooldown or hold does not change fit; Curate owns holds under stages/curate.md. Preserve human declines and submitted/terminal outcomes. Offers and post-interview outcomes remain outside automatic tracking scope.

An uncertain Submit stays at its last verified pre-submission stage, normally Ready, with a prominent uncertainty note and saved attempt identity/outcome. Never label an unverified resume Ready or claim Applied without evidence. The outstanding attempt blocks another Submit regardless of manual status resets; reconcile it first. Hold other work that could obscure the outstanding attempt and its exact submitted PDF.

Keep confirmations in Confirmation reference, ratings in Career fit/Resume fit, and exact scores, reasons and duplicate references in History. Agent notes explains both scores and the outcome. A status label alone is not acceptance, PDF verification or submission permission. The three-step score supersedes older OR-fit, preferred-majority and provisional-salary queue rules.

## Existing status migration

Preserve exact prior status, notes, timestamps, evidence and outcomes before changing a label. Existing reviewed-but-unresolved Inventoried records become Need review; genuinely unreviewed records remain Inventoried. Needs review/Needs eligibility and historical Needs attention labels normalize to the existing Need review state. Keep the existing Airtable choice and its identity; no UI rename or extra pending state is needed. Existing Duplicate records retain Duplicate. Confirmed becomes Applied; In process becomes Interviewing. Other obsolete decline labels map to Not pursuing with their original reasons retained. Do not infer a duplicate from an old reason alone: Run verifies objective identity.

Old Queued/Ready approvals need current scored Review evidence before advancing. Do not manufacture new scores from old High/Medium labels whose definitions differed. Preserve old acceptance and submitted/terminal history. Add the two new select choices, verify mappings, and retire obsolete choices only when unused. If the connector cannot manage choices, save the exact remaining UI action and keep the migration Partial.
