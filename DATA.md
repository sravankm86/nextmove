# Data and recovery

The single reference for Airtable, evidence, history and stage handoff. contracts/core-schema.json is the machine-readable blueprint. Read only the section you need; keep bulk records and verification out of model context.

## Nine active tables

| Table | Purpose |
|---|---|
| Companies | Human targeting, funding, notes and Feedback |
| Applications | Candidate facts, review, preparation readiness, notes and Feedback |
| Sources | Official board/region, reader, pagination and coverage |
| Runs | Frozen inputs, progress, ownership and handoff |
| Settings | Private references, policies, controls and verification |
| History | Meaningful field changes, decisions and failures |
| Review eval | Frozen feedback answer key and eval results |
| Answer bank | Reusable Form answers: question, answer, guidance and approval |
| Application questions | Role-specific questions, drafts and resolved final answers |

The generated contract defines fields and reciprocal links. Native record IDs and createdTime replace metadata columns. Display keys are not uniqueness constraints: writers validate business keys, link cardinality and intended deltas. Existing installations may retain extra history fields/tables/options; these are not new-setup requirements. Never delete them as part of startup or write outside the active schema. See WORKFLOW.md "Existing installations" and docs/MAINTENANCE.md for non-destructive upgrades.

**Companies.** Company, Company key, Search status, Manual notes, Feedback, Agent notes, Funding stage, Company evidence, Applications, Sources, and Curate run. Human targeting is Proposed/Allow/Exclude; only the human sets Allow/Exclude. Funding stage is ordered from Pre-seed / Seed through Series A–D, Series E+, Late private and Public; Unknown is not a verified funding stage. Keep actual maturity separate from investment type. Full evidence, round labels/amounts/dates, parent history, advisory company-fit reasoning and creation origin belong in versioned evidence/History, not columns. Curate owns factual company writes; Review independently applies current goals.

**Applications.** The active fields in scripts/stage_state.py:CORE_FIELDS, including Company, three stage Run links and History. Application ID is the formula RECORD_ID(); never write it. Job key holds the canonical employer posting identity. Resume link/version/verified time identify the exact Ready PDF. Application questions links the role-specific answer table; Answer bank rows are general and are not linked to applications. Other retired submission/confirmation fields and post-Ready outcomes remain read-only history; they are not requirements for a new run.

**Sources.** Source key, Company, Official careers URL, Catalog URL, Region, Reader, Reader version, Latest coverage, Checkpoint (JSON), Last error, Last scanned at, Last run, Archived at. Checkpoints hold cursor/end proof, counts, manifest identity and pagination details. Archived at disables a retired source; every other configured board/region remains in scope.

**Runs.** Run key, Run type, Status, Owner, Instruction revision, Input versions (JSON), Scope (JSON), Checkpoint (JSON), Expected/Completed/Blocked items, Started at, Finished at, Agent notes, plus Curate companies, History, Sources and three application-stage reciprocals. Checkpoints retain pending checks, next actions and ownership release (scripts/stage_state.py:run_progress). Input versions are fixed; progress updates never rewrite them. Expired heartbeats are not proof of writer release.

**Settings.** Key, Value, Reference URL, Version, Verification, Notes. Private references, source-versioned extracted preferences, policies and Stop all. Procedures and command routing stay in Git. The answer_bank resource maps both active answer tables. Legacy mailbox/submission resources and old pause controls may remain archived; do not read them as required stage inputs or turn old controls off.

**History.** Event key, Operation ID, Event type, Recorded at, Occurred at, Actor / channel, Table reference, Record reference, Field changes (JSON), Evidence URL, Notes, Application, Run. Record intended before/after and actual persistence. Preserve all legacy events, even for retired stages.

**Review eval.** Example, Application record, Job link, Your verdict (Pursue/Not pursuing), Reason, Reason type, Split (Train/Holdout), Active, Inputs snapshot, Last prediction (Queued/Need review/Not pursuing), Last eval, Added on, Match. The user's graded Feedback supplies expected answers; predictions never supply the answer key. Ambiguous/partial feedback remains pending and inactive rather than receiving an invented verdict. Match is a convenience; score immutable predictions for coverage and recall.

## Feedback inbox and Review eval

