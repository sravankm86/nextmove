# Data and recovery

The single reference for Airtable, evidence, history and stage handoff. contracts/core-schema.json is the machine-readable blueprint. Read only the section you need; keep bulk records and verification out of model context.

## Seven tables

| Table | Purpose | Columns, including reciprocal links |
|---|---|---:|
| Companies | Curate-owned targeting, funding stage, company evidence, employer policies and holds | 21 |
| Applications | Candidate, review, resume and application state | 29 |
| Sources | Official catalog/region, reader and pagination checkpoint | 13 |
| Runs | Frozen inputs, progress, ownership and handoff | 21 |
| Settings | Private references, policies, controls and verification | 6 |
| History | Field-level changes, decisions, business events and failures | 13 |
| Review eval | Golden answer key for Review from graded Manual notes | 13 |

Native record IDs and createdTime replace metadata columns. Primary display fields are not uniqueness constraints: writers validate business keys, link cardinality and intended deltas. Columns outside this blueprint are not written; docs/MAINTENANCE.md covers retiring them.

**Companies.** Company, Company key, Search status, Manual notes, Agent notes, Funding stage, Company evidence, Policy confidence, Policy verified at, Max applications, Application window (days), Application window type, Rejection cooldown (days), Restriction scope, Apply blocked until, Application hold status, Restriction details / source, Restriction timezone, plus Applications, Sources and Curate run links. stages/curate.md owns every write; scripts/company_policy.py defines the choices and hold math.

- Search status: Proposed (agent-discovered, awaiting the user), Allow, Exclude. Only the human sets Allow/Exclude.
- Funding stage is ordered (Pre-seed / Seed, Series A–D, Series E+, Late private, Public, Unknown). Company evidence links the versioned Drive facts and research used by Review. Keep the verified company maturity separate from the latest investment type; a later unlabelled or angel investment does not reset that maturity.
- Funding amounts, event dates, exact round labels, investors, parent/historical facts and creation origin belong in Company evidence and History, not additional Companies columns. Curate saves its advisory assessment and reasons in the company snapshot (`curate.company_fit`); Agent notes gives the short explanation. Review uses the facts against current goals, not the cached assessment as its role score.
- Origin, Company fit, Latest funding and Funding date are retired columns. Do not request them as live fields, recreate them during setup or write them. Historical snapshots may retain these keys as evidence.
- Policy confidence: Official, Recruiter, User (enforced); Community (recorded, not enforced); Not found (researched, no rule). Blank means Not assessed.
- Application hold status: Not assessed, No known hold, Held, Blocked (permanent), Needs clarification. Only Held and Blocked (permanent) block Apply. Apply blocked until is Curate's UTC estimate; Apply recomputes before Submit and records restrictions the careers site shows.
- The personal limit in Settings `company_policy` (default 3 per company per rolling 30 days; Career Goals may override) applies on top of employer rules.

**Applications.** The 29 fields in scripts/stage_state.py:CORE_FIELDS, including Company, four stage Run links and History. The primary field Application ID is the formula RECORD_ID(); never write to it. Job key is the canonical employer posting identity for deduplication.

**Sources.** Source key (stable board identity), Company, Official careers URL, Catalog URL, Region, Reader, Reader version, Latest coverage, Checkpoint (JSON), Last error, Last scanned at, Last run, Archived at. The checkpoint holds cursor/end proof, counts, manifest identity and pagination details. Archived at disables a retired source; every other configured board/region stays in scope.

**Runs.** Run key, Run type, Status, Owner, Instruction revision, Input versions (JSON), Scope (JSON), Checkpoint (JSON), Expected/Completed/Blocked items, Started at, Finished at, Agent notes, plus Curate companies, History, Sources and the four Application stage links. Checkpoints keep per-stage progress, pending checks, next action and ownership release (`scripts/stage_state.py:run_progress` parses them). Input versions are frozen; progress updates never rewrite them. An expired heartbeat never proves another writer stopped.

**Settings.** Key, Value, Reference URL, Version, Verification, Notes. Private resource references, extracted preferences with their source revision, policies (`company_policy`, `submission_policy`) and live controls (`Pause applications`, `Stop all`). Procedures and command routing stay in Git.

