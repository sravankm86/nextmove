# Workflow and lifecycle

Read AGENTS.md and the requested stage. Load reference docs only when needed, and keep bulk catalogs/verification of saved values outside model context.

| Command | Scope |
|---|---|
| Run / Run Nextmove | Default single agent: Scan → Review → Prepare → Apply → Track (ends at Interviewing) |
| Scan | Derive broad role criteria from current goals; complete source coverage and basic semantics → Inventoried; no career-fit assessment |
| Review / Assess / Shortlist | Inventoried/retryable backlog → full eligibility/career/resume assessment → Queued |
| Prepare | Current review-approved Queued roles |
| Apply | Ready roles without unresolved attempts; preflight unless separately authorized |
| Track | Exact-role mail/receipt reconciliation from checkpoint |

Quoted examples/setup discussions do not dispatch production work. A single stage stops after handoff. Run advances authorized useful stages without asking to continue, but cannot infer submission permission or launch another harness.

## Startup and ownership

Discover/map the six tables, Settings and live controls. For Scan/Review resolve the current Career Goals revision and validate the corresponding preference set of extracted preferences/readiness under CAREER-GOALS.md; reuse one verified extraction within a full Run and refresh affected values if it changes. Record run-level read scope, not routine per-read events. Resolve goals/master/content as required and verify this harness's access/capabilities. Connections and local files are not inherited.

Resume one compatible released unfinished Run or create one. Pin instruction/input versions, owner and frozen scope. A full run uses one row with stage checkpoints; manual invocations use the same checkpoint format. Sources hold board cursors and Applications hold job state. Bounded Run segments handle oversized pending lists without truncation.

One active writer. Never seize an owner solely on timeout. Missing global access, Stop all or uncertain writes block affected work; item problems need not stop independent work. Submission pause affects Apply, not useful Scan/Review/Prepare/Track work.

## Execute and persist

Use code for enumeration, normalization, identity, candidate filters, hashes and verification. Reuse verified unchanged inputs, but recheck authoritative versions and live gates at relevant boundaries. No unverified time-based freshness assumption, hidden page/item/time cap or false completion after one batch.

Scan inventories plausible PM candidates after keywords/basic semantics, including uncertain seniority for Review. Unknown identity remains a Run checkpoint; clear unrelated/junior failures produce aggregate counts. Review alone verifies final eligibility, qualifications, private resume-fit exclusions and career/resume fit before Queued. Apply requires resolved role-specific base pay; an explicit salary-only provisional queue can proceed to Prepare. Record review reason categories and follow stages/scan.md for validated improvements; do not learn career exclusions into Scan.

Preserve human outcomes/notes. Read Manual notes and current status under DATA.md before processing and writing a job; record newly observed feedback in the stage snapshot/History without rewriting the notes. Legacy Queued rows require explicit current review evidence, not automatic certification. Do not reopen submitted/terminal roles when fit inputs change.

Reread affected state, reconcile human edits, write permitted deltas and verify actual persisted values/artifacts. Save meaningful changes/events and failed/uncertain writes in History under the run. For bounded migration batches, exact per-record private delta artifacts can be indexed by a verified History manifest; never hide unverified changes.

Applications retains current evidence/PDF references, current PDF version/verification and stage Run links. DATA.md stores exact stage metadata in History and fixed shared inputs in Runs. Content lives in registered Drive locations. Schema-only releases retain decision-policy versions; changed decision inputs still require revalidation. A vanished local reader is a recovery gap, not evidence of incremental support.

Review owns final eligibility/hard career checks and approves Queued; Prepare requires its current acceptance evidence. A base PDF requires factual/current/visual verification; a URL does not mean Ready. Before Submit persist unique attempt identity and exact resume version. Require explicit scope, answers, an accessible actual application form, restrictions and live controls; capture receipt or uncertainty. Never blind-retry, and never infer non-submission from missing mail.

## Stage boundaries and exit

Save accepted stage outputs before advancing. Continue independent useful work safely, but blocked required stages/items mean Partial/Blocked. Verify every planned item and count before Complete. No work means verified empty eligible scope, not invented coverage.

Persist versions, outputs, pending identities/reasons, errors, next action and ownership release. Report source coverage, transient rejects, plausible inventory, review-pending, verified eligible, approved queue and later outcomes separately. A new harness must recover this without prior chat/local state.

Use the 28-column tracker under DATA.md. Write concise current context and next action in Agent notes; never overwrite Manual notes. Resolve explicit review checks and structured feedback from History. Sources remains board-level scanner state, not an Applications field. Do not require posting availability during Scan/Review or maintain Last seen at; check the real form during Apply.

## Clarification rules

Every harness must ask concise, targeted questions when essential information is missing or contradictory. Users do not need to write agent instructions.

