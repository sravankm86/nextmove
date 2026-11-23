# Workflow and lifecycle

Read AGENTS.md and the requested stage. Load reference docs only when needed, and keep bulk catalogs/verification of saved values outside model context.

| Command | Scope |
|---|---|
| Run / Run Nextmove | Default single agent: Curate → Scan → Review → Prepare (ends at Ready) |
| Curate / Companies | Refresh company/funding evidence; on cadence propose matching companies new to the list as Proposed. Never sets Allow/Exclude |
| Scan | Derive broad role criteria from current goals; complete source coverage and basic semantics → Inventoried; no career-fit assessment |
| Review / Assess / Shortlist | Inventoried/Need review → JD extraction, career fit and resume fit scores → Queued, Need review or Not pursuing |
| Prepare | Current review-approved Queued roles → reuse a fully covering approved base or tailor from the closest base under the resume guidelines → verified resume and approved/resolved required answers → Ready |
| Review eval / Eval Review | Capture feedback, prepare frozen label-free inputs, run a fresh blind Review and score it under DATA.md; no production decisions change |
| Capture feedback | Move feedback into verified eval cases and clear only the captured unchanged notes; no role decisions |

Match command aliases as complete phrases: Review eval / Eval Review is an Experiment, not production Review.

Quoted examples/setup discussions do not dispatch production work. A single stage stops after handoff. Run advances authorized useful stages without asking to continue, and stops at the verified resume-and-answer handoff. It cannot launch another harness.

## Startup and ownership

Discover/map the nine active tables, Settings and Stop all. Curate runs first in a Run so later stages read current company evidence; a Partial Curate does not block independent Scan/Review/Prepare work. For Scan/Review resolve the current Career Goals revision and validate the corresponding preference set of extracted preferences/readiness under CAREER-GOALS.md; reuse one verified extraction within a full Run and refresh affected values if it changes. Record run-level read scope, not routine per-read events. Resolve goals/master/content as required and verify this harness's access/capabilities. Connections and local files are not inherited.

Resume one compatible released unfinished Run or create one. Pin instruction/input versions, owner and frozen scope. A full run uses one row with stage checkpoints; manual invocations use the same checkpoint format. Sources hold board cursors and Applications hold job state. Bounded Run segments handle oversized pending lists without truncation.

One active writer. Never seize an owner solely on timeout. Missing global access, Stop all or uncertain writes block affected work; item problems need not stop independent work. Legacy application controls are preserved but do not govern the retained stages.

## Company handoff and stage independence

A full Run starts with Curate's company/funding work; continue Scan and Review while independent research or discovery is blocked, keeping unfinished parts visible as Partial. Standalone stages read current Companies and saved Curate evidence without automatically launching Curate. Only human-Allow companies receive new inventory or automatic advancement. Recheck targeting at every write boundary. Respect any permanent block retained in a legacy base; new setups use Exclude for company exclusions. Employer application limits and cooldowns are outside the active workflow.

## Run checks: objective duplicate discovery

Every invocation, including a single stage command, starts with Run checks. Build one company-scoped identity index from live role IDs, official job links, role names and posted dates. Refresh this index when Scan encounters new postings. Run owns discovery; Review and later stages consume its result rather than repeating duplicate searches.

An exact verified employer role ID or verified posting-specific canonical link confirms identity. Role name and posted date corroborate it; they cannot alone prove identity. Preserve meaningful URL parameters. Different verified role IDs, regional postings or conflicting evidence need reconciliation rather than a title-based merge. Use scripts/stage_state.py:run_duplicate_match.

Reobserving an existing posting does not create another row or turn the canonical record into Duplicate. For confirmed redundant rows, retain the record with actual application history or authoritative human state as canonical; preserve submitted/rejected/interview outcomes. Do not modify protected historical records even if redundant; report the pair instead. Mark only an unprotected verified redundant record Duplicate, save duplicate_of, objective evidence and original values in History, and retain all notes and artifacts. Historical mirror copies require evidence that they describe the same application. An unresolved identity stays a Run question and cannot advance automatically. Do not delete or merge distinct submissions.

Use Duplicate evidence to improve reader identity/canonicalization and prevent repeated inserts. Do not learn career exclusions or title blacklists from it. Record checked counts, confirmed pairs, canonical IDs and unresolved cases in the Run checkpoint. DATA.md defines preservation and verification.

## Execute and persist

Use code for enumeration, normalization, identity, candidate filters, hashes and verification. Reuse verified unchanged inputs, but recheck authoritative versions and live gates at relevant boundaries. No unverified time-based freshness assumption, hidden page/item/time cap or false completion after one batch.

Scan inventories plausible candidates for the user's role family (Settings `role_family`) after keywords/basic semantics, including uncertain seniority for Review. Unknown identity remains a Run checkpoint; clear unrelated/junior failures produce aggregate counts. Review uses the three-step scoring frame in stages/review.md. Personal requirements come from current Career Goals; candidate facts come from the editable master. Career fit measures desired work; resume fit measures demonstrated suitability for the whole JD. Follow the numeric routing in stages/review.md, including Unresolved at zero; only a current qualifying score can advance to Prepare. Record review reason categories and follow stages/scan.md for validated improvements; do not learn career exclusions into Scan.

