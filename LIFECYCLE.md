# Application lifecycle and work queues

Applications has one authoritative Lifecycle status (template lifecycle_status). Career fit, resume fit, eligibility, company holds, historical outcomes and evidence are separate fields. Legacy pipeline/history fields are provenance.

| Status | Meaning | Responsible worker / next queue |
|---|---|---|
| Queued | A verified broad candidate from an Allow company's scan; full assessment not yet completed | Reviewer |
| Shortlisted | Full-JD assessment finds High career-goal fit OR High resume fit; other-axis gaps remain visible | Preparer, subject to current evidence and blockers |
| Not a fit | Completed review finds both career-goal fit and resume fit Low | No automatic downstream work; reconsider on relevant changed inputs or explicit user request |
| Ready | Verified approved one-page base or tailored resume, grounded in the latest master, with change notes and version/link | Applier, only when authorization and live gates permit |
| Applied | Human reports submission or agent has a definite completed-submission record; employer receipt not implied | Tracker; Applier may capture an immediate receipt |
| Confirmed | Exact-role employer receipt, success page or acknowledgement confirms receipt | Tracker |
| In process | Actual recruiter engagement: screening, assessments, interviews or scheduling; acknowledgement/silence is insufficient | Tracker |
| Offer | An explicit offer is recorded | Tracker / human |
| Accepted | Acceptance is explicitly recorded | Human outcome; retain history |
| Rejected | Explicit employer rejection or user-reported rejection | Tracker / human; do not confuse with Not a fit |
| Withdrawn | Candidate withdrew after submission | Human outcome |
| Not pursuing | Candidate chose not to apply; preserve exact-role Not applying semantics | Human disposition; not a reviewer verdict |
| Closed | Verified unavailable/cancelled role; preserve Role not available semantics | Verified availability outcome; not a rejection |
| Needs review | Unresolved or borderline evidence; record blocker and next_owner | Only the assigned owner after changed evidence or explicit retry |
| Submission uncertain | A submission may have occurred; receipt/absence cannot be established | Tracker reconciliation; never blind retry |
| Duplicate | Stable-identity duplicate with a canonical record reference; title alone is insufficient | No duplicate downstream work |

The normal path is Queued → Shortlisted → Ready → Applied → Confirmed → In process, then an explicit outcome. Reviewer negatives branch to Not a fit. These are evidence states, not mandatory sequential steps: recruiter engagement can precede a formal application or receipt. Do not fabricate skipped events.

High on either review axis is sufficient; do not silently replace OR with AND, require both axes High, or hide a Low/unknown other axis. Both Low is Not a fit. Any other combination without a High is Needs review. Eligibility is assessed separately: Shortlisted does not authorize submission or invent missing qualifications.

Applied on is the known reported/evidenced submission date; Confirmed on is the exact-role receipt date; Outcome on is an explicitly known event date. Unknown times/dates stay blank. Status recorded at is the recording time, not an invented historical event time. Record source/evidence and preserve conflicts in notes. If configured, append an idempotent lifecycle event with prior/new state, worker, actual event time and recorded time.

Changed JD/criteria/master evidence may set review_pending for pre-submission assessed roles, including Not a fit, without the Scanner resetting their status. Re-review and any revision must record the changed-input reason. Removal of a public posting alone does not end an active application; track posting availability separately unless cancellation/outcome evidence supports a lifecycle change. No new scan resets status. No older acknowledgement regresses recruiter activity, offers or outcomes. No fit reassessment silently reopens a submitted, terminal or user-declined exact role. Preserve human edits and history; explicit reopening requires evidence/instruction and a fresh duplicate/eligibility check. A generic company email cannot confirm a specific application.

Count reported Applied submissions toward company capacity even without a receipt, including later rejected/withdrawn submissions under the actual policy. Uncertain attempts may occupy capacity. Company cooldowns do not change fit or remove Allow companies from scanning.

## Legacy migration

Reviewed and Rated formerly meant assessment completed, including non-positive results. Do not blindly rename them Shortlisted: use evidence under the two-axis rule or send to review-owned Needs review. Discovered is a Queued input alias where supported. Preserve old status/date, fit and pipeline fields, including exact-role dispositions. Do not invent historical dates or infer resume readiness from a link.

Updating these instructions does not migrate a live tracker or install automatic human-edit timestamp/event triggers. Map fields and migrate safely only during authorized tracker work.