**History.** Event key, Operation ID, Event type, Recorded at, Occurred at, Actor / channel, Table reference, Record reference, Field changes (JSON), Evidence URL, Notes, Application, Run. Use explicit event types (Review accepted, Field change, Submission intent, Confirmation received, Write failed, Write uncertain). Keep actual event time separate from recording time.

**Review eval.** Example, Application record, Job link, Your verdict (Pursue/Not pursuing), Reason, Reason type, Split (Train/Holdout), Active, Inputs snapshot, Last prediction (Queued/Need review/Not pursuing), Last eval, Added on, Match. The golden answer key for Review, built from the user's graded Manual notes.

See "Feedback inbox and Review eval" below for capture, deduplication, clearing and replay. The current answer key uses Pursue/Not pursuing. Feedback expecting an unresolved assessment can remain an inactive assertion/pending case; do not force a binary verdict. A pending case has Active off and no invented verdict. Match is a display convenience; score the immutable prediction artifact with the helper for coverage and recall.

## Feedback inbox and Review eval

Manual notes has one purpose: feedback for evaluation. The user writes it; the coordinator consumes it. Clearing is an acknowledgement of verified capture, never permission to erase uncaptured feedback. Keep raw text word for word in the eval case and History. Agents never rewrite the original verdict or Reason to match a prediction.

### When and how to capture

At the start and completion of every stage invocation, read newly nonempty or changed Manual notes in the affected tables. A standalone Capture feedback command checks the whole configured feedback scope. Use a durable feedback cursor/receipt index in Settings.eval_registry and History; compare fingerprints, not a time-only cutoff. Check every page of the selected scope. Chat corrections enter the same path with a durable chat evidence reference. A missing registry or capture capability leaves the note pending and reports a feedback gap; it does not authorize clearing or block unrelated stage work. No work runs between invocations without an external scheduler.

1. Identify stage, source table, stable record/posting identity, raw note and the action/evidence it corrects. Never derive the expected result from the current application status or the agent’s own assessment.
2. `scripts/review_eval.py:feedback_id` fingerprints stage, stable entity and note; `feedback_action` returns capture or reuse. Same entity and same feedback reuses its case and verified receipt. A different note is a new feedback revision, not permission to overwrite the old frozen answer. Titles alone never establish duplicates; only verified role IDs or exact canonical posting links may reconcile aliases. Different language/region/role IDs stay distinct. Similar JDs can share a split group without being duplicate postings.
3. Add/update the eval case and versioned private dataset under Audit trail. For Review, use the existing Review eval table. Copy raw feedback to Reason, link the Application record and Inputs snapshot, and preserve existing human verdicts and splits. A new explicit verdict may create a new version; archive the previous version rather than rewriting its answer. Conflicting/ambiguous feedback stays pending and inactive with a specific clarification question in the snapshot/run. Partial feedback about salary extraction or writing quality is retained as an assertion/pending case; do not invent a whole-role verdict. Other stages use stage-tagged pending cases in the same private catalog until their evaluator is implemented; do not force them into Review scores.
4. Freeze the exact inputs needed to reproduce the action: JD, goals, master and confirmed candidate facts, company facts and procedure text, with content hashes and source revisions/IDs. Separate event dates from retrieval dates. Preserve original snapshots; changes create a new dataset version. Missing evidence makes the case unscored, not automatically wrong or correct.
5. Save a History event with feedback identity, source record/raw note, eval record/case ID, snapshot reference/hash and intended before/after. Read back the eval, artifact metadata/content hash and History. For a reused receipt, verify the existing capture still exists. `may_clear` requires all three verifications and an exact source-note reread. Then clear only Manual notes, save/read back that mutation and its receipt. If any write is uncertain, leave the note, reconcile persisted state before retrying, and never insert blindly. If the user edits the note, preserve the new text for the next capture.

