# Apply

Default is preflight. A full Run, a Ready resume or a bare Apply command does not authorize unlimited submissions.

Require scripts/stage_state.py:apply_ready and all live authorization/form/restriction controls. Resolve outstanding evidence and require current scored Review before submitting. A prepared resume never waives salary or qualifications.

Read live pause/stop, explicit scoped authorization, answers, exact role history, whether the actual application form is accessible and accepting submissions, review/master/resume versions and the live company hold check below. Reconcile uncertainty. Generic rejection does not establish company-wide restriction; unknown rule/scope/boundary or answers block affected submissions. See stages/apply.md.

Only supported authorized browser actions may submit. Follow RESUME-FILES.md to verify the exact PDF file/version. Before Submit, persist/read back Submission attempt key and Submission run on Applications and a durable History intent/checkpoint with exact role, PDF file identity/version and approved answers under DATA.md. Reconcile an existing attempt before retry even if the UI status says Ready. Capture actual success/receipt, date and evidence. Definite submission → Applied. Exact-role receipt adds Confirmation reference/History while staying Applied. Unresolved possible submission stays at the last verified pre-submit stage with prominent Agent notes and a blocking saved attempt; never invent Applied or Ready. Never retry blind or infer non-submission from absent mail.

Keep meaningful attempt/receipt events in History and current state on Applications. Runs records stage progress and blockers. No general Task Attempts table is needed.

Check exact company-scoped employer role IDs or canonical job links against all recorded applications, including rejected history and unresolved attempts. Do not compare every regional variant or infer duplicates by title/description. Missing migration identity needs reconciliation only for affected records.

Use one submission writer and respect human edits. Do not send recruiting mail. Single-stage invocation stops at its handoff; a full Run can continue Track or other unaffected authorized work while reporting blocked submissions.

Before advancing, verify that the accepted review still matches the current goals, role policy, master and job description. Changed inputs require affected review/re-preparation, not silent reuse. Preserve existing submitted/terminal history.

Maintain the current concise result, unresolved material issue and next action in Agent notes, preserving previous values in History. Never overwrite Manual notes or erase unresolved company restrictions. Detailed evidence belongs in linked content and stage metadata.

There is no stored Availability or Last seen at field. Check the actual form during preflight/submission; unavailable forms block that attempt and are reported in Agent notes/History. Do not invent a successful submission or start recurring closure monitoring.

# Company application holds

Curate (stages/curate.md) owns company policies and writes Application hold status and Apply blocked until. Apply does not edit policy fields; it rechecks immediately before every Submit, using one submission worker:

1. Reread the company row, all Applied rows, unresolved attempt keys, known external applications and rejection events in History for that company.
2. Call `scripts/company_policy.py:apply_allowed` with the Settings `company_policy` personal limit (or the Career Goals override pinned in the Run). Submit only when it returns No known hold. Held, Blocked (permanent), Needs clarification and Not assessed all block the affected submissions; save the returned reasons in Agent notes and History.
3. Check Role family / Exact role rules in Restriction details / source against this role. Any unresolved rule or boundary blocks that role.
4. If the result differs from the saved company hold, write the recomputed value with History so Curate and the next harness see it.

An elapsed Apply blocked until does not authorize submission, prove role eligibility or override another limit. A hold does not lower role fit or remove a role from Queued/Ready. Do not infer a company cooldown from a generic rejection; report new policy evidence to Curate through History.

Before enabling auto-apply, configure a private answer bank, supported sites and submission cap, and connect an authorized browser runtime. Test one form, receipt capture, duplicate prevention, a simulated uncertain submission, and the live pause control. Use one submission worker.

Pass the current named Companies records to apply_ready/resume_ready as well as running the separate live company_policy.apply_allowed hold check. A valid score/PDF cannot bypass human Exclude, Proposed or a permanent block. Temporary holds block submission only, not prior fit assessment or resume preparation.
