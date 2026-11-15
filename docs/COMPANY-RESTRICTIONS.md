# Company application restrictions

Store per-company limits and cooldowns in Companies (legacy name Target Companies), separately from Search status and Pool. A temporary hold does not exclude a company from scanning. Map the optional fields in templates/companies.csv to live headers; extend the existing table during authorized setup without replacing company data. Blank policy values mean unrecorded, not zero or unlimited. New rows start with Application hold status “Not assessed”.

| Field | Meaning |
|---|---|
| Max applications | Confirmed positive whole-number limit within the specified window. |
| Application window (days) | Day-based window length; use details for calendar/fixed reset boundaries. |
| Application window type | Rolling / Calendar / Fixed / Unconfirmed. |
| Rejection cooldown (days) | Confirmed wait after a qualifying rejection; details specify elapsed/calendar days and trigger. |
| Restriction scope | Company / Role family / Exact role / Mixed / Unconfirmed. Mixed rules need separate scopes in details. |
| Last rejection date | Actual qualifying event date/time and evidence; not itself a company-wide ban. |
| Apply blocked until | Earliest date/time after all applicable restrictions; prefer ISO8601 with an explicit offset. |
| Application hold status | Not assessed / No known hold / Held / Needs clarification; separate from role fit and lifecycle status. |
| Restriction details / source | Published rule or explicit user instruction, evidence/date, duration basis, exceptions, affected roles, reset times and additional limits. |
| Restriction last verified | When the rule/evidence was actually reviewed. |
| Restriction timezone | Confirmed IANA timezone for boundaries/date-only inputs; do not assume the Sheet's timezone. |

Do not infer a company cooldown from a generic rejection or invent a waiting period. Preserve exact-role dispositions. Confirm scope, duration, trigger and rolling/calendar/fixed semantics. If multiple constraints apply, all must allow the submission; a future date is only an estimate until the quota is recomputed. Multiple windows or mixed scopes must be recorded in details and not silently collapsed to one rule.

Count distinct human/agent-reported or evidenced submission events in the applicable window (including Applied without a receipt), including applications subsequently rejected or withdrawn unless the rule explicitly restores capacity. Deduplicate duplicate tracker rows and receipts; include known external/manual applications. Uncertain attempts may occupy capacity but must not be marked Applied. If allowance cannot be proven, reconcile before submitting. Determine the next rolling-window opening when enough events expire, not necessarily when only the oldest event expires.

Keep scanning and inventorying plausible candidates, and reviewing for Queued approval, while an application hold applies. Record the hold separately; do not lower relevance because of a temporary restriction. Recheck the live company rule, current submission history, scope, timezone and all pause/stop controls immediately before Submit, using one submission worker. An elapsed date does not authorize auto-apply, prove role eligibility, or override any remaining limit. Known restrictions with unresolved dates/scope remain held for clarification.

Before enabling auto-apply, configure a private answer bank, supported sites and submission cap, and connect an authorized browser runtime. Test one form, receipt capture, duplicate prevention, a simulated uncertain submission, and the live pause control. Use one submission worker.