Manual notes is lasting human context and is never consumed or automatically cleared. Feedback is the separate evaluation inbox: the user writes it and the coordinator consumes it. Neither field supplies executable instructions or silently overrides goals, facts or lifecycle decisions. Clearing is an acknowledgement of verified capture, never permission to erase uncaptured feedback. Keep raw text word for word in the eval case and History. Agents never rewrite the original verdict or Reason to match a prediction.

### When and how to capture

At the start and completion of every stage invocation, read newly nonempty or changed Feedback in the affected tables. A standalone Capture feedback command checks the whole configured feedback scope. Use a durable feedback cursor/receipt index in Settings.eval_registry and History; compare fingerprints, not a time-only cutoff. Check every page of the selected scope. Chat corrections enter the same path with a durable chat evidence reference. A missing registry or capture capability leaves the note pending and reports a feedback gap; it does not authorize clearing or block unrelated stage work. No work runs between invocations without an external scheduler.

1. Identify stage, source table, stable record/posting identity, raw note and the action/evidence it corrects. Never derive the expected result from the current application status or the agent’s own assessment.
2. `scripts/review_eval.py:feedback_id` fingerprints stage, stable entity and note; `feedback_action` returns capture or reuse. Same entity and same feedback reuses its case and verified receipt. A different note is a new feedback revision, not permission to overwrite the old frozen answer. Titles alone never establish duplicates; only verified role IDs or exact canonical posting links may reconcile aliases. Different language/region/role IDs stay distinct. Similar JDs can share a split group without being duplicate postings.
3. Add/update the eval case and versioned private dataset under Audit trail. For Review, use the existing Review eval table. Copy raw feedback to Reason, link the Application record and Inputs snapshot, and preserve existing human verdicts and splits. A new explicit verdict may create a new version; archive the previous version rather than rewriting its answer. Conflicting/ambiguous feedback stays pending and inactive with a specific clarification question in the snapshot/run. Partial feedback about salary extraction or writing quality is retained as an assertion/pending case; do not invent a whole-role verdict. Other stages use stage-tagged pending cases in the same private catalog until their evaluator is implemented; do not force them into Review scores.
4. Freeze the exact inputs needed to reproduce the action: JD, goals, master and confirmed candidate facts, company facts and procedure text, with content hashes and source revisions/IDs. Separate event dates from retrieval dates. Preserve original snapshots; changes create a new dataset version. Missing evidence makes the case unscored, not automatically wrong or correct.
5. Save a History event with feedback identity, source record/raw note, eval record/case ID, snapshot reference/hash and intended before/after. Read back the eval, artifact metadata/content hash and History. For a reused receipt, verify the existing capture still exists. `may_clear` requires all three verifications and an exact source-note reread. Then clear only Feedback, save/read back that mutation and its receipt. If any write is uncertain, leave the note, reconcile persisted state before retrying, and never insert blindly. If the user edits the note, preserve the new text for the next capture.

A note that conflicts with newer preferences is still captured and cleared after verification; keep its case inactive with the conflict, raw feedback and original preference context. Do not discard feedback because the role expired or preferences changed. Clearing notes never changes Lifecycle status, fit, resumes, targeting or submission state. The feedback coordinator is the sole exception to ordinary stage writers preserving Feedback.

### Transition from the old inbox

Preserve all existing Manual notes. Copy only explicitly identified corrections into Feedback, record the source/identity and before/after in History, and leave the original note untouched. Ordinary annotations are not evals. Stable stage/entity/text fingerprints reuse existing verified receipts; do not recapture the same feedback merely because its column changed. Old datasets, labels and receipts remain historical truth. feedback_clear returns only a verified Feedback delta. Missing snapshots or ambiguous feedback stays pending; no note is cleared during schema migration.

### Blind replay

Settings.eval_registry identifies the current private dataset, feedback receipt index, Review eval table and latest baseline/report references. The public repo holds procedures only. Run Review eval / Eval Review as an Experiment, separate from production Review. Normal production commands capture feedback and propose improvements; they do not launch a full replay after every note.