Before each stage check the requested scope, required tools, current source references and relevant preferences. Ask when ambiguity changes which roles are eligible, a hard career requirement, the resume's factual content, application answers, submission authorization or a company restriction. State the uncertain fact, why it matters and which work can continue. Group related questions and do not ask again for an answer already provided.

Save the question, affected records, reason and next action in the Run. Wait for an answer before dependent work. Continue independent useful work. Do not treat elapsed time, silence, a missing salary or a blank preference as an answer. Unknown soft preferences can remain disclosed without blocking unrelated work. Use reasonable implementation choices for reversible details already within scope; do not ask permission for every step.

When the answer arrives, save the authorized preference/control change in its proper source, record History, refresh affected decisions and resume. If a goal changes, update preference data; if workflow behavior changes, update Git. Never silently write executable instructions into Career Goals.

If a tool or automatic approval review blocks an action, identify the exact action and stated reason. Finish independent work and present the concrete remaining approval or access requirement. Never call an incomplete stage Complete.

A stage handoff reports completed work, counts, unresolved questions, affected identities, next action and whether ownership was released. Missing global access/Stop all blocks affected work. A company-specific issue need not stop all companies. See WORKFLOW.md and DATA.md.

## Seven lifecycle states

| State | Meaning and next action |
|---|---|
| Inventoried | Scan admitted a plausible PM role. Review is pending, incomplete or waiting for evidence. |
| Queued | Review explicitly approved current qualifications, exclusions, eligibility and fit. Only base-pay verification may be explicitly deferred; Prepare is next and Apply remains blocked until resolved. |
| Ready | The grounded resume/PDF is verified. Apply may perform preflight; submission needs separate authorization. |
| Applied | The human reported or the agent established submission. Confirmation is additional evidence, not a new state. |
| Interviewing | Active recruiter engagement, screening, assessment, interview or scheduling. This is the endpoint of Nextmove's recruiting lifecycle. |
| Not pursuing | Review declined the role or the human chose to stop. Store the precise reason/category in History and a short explanation in Agent notes. |
| Rejected | Employer rejection received before the Interviewing endpoint. Record the actual event and applicable company restriction separately. |

The successful path is Inventoried → Queued → Ready → Applied → Interviewing. Not pursuing and Rejected are early exits. Offer, acceptance, negotiation, onboarding and outcomes after Interviewing are outside automatic tracking scope. Once a row reaches Interviewing, Track no longer polls it for later outcomes. Known later facts explicitly supplied by the user may be recorded as History/company restriction evidence without extending this lifecycle. This narrower scope does not guarantee complete post-interview rejection knowledge; Apply must still resolve any applicable company restriction before submission.

Only Scan admits new candidates; only Review approves Queued. A manually selected status is not review evidence, PDF verification or submission permission. Do not reopen submitted/terminal records merely because criteria change.

Missing information stays at the last justified stage with a specific next action in Agent notes and durable pending state. A blocked Inventoried role is not automatically reviewed repeatedly: retry when its missing evidence/input changes or the user requests it. A company cooldown does not lower fit or undo review approval.

An uncertain Submit stays at its last verified pre-submission stage, normally Ready, with a prominent uncertainty note and saved attempt identity/outcome. Never label an unverified resume Ready or claim Applied without evidence. The outstanding attempt blocks another Submit regardless of manual status resets; reconcile it first. Hold other work that could obscure the outstanding attempt and its exact submitted PDF.

Keep confirmations in Confirmation reference and History, eligibility in Role eligibility, independent fit ratings in Career fit/Resume fit, and reasons in review metadata/Agent notes. Neither High fit axis overrides a hard career contradiction, confirmed qualification failure or essential resume mismatch under the applicable assessment path. Explicit general senior PM preferences use the bounded exception in stages/review.md; unproven experience is never a resume fact. Only base pay can be explicitly deferred for provisional preparation. Review-owned career rejections are not automatic scan exclusions.

## Existing status migration

Preserve exact prior status, notes, timestamps, evidence and outcome in History before migration. Needs review/Needs eligibility become Inventoried; Confirmed becomes Applied with confirmation evidence retained; In process becomes Interviewing; Not aligned/Not a fit/Withdrawn/Closed/Duplicate become Not pursuing with distinct reasons retained. Shortlisted becomes Queued only with current explicit approval, otherwise Inventoried. Offer/Accepted become Interviewing for this tracker, while actual historical outcomes remain in History. Submission uncertain uses the last verified pre-submit stage plus a durable blocking attempt, never inferred success. Existing legitimate Queued/Ready/Applied/Rejected outcomes keep their evidence and safeguards.

Map and verify every record before removing old select choices. Never silently discard confirmation, duplicate relationships, employer rejection triggers or uncertainty. If the connector cannot manage choices, provide the exact Airtable UI action and keep migration marked incomplete. Existing aliases are for reading/recovery, not permission to emit obsolete states.
