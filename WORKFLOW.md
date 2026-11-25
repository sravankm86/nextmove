# Workflow and lifecycle

Read AGENTS.md and the requested stage. Load reference docs only when needed, and keep bulk catalogs/verification of saved values outside model context.

| Command | Scope |
|---|---|
| Run / Run Nextmove | Default single agent: Curate → Scan → Review → Prepare (ends at Ready) |
| Curate / Companies | Refresh company/funding evidence; on cadence propose matching companies new to the list as Proposed. Never sets Allow/Exclude |
| Scan | Derive broad role criteria from current goals; complete source coverage and basic semantics → Inventoried; no career-fit assessment |
| Review / Assess / Shortlist | Inventoried/Need review → JD extraction, career fit and resume fit scores → Queued, Need review or Not pursuing |
| Prepare | Queued roles, including human choices, plus earlier Needs answer roles and Ready roles that have never had an answer check → reuse a fully covering approved base or tailor from the closest base under the resume guidelines → verified resume and approved/resolved required answers → Ready, Needs answer or Apply manually |
| Submit applications | Explicit-only; never part of Run. Ready roles whose live Prepare checks still pass → fill approved answers, upload the verified resume and approved files, submit once, save proof → Applied, or Apply manually with the reason under [stages/submit.md](stages/submit.md) |
| Sanitize / Sanitize Nextmove | Explicit-only repository consistency and simplification under [Maintenance](docs/MAINTENANCE.md#sanitize-explicit-only); never a production stage |
| Review eval / Eval Review | Capture feedback, prepare frozen label-free inputs, run a fresh blind Review and score it under DATA.md; no production decisions change |
| Capture feedback | Move feedback into verified eval cases and clear only the captured unchanged notes; no role decisions |

Match command aliases as complete phrases: Review eval / Eval Review is an Experiment, not production Review.

Quoted examples/setup discussions do not dispatch work. Sanitize requires an explicit request; Run, stage commands, setup, retries, feedback and schedules never imply it. Read its maintenance procedure instead of loading production-stage prerequisites. A single stage stops after handoff. Run advances authorized useful stages without asking to continue, and stops at the verified resume-and-answer handoff. It cannot launch another harness.

## Startup and ownership

Discover/map the seven active tables, Settings, Stop all and Active writer. Curate runs first in a full Run so later stages read current company evidence; a Partial Curate does not block independent Scan/Review/Prepare work. For Scan/Review resolve the current Career Goals revision and validate the corresponding preference set of extracted preferences/readiness under CAREER-GOALS.md; reuse one verified extraction within a full Run and refresh affected values if it changes. Log the start and finish of each command in the Audit log, not routine reads. Resolve goals/master/content as required and verify this harness's access/capabilities. Connections and local files are not inherited.

There is no run record to resume: lifecycle statuses, each role's evidence and each company's Last scanned show what is done and what is left, so an interrupted command simply continues from the live rows. Work through long lists in batches without truncating them.

One active writer, claimed in Settings Active writer (DATA.md "Audit log and integrity"). Never take it over on age alone. Missing global access, Stop all or uncertain writes block affected work; item problems need not stop independent work. Legacy application controls are preserved but do not govern the retained stages.

## Company handoff and stage independence

A full Run starts with Curate's company/funding work; continue Scan and Review while independent research or discovery is blocked, keeping unfinished parts visible as Partial. Standalone stages read current Companies and saved Curate evidence without automatically launching Curate. Only human-Allow companies receive new inventory or agent queue admission; check targeting at those write boundaries and respect legacy permanent blocks. New setups use Exclude for company exclusions. Prepare follows the queue decision below. Employer application limits and cooldowns are outside the active workflow.

## Queue decisions

Queued authorizes Prepare, whether set by Review, by a human in Airtable or by an agent following the user's explicit request (recorded verbatim). Agents apply all career-fit, resume-fit, pay, seniority and company gates before queueing under stages/review.md. A human's Queued choice overrides an earlier fit decision for that role; no extra approval field or receipt is required. Preserve the scores and earlier assessment, and record the observed queue handoff without inventing an editor or edit time.

Prepare trusts Queued, rechecks Needs answer retries and gives Ready roles that have never had an answer check that check. It does not repeat fit or company admission checks, demand a matching Review approval, or reject unresolved salary/seniority. Goal or fit-policy changes affect future agent queue admissions; they do not automatically reopen Queued, Needs answer, Ready or Apply manually roles. To reassess one, explicitly request Review or move it back to Need review. Changing company targeting alone does not cancel an existing queue decision.

Stop all, writer ownership, objective identity and protected submission history still apply. Queued authorizes the work; Ready still requires the verified resume and required answers.

## Run checks: objective duplicate discovery

Every production, feedback or eval invocation, including a single stage command, starts with Run checks. Sanitize is exempt: its maintenance procedure can run without a private base. Build one company-scoped identity index from live role IDs, official job links, role names and posted dates. Refresh this index when Scan encounters new postings. Run owns discovery; Review and later stages consume its result rather than repeating duplicate searches.

An exact verified employer role ID or verified posting-specific canonical link confirms identity. Role name and posted date corroborate it; they cannot alone prove identity. Preserve meaningful URL parameters. Different verified role IDs, regional postings or conflicting evidence need reconciliation rather than a title-based merge. Use scripts/stage_state.py:run_duplicate_match.

Reobserving an existing posting does not create another row or turn the canonical record into Duplicate. For confirmed redundant rows, retain the record with actual application history or authoritative human state as canonical; preserve submitted/rejected/interview outcomes. Do not modify protected historical records even if redundant; report the pair instead. Mark only an unprotected verified redundant record Duplicate, save duplicate_of, objective evidence and original values in the Audit log, and retain all notes and artifacts. Historical mirror copies require evidence that they describe the same application. An unresolved identity is logged as an open question and cannot advance automatically. Do not delete or merge distinct submissions.

Use Duplicate evidence to improve reader identity/canonicalization and prevent repeated inserts. Do not learn career exclusions or title blacklists from it. Record checked counts, confirmed pairs, canonical IDs and unresolved cases in the Audit log. DATA.md defines preservation and verification.

## Execute and persist

Use code for enumeration, normalization, identity, candidate filters, hashes and verification. Reuse verified unchanged inputs, but recheck authoritative versions and live gates at relevant boundaries. No unverified time-based freshness assumption, hidden page/item/time cap or false completion after one batch.

Scan inventories plausible candidates for the user's role family (Settings `role_family`) after keywords/basic semantics, including uncertain seniority for Review. Unknown identity is logged as an open question; clear unrelated/junior failures produce aggregate counts. Review uses the three-step scoring frame in stages/review.md. Personal requirements come from current Career Goals; candidate facts come from the editable master. Career fit measures desired work; resume fit measures demonstrated suitability for the whole JD. Agents queue only under the current numeric routing, including Unresolved at zero; the queue decision above governs Prepare. Record review reason categories and follow stages/scan.md for validated improvements; do not learn career exclusions into Scan.

Preserve human outcomes. At every invocation capture new Feedback under DATA.md "Feedback inbox and Review eval" before stage decisions, and checkpoint capture again at completion. Once the eval case, snapshot and Audit log entry are verified, clear only the unchanged captured Feedback. Feedback updates evals; it does not silently change Career Goals, stage rules or the role status. Do not reopen submitted/terminal roles when fit inputs change.

Reread affected state, reconcile human edits, write permitted deltas and verify actual persisted values/artifacts. Log meaningful changes, decisions and failed/uncertain writes in the Audit log. Never hide unverified changes.

Applications retains current evidence/PDF references, current PDF version/verification and the role's stage evidence (Evidence (JSON), including the input versions each decision used); the Audit log records every change. Content lives in registered Drive locations. Check current fit inputs before agent queue admission; check current master, guidelines, JD, PDF and answers when preparing or reusing a Ready handoff.

Review owns agent queue admission (stages/review.md); humans may queue directly. Prepare produces the verified resume, inspects the official application questions and prepares approved/resolved answers under stages/prepare.md. It saves the evidence and stops at Ready; it does not fill forms, submit or monitor mail. Only the explicit Submit command submits, under stages/submit.md.

## Stage boundaries and exit

Save accepted stage outputs before advancing. Continue independent useful work safely, but blocked required stages/items mean Partial/Blocked. Verify every planned item and count before Complete. No work means verified empty eligible scope, not invented coverage.

Persist versions, outputs, pending identities/reasons, errors and next action in the finish-of-command Audit log entry, then clear Active writer. Report Curate results (company/funding evidence, discovery feed coverage, Proposed companies awaiting the user), source coverage, transient rejects, plausible inventory, review-pending, verified eligible, approved queue and verified resumes separately. A new harness must recover this without prior chat/local state.

## Clarification rules

Every harness must ask concise, targeted questions when essential information is missing or contradictory. Users do not need to write agent instructions.

Before each stage check the requested scope, required tools, current source references and relevant preferences. Ask when ambiguity changes which roles are eligible, a hard career requirement, the resume's factual content or company targeting. State the uncertain fact, why it matters and which work can continue. Group related questions and do not ask again for an answer already provided.

Save the question, affected records, reason and next action in the Audit log. Wait for an answer before dependent work. Continue independent useful work. Do not treat elapsed time, silence, a missing salary or a blank preference as an answer. Unknown soft preferences can remain disclosed without blocking unrelated work. Use reasonable implementation choices for reversible details already within scope; do not ask permission for every step.

When the answer arrives, save the authorized preference/control change in its proper source, log it in the Audit log, refresh affected decisions and resume. If a goal changes, update preference data; if workflow behavior changes, update Git. Never silently write executable instructions into Career Goals.

If a tool or automatic approval review blocks an action, identify the exact action and stated reason. Finish independent work and present the concrete remaining approval or access requirement. Never call an incomplete stage Complete.

A stage handoff reports completed work, counts, unresolved questions, affected identities, next action and whether ownership was released. Missing global access/Stop all blocks affected work. A company-specific issue need not stop all companies.

## Nine lifecycle states

| State | Meaning |
|---|---|
| Inventoried | Plausible role awaiting its first Review. |
| Need review | Review cannot confidently approve or reject it; Agent notes identifies the gap. |
| Queued | Authorized for Prepare by Review or a human's direct choice. |
| Ready | Verified resume available; complete form inspection; every required answer grounded in the current master, role resume or Career Goals, or Approved in Answer bank or Resolved in Application questions. Successful preparation endpoint. |
| Needs answer | Prepare could not finish: the resume is not yet verified, or a required answer or attachment is missing or not yet approved (an unticked Answer bank row or an Application questions row that is not Resolved). Agent notes says whether the next step is the user's (provide or approve something) or the agent's own retry (for example a failed render). Every Prepare run rechecks these roles and moves them to Ready once everything passes. |
| Apply manually | The resume is verified, but no agent could open or fully read the official application (for example sign-in or account creation, a bot check, a blocked host, a broken Apply link or a required assessment). The user starts this application themselves. Submit also ends here on any failure, with the reason and, if Submit may have been clicked, a warning to check before applying again. Neither stage retries it unless asked. |
| Applied | Submit clicked Submit once and saved verified confirmation proof under stages/submit.md. Read-only afterwards; later tracking is separate. |
| Not pursuing | Review declined the role or it is outside current targeting. |
| Duplicate | Confirmed redundant unprotected row; canonical identity and prior values remain in the Audit log. |

Manual Queued authorizes Prepare; manual Ready does not prove that the resume and answers were verified. Follow stages/review.md for agent score routing and Queue decisions above for reassessment. Preserve human edits and do not redo valid Ready work without a relevant resume/answer input change or an explicit request.

## Existing installations

Read seven active tables. Answer bank and Application questions are active for Prepare; reuse their current field IDs and preserve all existing answers/statuses. Preserve other extra columns, options, old controls and artifacts as inactive history. The retired Role eligibility flag is preserved but is no longer read or written: Queued is the preparation handoff. Setup never deletes or remaps legacy fields automatically. Applied rows (legacy or from Submit), Interviewing and Rejected rows, and any row with a legacy submission attempt, are read-only for stage writers; Submit writes Applied only with verified proof. Needs answer is an active Prepare state again; existing Needs answer rows are rechecked by the next Prepare run. Check both the retained row and its evidence with scripts/stage_state.py:protected_history; a manual reset of the label does not erase an attempt. The feedback coordinator may still consume Feedback by the verified DATA.md procedure without changing the outcome.

Bases created before the seven-table model keep their Runs, Sources and History tables as read-only history. Migrate once: copy each company's board URLs into Careers URLs and rename History to Audit log. Role evidence migrates on first touch: when a role's Evidence (JSON) is empty, build it with `scripts/stage_state.py:legacy_evidence` from that role's old snapshots in the Audit log and the archived Runs, save and read it back, log the migration, then continue. Keep Runs and Sources read-only until no active role still needs them; export them to Audit trail before retiring them under docs/MAINTENANCE.md. Reuse valid Scan/Review/resume evidence without fabricating completion or launching later work. Older Ready resumes do not establish answer readiness: Prepare selects Ready roles without a saved answer check (`scripts/stage_state.py:answer_check_due`), inspects the form and verifies current answers, keeping Ready only if everything passes and preserving the resume. Do not delete live columns or existing external automations as part of routine startup; report any out-of-repo automation that needs the user's attention.

## First full run after an input change

Refresh affected goal-derived criteria before new Curate, Scan and Review decisions. Read Settings.role_policy.revalidation_pending for unqueued roles; re-review only affected declined roles, not every historical Not pursuing row. Existing Queued, Needs answer, Ready and Apply manually roles follow Queue decisions above and are reassessed only on explicit request. Preserve their PDFs and prior scores. A changed master, guidelines or JD requires the relevant resume checks again, not another fit approval; a settings refresh never changes lifecycle by itself.

Curate reports Proposed companies for one human Allow/Exclude checkpoint. Existing Allow companies can continue independently. Newly discovered companies enter Scan only after the human's choices are saved and verified. Checkpoint if the user is absent; never auto-Allow. Missing earlier submitted resumes or dates do not block Prepare: use a current approved base or tailor, while preserving historical submissions. A master update governs future resume work, not a retrospective audit of submitted files.