A note that conflicts with newer preferences is still captured and cleared after verification; keep its case inactive with the conflict, raw feedback and original preference context. Do not discard feedback because the role expired or preferences changed. Clearing notes never changes Lifecycle status, fit, resumes, targeting or submission state. The feedback coordinator is the sole exception to ordinary stage writers preserving Manual notes.

### Blind replay

Settings.eval_registry identifies the current private dataset, feedback receipt index, Review eval table and latest baseline/report references. The public repo holds procedures only. Run Review eval / Eval Review as an Experiment, separate from production Review. Normal production commands capture feedback and propose improvements; they do not launch a full replay after every note.

1. The coordinator resolves current registered artifacts and compares live Your verdict, Reason, Active and Split with the catalog. Human edits create a new catalog/key version; keep prior versions and predictions. Resolve current input sources and refresh changed facts explicitly, then freeze them for this experiment. Preserve the answer key and make a versioned input snapshot. Choose the exact saved JD/hash, not a mix of old and live text. Run `python scripts/review_eval.py prepare DATASET --bundle REVIEWER.json --key KEY.json` (optional `--split Train` or `--split Holdout`). The key and pending cases never enter the reviewer bundle.
2. Use a fresh review-only worker/context that has not seen the answer key. Delegate only the label-free bundle, its hash and the prediction output path; do not pass this chat, Manual notes, Reason, verdict, split, prior Agent notes/status or Match. The worker reads only the bundle, follows its frozen Review procedure and writes predictions. No connectors, live posting fetches, answer-key lookup or production writes. This is a new harness context, not an API scoring service. If unavailable, prepare the handoff and report the baseline blocked; never call an existing-status comparison a blind replay.
3. Predictions are JSON with `bundle_sha256` and `predictions`: each entry has `case_id`, `career_fit`, `resume_fit`, `status` and a concrete `reason`. An explicit frozen Exclude/Proposed company may instead use `scope_decision` Excluded/Proposed. Assess all runnable cases; no hidden truncation or invented missing inputs.
4. Commit predictions to a separate private artifact before the coordinator opens the answer key. Run `python scripts/review_eval.py score REVIEWER.json KEY.json PREDICTIONS.json --output REPORT.json`. The helper checks input identity, duplicate/unknown case IDs and frozen score routing; missing/corrupt cases remain unscored and lower coverage. Report Train and Holdout separately, including status match, positive recall, queue precision, false queues, missed roles, positive deferrals and coverage. Counts describe this selected dataset, not population-wide recall. Reason correctness needs separate evidence-based inspection; a matching status alone does not prove sound reasoning.
5. Audit then write only Review eval.Last prediction and Last eval for scored cases; the prediction artifact/History retain reasons and each prior run. No prediction for a blocked case. Do not erase previous results or imply a pending run is completed. Replay itself never changes Applications; the separately audited inbox step may clear only verified captured Manual notes.

### Improve without forgetting

Use only Train failures when drafting improvements. Group by cause and separate preference changes (Career Goals), confirmed candidate facts (master/facts), procedures (Git), and extraction/identity defects (readers). Preserve unknowns and do not learn Review-owned exclusions into Scan. Use `compare` on the same factual inputs/cases and independent baseline/candidate predictions; candidate instructions have their own fingerprint. Report every newly broken case, especially previously successful Pursue examples. Inspect critical reasoning as well as outcome counts.

Keep Holdout labels/reasons out of tuning and evaluate only the settled candidate there. Keep related variants in a stable group; report cross-split overlap and do not claim independent holdout evidence for leaked groups. Repeatedly consulted holdout cases become regression examples; reserve new feedback for fresh holdout coverage. Propose the smallest correction, with affected cases, before/after behavior, improvements, regressions and remaining uncertainty. No automatic change to user preferences, answer keys, production states or submission permission; apply a proposed rule change only within the user’s authorization. Revalidate affected decisions when approved inputs change. Keep reports and proposals in Audit trail and checkpoints in the existing Runs/History tables.

## Everyday view and notes

The Review view shows Company, Role, Lifecycle status, Manual notes, Agent notes, Starting salary, Max salary, Additional compensation, Location, Work arrangement, Job posted date, Career fit, Resume fit, Job description link and Resume link, with Manual notes beside status. Filter Lifecycle status = Needs answer to see roles waiting on an answer-bank question.