Preserve human outcomes. At every invocation capture new Feedback under DATA.md "Feedback inbox and Review eval" before stage decisions, and checkpoint capture again at completion. Once the eval case, snapshot and History are verified, clear only the unchanged captured Feedback. Feedback updates evals; it does not silently change Career Goals, stage rules or the role status. Do not reopen submitted/terminal roles when fit inputs change.

Reread affected state, reconcile human edits, write permitted deltas and verify actual persisted values/artifacts. Save meaningful changes/events and failed/uncertain writes in History under the run. Never hide unverified changes.

Applications retains current evidence/PDF references, current PDF version/verification and stage Run links. DATA.md stores exact stage metadata in History and fixed shared inputs in Runs. Content lives in registered Drive locations. Changed decision inputs require revalidation.

Review alone approves Queued (stages/review.md). Prepare produces the verified resume, inspects the official application questions and prepares approved/resolved answers under stages/prepare.md. It saves the evidence and stops at Ready; it does not fill forms, submit or monitor mail.

## Stage boundaries and exit

Save accepted stage outputs before advancing. Continue independent useful work safely, but blocked required stages/items mean Partial/Blocked. Verify every planned item and count before Complete. No work means verified empty eligible scope, not invented coverage.

Persist versions, outputs, pending identities/reasons, errors, next action and ownership release. Report Curate results (company/funding evidence, discovery feed coverage, Proposed companies awaiting the user), source coverage, transient rejects, plausible inventory, review-pending, verified eligible, approved queue and verified resumes separately. A new harness must recover this without prior chat/local state.

## Clarification rules

Every harness must ask concise, targeted questions when essential information is missing or contradictory. Users do not need to write agent instructions.

Before each stage check the requested scope, required tools, current source references and relevant preferences. Ask when ambiguity changes which roles are eligible, a hard career requirement, the resume's factual content or company targeting. State the uncertain fact, why it matters and which work can continue. Group related questions and do not ask again for an answer already provided.

Save the question, affected records, reason and next action in the Run. Wait for an answer before dependent work. Continue independent useful work. Do not treat elapsed time, silence, a missing salary or a blank preference as an answer. Unknown soft preferences can remain disclosed without blocking unrelated work. Use reasonable implementation choices for reversible details already within scope; do not ask permission for every step.

When the answer arrives, save the authorized preference/control change in its proper source, record History, refresh affected decisions and resume. If a goal changes, update preference data; if workflow behavior changes, update Git. Never silently write executable instructions into Career Goals.

If a tool or automatic approval review blocks an action, identify the exact action and stated reason. Finish independent work and present the concrete remaining approval or access requirement. Never call an incomplete stage Complete.

A stage handoff reports completed work, counts, unresolved questions, affected identities, next action and whether ownership was released. Missing global access/Stop all blocks affected work. A company-specific issue need not stop all companies.

## Six lifecycle states

| State | Meaning |
|---|---|
| Inventoried | Plausible role awaiting its first Review. |
| Need review | Review cannot confidently approve or reject it; Agent notes identifies the gap. |
| Queued | Current evidence-backed Review approval; eligible for Prepare. |
| Ready | Verified resume available; complete form inspection; every required answer Approved in Answer bank or Resolved in Application questions. Successful preparation endpoint. |
| Not pursuing | Review declined the role or it is outside current targeting. |
| Duplicate | Confirmed redundant unprotected row; canonical identity and prior values remain in History. |

Manual status changes are not acceptance evidence. Follow stages/review.md for the score routing. Revalidate only affected unprotected decisions when their inputs change; preserve human edits and do not redo valid Ready work without a relevant input change or an explicit request.

## Existing installations

Read nine active tables. Answer bank and Application questions are active for Prepare; reuse their current field IDs and preserve all existing answers/statuses. Preserve other extra columns, options, old controls and artifacts as inactive history. Setup never deletes or remaps them automatically. Legacy Needs answer, Applied, Interviewing and Rejected rows, and any row with a legacy submission attempt, are read-only for stage writers. Check both the retained row and resolved History metadata with scripts/stage_state.py:protected_history; a manual reset of the label does not erase an attempt. The feedback coordinator may still consume Feedback by the verified DATA.md procedure without changing the outcome.

An old Run whose plan contains removed stages is not a compatible run to resume. Preserve it, release its owner only after verifying no writer remains, and start a new four-stage Run referencing the old checkpoints. Reuse valid Scan/Review/resume evidence without fabricating completion or launching later work. Older Ready resumes do not establish answer readiness: inspect the form and verify current answers before reusing an unsubmitted Ready handoff, while preserving the resume. Do not delete live columns or existing external automations as part of routine startup; report any out-of-repo automation that needs the user's attention.

## First full run after an input change

Refresh affected goal-derived criteria before Run checks. Read Settings.role_policy.revalidation_pending and the Run checkpoint; include affected unprotected Ready/Queued approvals in Review before reusing them. Preserve their PDFs and prior decisions. Re-review only affected declined roles, not every historical Not pursuing row. A settings refresh schedules revalidation; it does not manufacture a current approval or change lifecycle by itself.

Curate reports Proposed companies for one human Allow/Exclude checkpoint. Existing Allow companies can continue independently. Newly discovered companies enter Scan only after the human's choices are saved and verified. Checkpoint if the user is absent; never auto-Allow. Missing earlier submission dates/PDFs block only the affected company's resume consistency check; retain exact questions in the Run and continue independent roles.