1. The coordinator resolves current registered artifacts and compares live Your verdict, Reason, Active and Split with the catalog. Human edits create a new catalog/key version; keep prior versions and predictions. Resolve current input sources and refresh changed facts explicitly, then freeze them for this experiment. Preserve the answer key and make a versioned input snapshot. Choose the exact saved JD/hash, not a mix of old and live text. Run `python scripts/review_eval.py prepare DATASET --bundle REVIEWER.json --key KEY.json` (optional `--split Train` or `--split Holdout`). The key and pending cases never enter the reviewer bundle.
2. Use a fresh review-only worker/context that has not seen the answer key. Delegate only the label-free bundle, its hash and the prediction output path; do not pass this chat, Manual notes, Feedback, Reason, verdict, split, prior Agent notes/status or Match. The worker reads only the bundle, follows its frozen Review procedure and writes predictions. No connectors, live posting fetches, answer-key lookup or production writes. This is a new harness context, not an API scoring service. If unavailable, prepare the handoff and report the baseline blocked; never call an existing-status comparison a blind replay.
3. Predictions are JSON with `bundle_sha256` and `predictions`: each entry has `case_id`, `career_fit`, `resume_fit`, `status` and a concrete `reason`. An explicit frozen Exclude/Proposed company may instead use `scope_decision` Excluded/Proposed. Assess all runnable cases; no hidden truncation or invented missing inputs.
4. Commit predictions to a separate private artifact before the coordinator opens the answer key. Run `python scripts/review_eval.py score REVIEWER.json KEY.json PREDICTIONS.json --output REPORT.json`. The helper checks input identity, duplicate/unknown case IDs and frozen score routing; missing/corrupt cases remain unscored and lower coverage. Report Train and Holdout separately, including status match, positive recall, queue precision, false queues, missed roles, positive deferrals and coverage. Counts describe this selected dataset, not population-wide recall. Reason correctness needs separate evidence-based inspection; a matching status alone does not prove sound reasoning.
5. Audit then write only Review eval.Last prediction and Last eval for scored cases; the prediction artifact/History retain reasons and each prior run. No prediction for a blocked case. Do not erase previous results or imply a pending run is completed. Replay itself never changes Applications; the separately audited inbox step may clear only verified captured Feedback.

### Improve without forgetting

Use only Train failures when drafting improvements. Group by cause and separate preference changes (Career Goals), confirmed candidate facts (master/facts), procedures (Git), and extraction/identity defects (readers). Preserve unknowns and do not learn Review-owned exclusions into Scan. Use `compare` on the same factual inputs/cases and independent baseline/candidate predictions; candidate instructions have their own fingerprint. Report every newly broken case, especially previously successful Pursue examples. Inspect critical reasoning as well as outcome counts.

Keep Holdout labels/reasons out of tuning and evaluate only the settled candidate there. Keep related variants in a stable group; report cross-split overlap and do not claim independent holdout evidence for leaked groups. Repeatedly consulted holdout cases become regression examples; reserve new feedback for fresh holdout coverage. Propose the smallest correction, with affected cases, before/after behavior, improvements, regressions and remaining uncertainty. No automatic change to user preferences, answer keys, production states or submission permission; apply a proposed rule change only within the user’s authorization. Revalidate affected decisions when approved inputs change. Keep reports and proposals in Audit trail and checkpoints in the existing Runs/History tables.

## Everyday view and notes

The Review view shows Company, Role, Lifecycle status, Manual notes, Agent notes, Starting salary, Max salary, Additional compensation, Location, Work arrangement, Job posted date, Career fit, Resume fit, Job description link and Resume link, with Manual notes beside status. Filter Lifecycle status = Need review for decision gaps and Ready for finished resumes.

Keep Manual notes beside Lifecycle status for permanent annotations; show Feedback beside it for corrections. Only Feedback follows the capture/clear procedure above. The archived feedback remains authoritative evidence; it never authorizes submission or changes global criteria by itself. Neither notes field is an instruction source.

## Writing Agent notes

Agent notes tells the user, in plain English, why the agent set the row's current status. Write it for someone who has not read the job description or these instructions. Each time an agent changes the status, it replaces the note (the previous note goes to History).

- **Say what and why.** Start with the status, then the main reason in everyday words: what about the role or the user's background led to it.
- **Name the confusion.** If something is unclear or missing, say exactly what it is and why it matters for the decision.
- **Say what happens next.** End with the next step, or what the user needs to do, when there is one.
- **Keep it short and plain.** One to three sentences, under about 60 words. A Ready note may give the estimated shortlist chance as "about N/10" when Settings `preparation_notes.shortlist_estimate` is on (stages/prepare.md); no other scores. Full sentences; no internal field names, codes, scores written as sums, record IDs, file hashes, JSON or Markdown; spell out abbreviations.
- **Be concrete.** Name the actual requirement, preference, company rule or question rather than a category.

