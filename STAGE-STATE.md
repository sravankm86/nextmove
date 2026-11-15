# Stage metadata and the 36-field tracker

Applications holds current job facts, status/manual notes, independent eligibility/career/fit gates, the current PDF reference/hash/verification, attempt identity and four stage Run links. `scripts/stage_state.py` defines its 36-field allowlist and pure metadata readers/guards. It rejects writes to retired fields; do not recreate them to resume an old plan. Resolve live field IDs and aliases first. Every new candidate has a unique canonical Job key and one allowed Company. Preserve unmatched legacy history by native record identity rather than inventing employer IDs.

## Persistent metadata

Use the existing History `Field changes (JSON)` field for records with this bounded schema:

    {"schema":"nextmove.stage-state.v1","records":[{"record_id":"...","job_key":"...","stage_runs":{},"source":{},"review":{},"preparation":{},"submission":{},"feedback":{},"details":{}}]}

This is stage metadata in the audit table, not another current-job JSON field. Batch within actual field/tool limits; keep the full metadata snapshot per affected application so recovery does not require replaying an unbounded delta chain. Link each History row to its affected Applications and execution Run. Retain actor/channel, recorded time and actual event time when known. A successful metadata write must be read back before its Application handoff is accepted.

Read the application's History links and relevant Runs in bounded batches, parse outside model context, then use `resolve` and `stage_versions`. Do not concatenate all evidence into prompts. The newest complete snapshot for an application supersedes its earlier snapshot. Unknown legacy information stays unknown. Current records must have a snapshot before retired fields are removed. A migration snapshot can preserve original context Run IDs even though its audit event belongs to the migration Run.

`stage_runs` identifies Scan run, Review run, Preparation run and Submission run. Each is a real Runs relationship on Applications, at most one current context per stage. One full invocation can use the same Run for all four; separate harness commands use their own Runs. Keep prior contexts/events in History. A historical source admission and a later semantic revalidation must retain their actual provenance; a Scan link is not proof that every catalog was complete.

Migration may create immutable context-only Runs instead of altering old execution metadata. These have type Migration, explicitly declare that no new job stage was executed, and preserve the original execution Run ID. Snapshot `original_execution_runs` retains those identities. Such a context can back a migrated acceptance only when the original per-job explicit acceptance and exact input identities were preserved and verified; migration itself never approves a job.

## Input versions and evidence

Runs `Input versions (JSON).stage_inputs` holds shared fixed inputs by stage: goals/master/policy/instruction versions as applicable. Per-job review metadata holds its exact `jd_hash`, explicit `decision`, current-description provenance and review time. Rare mixed/legacy contexts use explicit `version_overrides`; null means unknown, not permission to inherit a current value. Freeze accepted input identities. A changed input scope creates a new stage segment/snapshot identity; never rewrite the pins underlying older approvals.

Use `contracts/policy-versions.json` for decision-policy versions. A schema-only repository release retains existing policy versions; audit the deployment revision separately. Changed goals, master, decision rules, JD or PDF still requires the affected checks. A manually selected Queued or Ready status is not acceptance evidence.

Detailed source/assessment content lives in exact versioned Drive captures. `details` contains its file URL/ID, role selector and integrity reference. It preserves original salary/location conditions, employer posting aliases, full assessment evidence, resume change/claim notes and role-specific answers. A shared file URL without a role selector is insufficient. Never discard those facts because the display columns are shorter. Current job evidence remains directly accessible on Applications.

## Stage writes

- Scan: save basic-semantic/source metadata and policy context, update Scan run, current job facts and Last seen at. Preserve outcomes/manual notes. Unknown identity stays in Runs; ambiguity in eligible scope can stay inventoried. `source` keeps real requisition IDs, verified aliases, capture selectors and first-observed time; do not derive employer identity from a title or a URL hash.
- Review: save accepted full-JD metadata, exact JD fingerprint, decision and fixed inputs before updating Review run, Role eligibility, Career gate, independent fit values, Decision category, concise Assessment summary and Blocker. Full reasoning is in the captured assessment. Only explicit approval plus current versions/gates supports Queued. `review_ready` does not infer approval from status.
- Prepare: save grounded change notes, claims evidence, input references, editable source/base reuse, exact file hash and visual verification in the preparation result. Set Preparation run, Resume link, Resume version and Resume verified at only after verification. Preserve submitted files. Use `resume_ready` with the actual downloaded bytes and current inputs; hashes must not come from filenames.
- Apply: before Submit, persist/read back the distinct attempt intent with role, exact submitted PDF ID/version, answer/evidence references and context. Persist/read back Submission attempt key and Submission run on Applications. Only then may an authorized supported browser click Submit. Save the actual result/receipt or uncertainty in History/checkpoint; set current state accordingly. An existing attempt blocks blind retry even if a UI status was changed back to Ready. Never reconstruct submitted bytes later from a changed current resume.
- Track: preserve receipt/message identities, confirmation/outcome dates, actual occurrence time and recorded time in History. Keep current lifecycle and compact Confirmation reference on Applications. Applied on remains an actual date; precise rolling restrictions use known event times where required. Missing mail does not establish non-submission.

Keep history and stage state when current job/resume versions change. A job-specific answer belongs to that attempt/result; reusable candidate facts belong in the registered answer source. Resume requirements are not evidence of experience.

## Manual edits and migration compatibility

Manual notes is human-owned. On changed observed note/status, save the exact observation/fingerprint in `feedback` and a meaningful History event; do not clear or rewrite the note. The editor and actual edit time may be unknown. Never use that feedback as implicit submission authorization or an untested global scan exclusion.

Schema 6 writers use current fields only, even while retired fields remain physically present. Archived pre-migration write plans are incompatible and must be rebuilt against the live schema. Current operational gates and submission controls stay in Airtable; detailed source content stays in Drive. No chat/local file is sole memory. `Settings` stores the schema release and migration manifest reference; instructions stay in Git.
