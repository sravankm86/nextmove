# Apply

Default is preflight. A full Run, a Ready resume or a bare Apply command does not authorize unlimited submissions.

Require scripts/stage_state.py:apply_ready and all live authorization/form/restriction controls. Resolve any provisional base-pay check through current verified Review before submitting. A prepared resume never waives salary or qualifications.

Read live pause/stop, explicit scoped authorization, answers, exact role history, whether the actual application form is accessible and accepting submissions, review/master/resume versions and every applicable company quota/cooldown. Reconcile uncertainty. Generic rejection does not establish company-wide restriction; unknown rule/scope/boundary or answers block affected submissions. See stages/apply.md.

Only supported authorized browser actions may submit. Follow RESUME-FILES.md to verify the exact PDF file/version. Before Submit, persist/read back Submission attempt key and Submission run on Applications and a durable History intent/checkpoint with exact role, PDF file identity/version and approved answers under DATA.md. Reconcile an existing attempt before retry even if the UI status says Ready. Capture actual success/receipt, date and evidence. Definite submission → Applied. Exact-role receipt adds Confirmation reference/History while staying Applied. Unresolved possible submission stays at the last verified pre-submit stage with prominent Agent notes and a blocking saved attempt; never invent Applied or Ready. Never retry blind or infer non-submission from absent mail.

Keep meaningful attempt/receipt events in History and current state on Applications. Runs records stage progress and blockers. No general Task Attempts table is needed.

Check exact company-scoped employer role IDs or canonical job links against all recorded applications, including rejected history and unresolved attempts. Do not compare every regional variant or infer duplicates by title/description. Missing migration identity needs reconciliation only for affected records.

Use one submission writer and respect human edits. Do not send recruiting mail. Single-stage invocation stops at its handoff; a full Run can continue Track or other unaffected authorized work while reporting blocked submissions.

Before advancing, verify that the accepted review still matches the current goals, role policy, master and job description. Changed inputs require affected review/re-preparation, not silent reuse. Preserve existing submitted/terminal history.

Maintain the current concise result, unresolved material issue and next action in Agent notes, preserving previous values in History. Never overwrite Manual notes or erase unresolved company restrictions. Detailed evidence belongs in linked content and stage metadata.

There is no stored Availability or Last seen at field. Check the actual form during preflight/submission; unavailable forms block that attempt and are reported in Agent notes/History. Do not invent a successful submission or start recurring closure monitoring.

# Company application restrictions

Store per-company limits and cooldowns in Companies (legacy name Target Companies), separately from Search status. A temporary hold does not exclude a company from scanning. Map the optional fields in templates/companies.csv to live headers; extend the existing table during authorized setup without replacing company data. Blank policy values mean unrecorded, not zero or unlimited. New rows start with Application hold status “Not assessed”.

| Field | Meaning |
|---|---|
| Max applications | Confirmed positive whole-number limit within the specified window. |
| Application window (days) | Day-based window length; use details for calendar/fixed reset boundaries. |
| Application window type | Rolling / Calendar / Fixed / Unconfirmed. |
| Rejection cooldown (days) | Confirmed wait after a qualifying rejection; details specify elapsed/calendar days and trigger. |
| Restriction scope | Company / Role family / Exact role / Mixed / Unconfirmed. Mixed rules need separate scopes in details. |

| Apply blocked until | Earliest date/time after all applicable restrictions; prefer ISO8601 with an explicit offset. |
| Application hold status | Not assessed / No known hold / Held / Needs clarification; separate from role fit and lifecycle status. |
| Restriction details / source | Published rule or explicit user instruction, evidence/date, duration basis, exceptions, affected roles, reset times and additional limits. |

| Restriction timezone | Confirmed IANA timezone for boundaries/date-only inputs; do not assume the Sheet's timezone. |

Do not infer a company cooldown from a generic rejection or invent a waiting period. Preserve exact-role dispositions. Confirm scope, duration, trigger and rolling/calendar/fixed semantics. If multiple constraints apply, all must allow the submission; a future date is only an estimate until the quota is recomputed. Multiple windows or mixed scopes must be recorded in details and not silently collapsed to one rule.

Count distinct human/agent-reported or evidenced submission events in the applicable window (including Applied without a receipt), including applications subsequently rejected or withdrawn unless the rule explicitly restores capacity. Deduplicate duplicate tracker rows and receipts; include known external/manual applications. Uncertain attempts may occupy capacity but must not be marked Applied. If allowance cannot be proven, reconcile before submitting. Determine the next rolling-window opening when enough events expire, not necessarily when only the oldest event expires.

Keep scanning and inventorying plausible candidates, and reviewing for Queued approval, while an application hold applies. Record the hold separately; do not lower relevance because of a temporary restriction. Recheck the live company rule, current submission history, scope, timezone and all pause/stop controls immediately before Submit, using one submission worker. An elapsed date does not authorize auto-apply, prove role eligibility, or override any remaining limit. Known restrictions with unresolved dates/scope remain held for clarification.

Before enabling auto-apply, configure a private answer bank, supported sites and submission cap, and connect an authorized browser runtime. Test one form, receipt capture, duplicate prevention, a simulated uncertain submission, and the live pause control. Use one submission worker.

Actual rejection event times and rule-verification times are recorded in History, not duplicate company date columns. Read all applicable known events and verify restrictions immediately before Submit. If post-interview events are outside tracking scope, missing rule-trigger evidence must be clarified rather than assumed absent.