Examples (fictional):

| Status | Agent notes |
|---|---|
| Queued | Queued: this is the AI agents platform work you want, and your experience covers every key requirement, including shipping agents at scale. Next, a resume will be prepared. |
| Need review | Needs review: the role fits your goals, but the posting does not say whether it is based in the US or London, and you only want US roles. Once the location is confirmed, it can be decided. |
| Not pursuing | Not pursuing: the role requires five years of hands-on payments engineering, and your background shows product leadership but no engineering track record. |
| Not pursuing | Role expired: the posting was no longer available when checked on 17 Nov. |
| Ready | Ready: your platform base was reused because it leads with the large-scale launches this role asks for. Gaps: no direct experience in the retail industry. |
| Duplicate | Duplicate: this is the same posting (same requisition number) as the existing Senior Analyst row for this company, so that row is kept. |

Company Agent notes follow the same rules, for example: `Proposed: the latest verified funding round meets your company-stage preference. Please choose Allow or Exclude.` `scripts/stage_state.py:agent_note_problems` flags notes that break the mechanical rules (too long, code-like text); writers fix those before saving.

## Compact job facts

Starting salary and Max salary are numeric endpoints of one verified advertised base-pay band, in the single currency and period registered in Settings.applications_schema.salary_display. Pick the highest advertised maximum in that currency with its paired minimum; leave both blank when no compatible verified band exists. Never mix currencies or periods, convert implicitly, use total compensation or write zero. Additional compensation: Equity, Bonus, Commission, Bonus or commission, Not stated. Location holds short places; Work arrangement is Remote/Hybrid/On-site/Unspecified. Use scripts/tracker_values.py for parsing. Job evidence preserves the exact JD with every band, condition and location; Review checks applicability there.

No availability column is kept and Scan does not monitor closures. Review opens the live posting when it can and sets an expired role to Not pursuing (stages/review.md Step 1); when the page cannot be reached, a saved exact official JD supports Review. Prepare inspects application questions under stages/prepare.md; Scan and Review do not. When Scan reobserves a role, record source membership, observation time and content fingerprint in History; a changed fingerprint triggers comparison and affected re-review.

## Stage metadata

Stage snapshots live in History `Field changes (JSON)`:

    {"schema":"nextmove.stage-state.v2","records":[{"record_id":"...","job_key":"...","stage_runs":{},"source":{},"review":{},"preparation":{},"feedback":{},"details":{}}]}

Each record is a complete snapshot for one application, so recovery never replays a delta chain. Build it with `merge_state` (or `merge_company_state` for Curate), wrap it with `payload`, link the History row to the affected Applications and the Run, and read it back before accepting the handoff. Read with `resolve` (newest complete snapshot wins) and `stage_versions`. Batch within tool limits and parse outside model context.

`stage_runs` names the Scan, Review and Preparation runs; each matches the Application's Run link (at most one current context per stage). One full Run can fill all three.

Runs `Input versions (JSON).stage_inputs` holds shared fixed inputs per stage (goals, master, policy, guidelines, instruction versions); per-job metadata holds the exact `jd_hash`, decision and review time, with `version_overrides` for per-job differences. Null means unknown, never an inherited current value. Review's policy identity is `review-sha256:<digest>` of stages/review.md, computed by `scripts/role_gate.py:review_frame_contract`; editing that file requires revalidating affected approvals. Other policy identifiers live in contracts/policy-versions.json. A manually set Queued or Ready status is never acceptance evidence.

Long content (full JD captures, assessment evidence and resume change notes) lives in versioned Drive files; `details` holds the file ID, role selector and integrity hash.

## Drive destinations

Settings.resume_output is the Role specific folder; Settings.content_output is the Audit trail folder. Both record root_folder_id; verify parent and privacy. RESUME-FILES.md owns placement and naming. Run captures, reports and metadata go to Audit trail.

## Stage writes

