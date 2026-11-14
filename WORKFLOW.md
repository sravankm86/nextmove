# Run Nextmove

Lifecycle status determines the work queue. The five responsibilities are logical workers, not a requirement to start five model agents. Use code for bulk I/O and comparisons, models for judgment and exceptions, and one coordinator as the shared-state writer.

| Worker | Input queue | Responsibility | Output |
|---|---|---|---|
| Scanner | Every Target Companies row marked Allow, regardless of existing application states or temporary holds | Enumerate official catalogs; apply broad metadata filters; deduplicate; capture job metadata | New verified broad matches → Queued; refresh metadata without resetting tracked states |
| Reviewer | Queued; review_pending pre-submission rows; review-owned Needs review after changed evidence or explicit retry | Read the full JD against career goals and the latest master resume; assess both axes independently | Shortlisted, Not a fit, or Needs review |
| Preparer | Shortlisted with current review evidence and required factual sources | Reuse a suitable approved base resume or tailor from the master; verify integrity, PDF and change notes | Ready, or remain Shortlisted with a preparation blocker |
| Applier | Ready with explicit submission authorization and all live gates satisfied | Submit the exact role using the verified resume and capture the receipt | Applied → Confirmed when receipt is available; Submission uncertain if unresolved |
| Tracker | Mailbox changes and submitted/active/uncertain roles; exact-role events may also concern terminal records | Reconcile receipts, recruiter activity and outcomes read-only from mail | Confirmed, In process, Offer, Accepted, Rejected, Closed, or a scoped unresolved exception |

## Manual harness commands

Use [COMMANDS.md](COMMANDS.md) for Scan / Review / Prepare / Apply / Track. The operator chooses one active harness; it recovers context and state, completes its authorized queue and saves a handoff. A single-stage invocation then stops. An explicit multi-stage plan in ARCHITECTURE.md may advance the same harness after acceptance; manually switching harnesses uses the identical contract. Next command is advisory, not an automatic launch. Stage execution state is separate from application lifecycle. See the [one-time bootstrap](HARNESS-BOOTSTRAP.md).

## Run contract

Load [setup](SETUP.md), [universal rules](AGENTS.md), [storage contract](STORAGE.md), [data governance](DATA-GOVERNANCE.md), private inputs, live Airtable schema and controls. Record run ID, instruction/version hashes, requested workers, mode and timezone. Follow [LIFECYCLE.md](LIFECYCLE.md). A stage-specific request runs only that worker and its necessary preflight. Only an explicitly requested, privately recorded ordered plan may advance to another stage, using the same acceptance checks; no inferred pipeline or submission authorization.

1. Run [Scanner](stages/scan.md) across every Allow company, including regional boards. Preserve Exclude-over-Allow precedence and Pool. Reuse readers, validate catalog coverage, process deltas and save Queued candidates with salary, work-location details, job-posted date and provenance. Unknown metadata remains explicitly unknown.
2. Run [Reviewer](stages/review.md). A High career-goal fit OR a High resume fit qualifies for Shortlisted. Both Low means Not a fit. Borderline or unresolved evidence means Needs review, not an invented negative. Record the independent scores, rationale, gaps and versions.
3. Run [Preparer](stages/prepare.md). Every resume claim must be grounded in the latest editable master. Record base/tailored choice, change notes, master version, verification and PDF link. Unsupported claims block Ready.
4. Run [Applier](stages/apply.md) serially only under explicit auto-apply authorization. Recheck exact-role history, live availability, company quotas/cooldowns, answers, resume version and pause/stop controls immediately before Submit. Review/prepare modes never submit.
5. Run [Tracker](stages/track.md) independently on a resumable mailbox checkpoint. Track confirmation separately from a submission mark, and actual recruiter engagement separately from acknowledgement. The Applier may capture an immediate receipt; the Tracker handles later mail and reconciliation.
6. Report queue sizes, transitions, coverage, blockers, deferred work and receipts/outcomes. Scan coverage and description gaps are independent of review decisions.

The Tracker may be invoked as an explicit preflight reconciliation before submission or another requested workflow. Missing mail access must be reported and must not be presented as a reconciled mailbox or prevent an otherwise authorized scan.

## Handoffs, persistence and ownership

Process review and preparation in bounded batches with durable checkpoints. Report the remaining queue explicitly; a completed batch is not a completed queue. Reuse assessments only when their JD, career-criteria and master versions remain valid. A whole-queue request continues through checkpoints unless a live control, explicit budget or unresolved blocker stops it.


Each handoff includes run ID, worker, job key, current/expected state, input versions, artifact/evidence references and blocker/next owner. The coordinator journals read/mutation intent and scope under DATA-GOVERNANCE.md, rereads affected rows, checks that state and versions still match, writes only the permitted delta and verifies readback. Concurrent human edits take precedence over a stale plan and must be reconciled.

Record transitions and their provenance in the authorized lifecycle event log when configured. Make events idempotent by source event/job identity; do not duplicate receipts or replay uncertain submissions. Keep current status, fit scores, history and company holds separate. In a runtime such as Dot, delegated work must remain visible and return a durable checkpoint.

Flag review_pending for relevant JD, criteria or master changes on pre-submission assessed roles, including Not a fit. The Reviewer may revise a pre-submission state with the changed-input reason recorded; a new scan alone must not do so. Do not continuously reprocess unchanged Not a fit, completed or blocked records. Retry when relevant JD/criteria/master evidence changes, a blocker is resolved, or the user explicitly requeues. Submitted or terminal records are not silently reopened by changed fit scores.

## Dashboard and controls

Show each lifecycle queue, independent career/resume fit, scan coverage, metadata/description gaps, preparation blockers, company eligibility, uncertain submissions, unmatched mail and latest successful checkpoints. Link exceptions to evidence and next owner.

Pause applications blocks the next submission while scanning, review, preparation and tracking may continue. Stop all stops new work and active workers at their next safe checkpoint. A stop cannot recall an application already sent. This repository defines contracts and templates; the chosen runtime must implement workers, scheduling, durable state and controls.

