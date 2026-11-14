# Reviewer: assess and route candidates

For a short-command invocation, use [../COMMANDS.md](../COMMANDS.md) to recover private context, queue, attempts and checkpoints, persist verified outputs/handoff, and stop after this stage.


Input: Queued rows or review_pending pre-submission records, full official JDs, private career goals, latest editable Google Doc master resume, exact-role history and review policy/version. Review-owned Needs review records are retryable after relevant evidence changes or explicit requeue. Legacy shortlist commands route here.

Select the requested batch and checkpoint completed job keys; leave the remaining queue visible. Verify the requisition and full responsibilities/qualifications. Use current verified cached full text or refresh it under scan freshness rules. Missing, blocked, summary-only or wrong-role descriptions stay retryable; do not manufacture a rating. Record role eligibility separately from fit and company cooldowns.

Score two independent axes:

| Axis | High — good fit | Medium — borderline/adjacent | Low — clear poor fit |
|---|---|---|---|
| Career fit | Strong alignment with the user's stated career direction, desired scope/seniority, domains and preferences | Plausible alignment with material tradeoffs needing judgment | Clear mismatch with stated direction/preferences |
| Resume fit | Strong demonstrated evidence in the master for the role's central responsibilities and qualifications | Transferable/adjacent evidence with material gaps | Little relevant demonstrated evidence for central requirements |

Use Unresolved when necessary evidence is missing. Career goals describe preferences, not candidate experience. The JD describes employer requirements, not facts to copy into the resume. Do not infer skills, tenure, credentials or achievements absent from the master.

Apply the explicit decision rule:

- Career fit High OR resume fit High → Shortlisted. State which axis qualifies it and disclose the other axis's gaps/unknowns.
- Both axes Low, after a completed review → Not a fit, with evidence.
- No High and at least one Medium/Unresolved, or unverified full JD/requisition identity → Needs review, next_owner Reviewer, with a specific blocker. Do not convert ambiguity to a permanent negative.
- Eligibility blockers remain separate even on a Shortlisted role and must be resolved before application. A match does not waive a requirement or permit unsupported resume claims.

A valid full JD/identity is required before a positive decision. An unresolved other axis does not negate a supported High; disclose it and block any downstream work that requires the missing evidence. Save both scores, axis-specific rationale in fit_rationale, material gaps, eligibility, review time, career-criteria version, master version and JD hash/reference. Keep any legacy overall relevance score as history; do not assume it represents both new axes. Clear review_pending only after the review/exception has been persisted with its new versions. Report Shortlisted / Not a fit / Needs review counts and why the positive branch qualified.

Never reset later application states or user dispositions during re-review. Do not advance already submitted, active, offered, accepted, rejected, withdrawn, user-declined, closed, duplicate or Submission uncertain exact roles. Reconcile submission-history Needs review through Tracker before any preparation/application advancement. Reconsider completed decisions only on relevant changed inputs or explicit user instruction. Record but do not silently reopen the prior application cycle.