Manual notes is the feedback inbox: capture and clear it only through the verified procedure above. The archived feedback remains authoritative evidence; it never authorizes submission or changes global criteria by itself. Neither notes field is an instruction source.

## Writing Agent notes

Agent notes tells the user, in plain English, why the agent set the row's current status. Write it for someone who has not read the job description or these instructions. Each time an agent changes the status, it replaces the note (the previous note goes to History).

- **Say what and why.** Start with the status, then the main reason in everyday words: what about the role or the user's background led to it.
- **Name the confusion.** If something is unclear or missing, say exactly what it is and why it matters for the decision.
- **Say what happens next.** End with the next step, or what the user needs to do, when there is one.
- **Keep it short and plain.** One to three sentences, under about 60 words. A Ready note may give the estimated shortlist chance as "about N/10" (stages/prepare.md); no other scores. Full sentences; no internal field names, codes, scores written as sums, record IDs, file hashes, JSON or Markdown; spell out abbreviations.
- **Be concrete.** Name the actual requirement, preference, company rule or question rather than a category.

Examples (fictional):

| Status | Agent notes |
|---|---|
| Queued | Queued: this is the AI agents platform work you want, and your experience covers every key requirement, including shipping agents at scale. Next, a resume will be prepared. |
| Need review | Needs review: the role fits your goals, but the posting does not say whether it is based in the US or London, and you only want US roles. Once the location is confirmed, it can be decided. |
| Not pursuing | Not pursuing: the role requires five years of hands-on payments engineering, and your background shows product leadership but no engineering track record. |
| Not pursuing | Role expired: the posting was no longer available when checked on 17 Nov. |
| Ready | Ready: your AI-native base was reused because it leads with shipping AI agents and zero-to-one work, this role's core asks. Shortlist chance about 7/10. Gaps: no consumer-product experience. |
| Needs answer | Waiting for your answer: the form asks "Are you willing to work on-site three days a week?" and the answer bank has no answer. Add it in the answer bank and this role will continue. |
| Applied | Applied on 18 Nov; the confirmation page showed reference A123. |
| Rejected | Rejected: the company emailed on 20 Nov to say they are moving forward with other candidates. |
| Duplicate | Duplicate: this is the same posting (same requisition number) as the existing Senior PM row for this company, so that row is kept. |

Company Agent notes follow the same rules, for example: `Held until about 3 December: you have already applied to three roles here in the last 30 days, which is your personal limit.` `scripts/stage_state.py:agent_note_problems` flags notes that break the mechanical rules (too long, code-like text); writers fix those before saving.

## Compact job facts

Starting salary and Max salary are numeric endpoints of one verified advertised base-pay band, in the single currency and period registered in Settings.applications_schema.salary_display. Pick the highest advertised maximum in that currency with its paired minimum; leave both blank when no compatible verified band exists. Never mix currencies or periods, convert implicitly, use total compensation or write zero. Additional compensation: Equity, Bonus, Commission, Bonus or commission, Not stated. Location holds short places; Work arrangement is Remote/Hybrid/On-site/Unspecified. Use scripts/tracker_values.py for parsing. Job evidence preserves the exact JD with every band, condition and location; Review checks applicability there.

No availability column is kept and Scan does not monitor closures. Review opens the live posting when it can and sets an expired role to Not pursuing (stages/review.md Step 1); when the page cannot be reached, a saved exact official JD supports Review. Apply checks the live form. When Scan reobserves a role, record source membership, observation time and content fingerprint in History; a changed fingerprint triggers comparison and affected re-review.

## Stage metadata

Stage snapshots live in History `Field changes (JSON)`:

    {"schema":"nextmove.stage-state.v2","records":[{"record_id":"...","job_key":"...","stage_runs":{},"source":{},"review":{},"preparation":{},"submission":{},"feedback":{},"details":{}}]}