Before any existing-row stage update, resolve the latest complete state and call application_write with existing_application and existing_state from live reads. The writer rejects Manual notes writes. protected_history is a preservation check, not a submission/retry workflow. The feedback coordinator may clear only verified captured Feedback on a protected row. Preserve archived schema keys in existing snapshots when merging; new snapshots do not create submission state.

- **Curate:** company snapshots use `merge_company_state` with the company record ID and link to the Run, never to Applications. Save `funding` facts with source identity, retrieval time, event-date meaning and any uncertainty, `company_fit` with the advisory rating and evidence-based reason, and `origin` when known. Preserve prior snapshot sections when updating one part. These are History metadata, not Companies columns. Run checkpoint `stages.curate` keeps company_research and discovery parts separately; discovery feed cursors live in Settings.company_policy.discovery.checkpoints and advance only after verified complete coverage.
- **Scan:** freeze scope from current Companies (`scan_enabled`) and active Sources; recheck targeting at the write boundary. `application_write(creating=True)` needs current Companies records, a new canonical Job key, and Inventoried status. Save source memberships, requisition IDs, aliases, capture selectors, observation times and fingerprints in `source`.
- **Review:** save the three-step assessment (method, exact input identities, career and resume ratings, total, outcome, evidence, unresolved questions) before changing status, fit ratings, Review run and Agent notes. Record the decisive company evidence identity in `stage_inputs.review.company_evidence`; Curate’s saved company assessment is advisory and never copied into Career fit.
- **Prepare:** save `path`, base, base_version, base_master, guidelines version, coverage, company_history (verified match count, evidence, compared versions and any missing details), company_consistency and, for tailored versions, change notes, `grounding`, `guideline_check`, editable source, file hash and visual verification. Save the verified resume fields after `resume_verified` passes on the downloaded bytes, while keeping Queued. Save `preparation.application_questions` with form identity/hash/time, full coverage evidence, blockers and every question's exact text/options/type/required flag plus matched table/record/fingerprint/mapped answer. `resume_ready` additionally checks current live Approved/Resolved answers before Ready.

## History and integrity

Log meaningful changes and business events plus run-level read scope, not every read. Each event records identity, actor/harness, affected table/record/field, before/after values, evidence, actual event time and recording time. Keep receipts, failures, uncertainty and corrections even without a status change.

Airtable writes are not atomic: reconcile persisted state before any retry, and stop dependent work after an uncertain write. Owners can edit records directly, so History is a journal, not tamper-proof auditing. No automatic purge or retention window.

## Preferences and candidate facts

Career Goals holds desired work and tradeoffs only (CAREER-GOALS.md). The editable master, plus any confirmed-facts artifact indexed by Settings.master_resume, is the only source of candidate facts. Record the goals revision and candidate-evidence identity in each Review Run. Goals never authorize submissions or supply qualifications.

## Registered sources and small artifact reads

Keep the existing split: Drive holds source documents, frozen captures, reports and archives; Airtable holds references/state; Git owns procedures. Do not add preference/fact tables or a current-JD column during source-registration repair.

At startup read each stage's registered sources by ID, including every document tab. Record the observed provider revision and SHA-256 of extracted text in Settings/Run inputs. For native Docs use source_registry.document_text: concatenate all tab-body text runs in provider order, preserving whitespace; exclude style/header/footer metadata. Do not substitute a trimmed export hash. Use scripts/source_registry.py:inspect to detect changes. Refresh the source reference after readback, but do not relabel an old extraction as current: cache_current requires both source_revision and source_text_sha256. Changed goals mark affected extracted preference sets stale. Re-extract them under CAREER-GOALS.md before using them; update readiness only after validating passages, comparisons, units, conditions and exceptions. Do not change production fit/status merely while repairing pointers. Check again before consequential writes. Metadata Verified means the reference/content was read, not that its factual claims were independently verified.

Settings.reader_artifacts registers pinned public reader paths and their supported artifact shapes; board-specific parameters and coverage remain in Sources. Download complete artifacts through the harness's own authenticated connector, using file-backed downloads when needed; verify expected byte hashes when registered. Then call `python scripts/artifact_reader.py LOCAL_FILE --kind job --id EXACT_APPLICATION_ID` (or company/source with the corresponding exact ID; optional --sha256 EXPECTED_BYTES_HASH). Only the selected record enters model context. The job reader emits the complete JD and posting identity, excluding previous decisions and shared personal inputs; missing/ambiguous records, missing full descriptions and hash mismatches are blockers, never permission to choose a similar title. Frozen eval inputs require the dedicated label-free eval workflow; selecting a catalog case does not make it a blind reviewer input. Reader registration does not certify board coverage or implement every catalog provider.

