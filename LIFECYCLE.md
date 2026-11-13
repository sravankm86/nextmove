# Application lifecycle

Applications has one authoritative current field: Lifecycle status (template lifecycle_status). Fit/relevance, company cooldowns, historical outcomes and evidence remain separate. Legacy pipeline/history fields are read-only provenance.

| Status | Meaning and evidence |
|---|---|
| Queued | Found by scan and retained by the broad first-pass filter; no full assessment implied. |
| Reviewed | Shortlist assessment completed and recorded. A review does not mean the role is recommended or submitted. |
| Ready | A verified, approved one-page base or tailored resume is available and suitable for this role. A link alone does not establish readiness. Form answers and submission eligibility are separate gates. |
| Applied | The human reports submission, or the agent has a definite completed-submission record. Record the source and known date; employer confirmation is not implied. |
| Confirmed | An exact-role employer receipt, success page or acknowledgement confirms receipt. A generic company email is insufficient. |
| In process | Actual recruiter engagement, including screening, assessments, interviews or scheduling. Silence or an application acknowledgement alone is insufficient. |
| Offer | An explicit offer is recorded. |
| Accepted | Acceptance of an offer is recorded. |
| Rejected | An explicit exact-role rejection or user-reported rejection is recorded. |
| Withdrawn | The candidate withdrew after submission. |
| Not pursuing | The candidate explicitly chose not to apply; preserve exact-role Not applying semantics. |
| Closed | The role is verified unavailable/cancelled; this is not a rejection. Preserve Role not available semantics. |
| Needs review | Identity, submission history or other state evidence cannot be reconciled. Record what needs clarification. |
| Submission uncertain | A submission may have occurred but cannot be verified. Reconcile before retrying. |
| Duplicate | A stable-identity duplicate of another tracked record. Preserve history and point to the canonical record; title-only matches are insufficient. |

The usual path is Queued → Reviewed → Ready → Applied → Confirmed → In process, followed by an explicit outcome. These are evidence states, not mandatory sequential steps: recruiter engagement may start before a formal application or receipt. Do not fabricate skipped events or dates.

Applied on records the known reported/evidenced submission date. Confirmed on records the exact-role receipt date. Outcome on records an explicitly known outcome date, not the application date or the date a user later confirmed an old outcome. Leave unknown dates blank. Status recorded at is the recording/reconciliation timestamp, not an invented historical event time. Status source identifies the actor or evidence; Status notes preserves conflicts and clarification needs.

A new scan must not reset an existing status. A later-arriving older acknowledgement must not regress In process, an offer or an outcome. Preserve human marks and historical evidence; flag contradictions instead of silently resolving them. Reopening/reapplication requires explicit user instruction or verified reopening and a fresh duplicate/eligibility check.

Count human/agent-reported Applied submissions toward company capacity even before a receipt; include later rejected/withdrawn submissions according to the actual policy. Uncertain attempts may also occupy capacity until reconciled. A temporary cooldown does not change lifecycle status or relevance and does not exclude an Allow company from scanning.

During migration, preserve original combined status/date text and legacy pipeline values. Map ambiguous Pending using evidence, not an assumed meaning. Do not rescore fit or infer resume readiness from file presence. Existing old Discovered/Rated values are input aliases for Queued/Reviewed only where supported; future writes use Lifecycle status. Manual cell edits have no automatic audit/timestamp trigger unless a runtime has explicitly installed one.
