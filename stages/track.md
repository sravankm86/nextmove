# Tracker: reconcile recruiting updates

For a short-command invocation, use [../COMMANDS.md](../COMMANDS.md) to recover private context, queue, attempts and checkpoints, persist verified outputs/handoff, and stop after this stage.


Input: configured read-only recruiting mailbox(es), Applications and exact-role aliases/history, prior event IDs and a durable successful mailbox checkpoint. Prioritize Applied, Confirmed, In process, Offer and Submission uncertain, but inspect relevant exact-role messages about terminal records as well; do not miss an explicit correction by filtering only active states.

Use an overlapping time window from the last successful checkpoint, enumerate all matching result pages and deduplicate by source message/event identity plus job key. Do not rely on unread status or a single results page. Keep mail bodies, private links and personal data outside public Git and bulk model context. Missing access, incomplete pages and checkpoint gaps must be reported; do not advance the successful fetch checkpoint beyond unread or unstaged coverage. Ambiguous events may advance the fetch watermark only after being durably saved to an unresolved-event queue; they remain unreconciled and are retried when identity/evidence changes. Fetch coverage is not proof that every event has a resolved role.

Read the relevant message/thread and distinguish new text from quotes/forwarded history. Match exact requisition/job identity, or an unambiguous company-plus-role with sufficient evidence. Company-only acknowledgements and ambiguous titles remain unmatched/ambiguous, not attributed to every company application.

Propose evidence-backed transitions:

- Exact-role receipt → Confirmed, with the known confirmation date.
- Actual recruiter engagement, screening, assessment, interview or scheduling → In process.
- Explicit offer/acceptance/rejection/withdrawal/cancellation → the corresponding Offer, Accepted, Rejected, Withdrawn or Closed state.
- Uncertain submission → resolve only with reliable evidence; absence of an email is not evidence that no submission occurred.
- Conflicting or ambiguous events → retain current state and record a scoped Tracker blocker / next owner; do not overwrite a stronger known outcome.

Preserve actual event time separately from received/recorded time. An older acknowledgement cannot regress a later rejection, active interview or offer. A later email is not automatically a reversal: contradictory events require explicit correction evidence or user clarification. Preserve user dispositions and history; do not silently reopen or reapply to terminal roles.

Send findings through the coordinator's single writer, which rereads current rows and reconciles human edits. Record current state, source/private evidence, known event dates, status recorded time and idempotent transition events in the authorized store. Repeated polling must not duplicate transitions, confirmations or quota counts.

A rejection does not imply a company-wide cooldown. Update company restriction state only under a confirmed applicable rule with known scope, trigger, duration, timezone and evidence; otherwise flag clarification. Do not alter fit ratings merely because of a receipt or outcome.

Save a mail audit and checkpoint in the existing authorized store: mailbox scope/window, pages/messages, matched/unmatched/ambiguous/duplicate events, transitions, failures and last successful coverage. Mail coverage is distinct from scan coverage. Remain read-only on mail: do not send, draft, label, archive, delete or contact recruiters without a separate explicit instruction.

Tracking runs independently of the Applier and may also be an explicit preflight reconciliation. It never submits an application or treats cooldown expiry as submission authorization.
