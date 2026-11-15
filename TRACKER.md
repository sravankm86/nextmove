# The 36-field application tracker

Applications uses the36 fields in scripts/stage_state.py:CORE_FIELDS and contracts/core-schema.json. Four Run links replace repeated stage context columns. History stores bounded versioned stage metadata and Drive holds detailed content. Read STAGE-STATE.md before stage work. Native record IDs are technical identities; Job key is a validated canonical business identity, with explicit unmatched legacy exceptions.

## Everyday view

Show Application, Lifecycle status, Manual notes, Posted salary range, Additional compensation, Location, Work arrangement, Job posted date, Career fit, Resume fit, Blocker, Job description link and Resume link in that order. Manual notes belongs beside status. This is a view over the36-field physical schema, not a substitute for retiring columns after a verified migration.

Some connectors cannot configure views or delete/retype fields. Complete supported data/schema work and report the exact remaining UI action. Existing extra columns may remain during cutover; current writers ignore them and never recreate retired fields.

## Compact values and full evidence

Salary contains only distinct advertised ranges, currency and rate unit where applicable. Missing ranges stay blank. Additional compensation uses Equity, Bonus, Commission, Bonus or commission, Not stated; mentions may be conditional and do not promise a grant. Location contains short places, never source JSON or directions. Work arrangement is Remote/Hybrid/On-site/Unspecified and Availability is Open/Closed/Unknown. A remote pay band does not establish remote eligibility.

Use scripts/tracker_values.py for supported formats and verify unfamiliar structures. Never manufacture salary envelopes across currencies, levels or locations. Job evidence and its exact indexed capture preserve full salary conditions, restrictions, JD and assessment reasoning. Assessment summary gives the current explanation; Blocker gives the current next action. Do not duplicate full source content into display columns.

## Human feedback and readiness

Manual notes belongs to the human. Agents read it with current status and never overwrite, clear or rewrite it. Save changed observed notes/status and their fingerprint in stage metadata/History, recording only known edit times/actors. Blank notes do not invalidate a human status change. A personal decline does not automatically become a scanner error or global criterion.

Lifecycle, eligibility, career gate and fit are separate facts. Queued alone is not approval: verify the explicit review snapshot, fixed decision rules and current goals/master/JD. Ready alone is not verified PDF identity or submission authorization. An existing attempt requires reconciliation even after a manual status reset. Preserve submitted PDF identity separately from the current editable resume reference.

## Retirement and compatibility

Use the installation's verified migration manifest. Preserve exact prior values and indexed content, migrate required state to History and fixed context snapshots to Runs, backfill stage links, update every reader/writer/alias/schema/template/check, and replay guards after removing proposed fields from a copy. Preserve actual event times and explicit unknowns. Then those columns may retire.

Keep Company, Job key, current lifecycle/manual notes, independent gates/fit, Job evidence, current PDF version/verification, Submission attempt key and the real History relationship. The empty old Lifecycle Events text helper is not the reciprocal History.Application link.

Resolve company identities before removing Company name; historical identities do not imply Allow. Native IDs remain available without a Record ID formula. Posted/application/observation dates are not database creation/update time. Empty future guards remain where required by the36-field profile.

The same six tables support one full agent invocation or separately launched stages. Schema migration changes storage, not role criteria, recall, resume truthfulness, company restrictions, live controls or submission permission.