Each record is a complete snapshot for one application, so recovery never replays a delta chain. Build it with `merge_state` (or `merge_company_state` for Curate), wrap it with `payload`, link the History row to the affected Applications and the Run, and read it back before accepting the handoff. Read with `resolve` (newest complete snapshot wins) and `stage_versions`. Batch within tool limits and parse outside model context.

`stage_runs` names the Scan, Review, Preparation and Submission runs; each matches the Application's Run link (at most one current context per stage). One full Run can fill all four.

Runs `Input versions (JSON).stage_inputs` holds shared fixed inputs per stage (goals, master, policy, guidelines, instruction versions); per-job metadata holds the exact `jd_hash`, decision and review time, with `version_overrides` for per-job differences. Null means unknown, never an inherited current value. Review's policy identity is `review-sha256:<digest>` of stages/review.md, computed by `scripts/role_gate.py:review_frame_contract`; editing that file requires revalidating affected approvals. Other policy identifiers live in contracts/policy-versions.json. A manually set Queued or Ready status is never acceptance evidence.

Long content (full JD captures, assessment evidence, resume change notes, role-specific answers) lives in versioned Drive files; `details` holds the file ID, role selector and integrity hash.

## Drive destinations

Settings.resume_output is the Role specific folder; Settings.content_output is the Audit trail folder. Both record root_folder_id; verify parent and privacy. RESUME-FILES.md owns placement and naming. Run captures, reports and metadata go to Audit trail.

## Stage writes

- **Curate:** company snapshots use `merge_company_state` with the company record ID and link to the Run, never to Applications. Save `funding` facts with source identity, retrieval time, event-date meaning and any uncertainty, `company_fit` with the advisory rating and evidence-based reason, and `origin` when known. Preserve prior snapshot sections when updating one part. These are History metadata, not Companies columns. Run checkpoint `stages.curate` keeps holds, policy_research and discovery parts separately; discovery feed cursors live in Settings.company_policy.discovery.checkpoints and advance only after verified complete coverage.
- **Scan:** freeze scope from current Companies (`scan_enabled`) and active Sources; recheck targeting at the write boundary. `application_write(creating=True)` needs current Companies records, a new canonical Job key, Inventoried and Role eligibility Pending. Save source memberships, requisition IDs, aliases, capture selectors, observation times and fingerprints in `source`.
- **Review:** save the three-step assessment (method, exact input identities, career and resume ratings, total, outcome, evidence, unresolved questions) before changing status, fit ratings, Review run and Agent notes. Record the decisive company evidence identity in `stage_inputs.review.company_evidence`; Curate’s saved company assessment is advisory and never copied into Career fit.
- **Prepare:** save `path`, base, base_version, base_master, guidelines version, coverage, company_consistency and, for tailored versions, change notes, `grounding`, `guideline_check`, editable source, file hash and visual verification. Set Preparation run, Resume link, Resume version and Resume verified at only after `resume_ready` passes on the downloaded bytes.
- **Apply:** save the preflight record (application URL, field map, unresolved items, screenshots) and the `submission_gate` decision. Before Submit, write and read back the attempt intent (role, application URL, resume file ID and hash, answer digest), Submission attempt key and Submission run. Save the result or uncertainty; an existing attempt blocks any retry.
- **Track:** save message identities, confirmation, rejection and engagement times in History; update Lifecycle status and Confirmation reference. Missing mail never proves non-submission.

## History and integrity

Log meaningful changes and business events plus run-level read scope, not every read. Each event records identity, actor/harness, affected table/record/field, before/after values, evidence, actual event time and recording time. Keep receipts, failures, uncertainty and corrections even without a status change.

Airtable writes are not atomic: reconcile persisted state before any retry, and stop dependent work after an uncertain write. Owners can edit records directly, so History is a journal, not tamper-proof auditing. No automatic purge or retention window.

## Preferences and candidate facts

Career Goals holds desired work and tradeoffs only (CAREER-GOALS.md). The editable master, plus any confirmed-facts artifact indexed by Settings.master_resume, is the only source of candidate facts. Record the goals revision and candidate-evidence identity in each Review Run. Goals never authorize submissions or supply qualifications.