Legacy spreadsheet references are historical-only and permitted only when the particular record explicitly points to them. Preserve exact sheet/tab/cell references for existing applied/rejected history. Do not use a global spreadsheet fallback, recreate retired columns, delete historical links or infer that a blank capture proves a role never existed. New records use current official postings and verified Drive capture references. Old reports and archived answer documents are not active preference sources.

Legacy answer documents and mailbox checkpoints are inactive history. The live answer tables are active; narrative drafts can use relevant verified source content without turning old documents into workflow instructions. Do not require access, refresh them or infer coverage for removed tasks. Their source content and private references remain untouched. Registered goals, master, resume guidelines/base library, exact job/company evidence and the live answer tables govern the active stages.

## Answer bank and Application questions

**Answer bank** holds reusable Form answers in five fields: Question (a short readable label and the primary field), Answer (the value to give), Guidance (only real rules: how to map to offered options, limits and any company or role restriction), Source field (only for values that come from another registered source, such as Career Goals salary) and Approved (checkbox). Only a nonempty Answer with Approved ticked is ready, and only within any restriction its Guidance states. Use the Answer's meaning: select the offered option or wording that means the same thing; never add claims, merge answers or broaden a rule. A Source field pointer without an Answer is not ready; capture the current source value as an unapproved Answer and ask for approval. Never tick Approved or edit an approved rule automatically. Use the native record ID for rule identity; the readable Question label is not globally unique when Guidance differs.

**Application questions** holds Question ID, exact Question, Draft answer, Final answer, Status (Needs answer/Resolved), Field key, Options, Question type (Form/Narrative), Sources and Answered on, plus the Application link. New narrative questions belong here, linked to exactly one application. Resolve company context through that Application’s Company link; a retained text Company column is only historical/display context. Resolved requires a nonempty Final answer; Draft answer does not count. Existing resolved Form records remain usable for their own application. Preserve extra historical columns, human final answers and feedback. Answered on records the user's actual submission date, not the date the agent drafted or resolved an answer.

Prepare owns discovery, deduplication, drafting and readiness checks under stages/prepare.md. The user supplies/approves form answers and confirms final narrative answers. Save exact employer field identity, prompt/options, source URL, applicability and before/after values in History/Drive; no extra Applications columns are needed. For a new Answer bank row, Question is a short readable label and Guidance preserves the exact employer prompt and options. Use stable semantic question identity plus scope/options to reuse rows; do not create another blank draft on each retry. Do not collapse distinct answers simply because prompts resemble each other.

The per-application manifest uses schema `nextmove.application-questions.v1`, application_id, job_key, job_url, form_url, inspected_at, coverage, evidence, blockers and questions. Each question has field_key, question, options, type, required and, when answered, answer = {table, record_id, fingerprint, mapped_answer, mapping_verified, match_evidence}. `question_key` supplies a stable per-application employer-field key for discovery retries; semantic cross-role reuse still needs judgment. `form_fingerprint` hashes the question definitions; `answer_fingerprint` pins the current question label, answer, guidance, source and approval (bank) or question/final answer/status (role questions). Save the complete manifest in the preparation snapshot, with large form evidence in Audit trail. Empty questions is valid only after a complete verified inspection; missing or blocked inspection never passes.

Normalize live select values to names and links to record-ID lists before helper calls. `resume_ready(..., answer_bank=LIVE_ROWS, application_questions=LIVE_ROWS)` uses `current_inputs.answer_check_date` in the user's timezone and the freshly inspected per-role `current_inputs.form_hash`. A saved manifest cannot certify its own freshness. Live row changes, revoked approval, failed Guidance restrictions, unanswered required fields and unknown coverage block Ready. Optional unanswered questions do not block it. Keep the verified resume and Queued status while blocked; an old Ready PDF is reusable evidence, not proof of this expanded handoff. Preserve protected later outcomes unchanged. No automated form filling, submission or mailbox work is added.
