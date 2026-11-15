# A readable application tracker

Use short, structured values in the columns people review. Keep exact job descriptions, salary conditions, location restrictions and review evidence in the linked Drive capture and existing agent-detail fields. A shorter display must not reduce the evidence available to Review, Prepare or Apply.

## Everyday view

Create a grid named **Review** with these columns in this order. Keep **All fields** as a separate maintenance view; do not delete workflow fields to hide them.

1. Application
2. Lifecycle status
3. Manual notes
4. Posted salary range
5. Additional compensation
6. Location
7. Work arrangement
8. Job posted date
9. Career fit
10. Resume fit
11. Blocker
12. Job description link
13. Resume link

Application already contains company and role. Separate company/role columns remain available for filters and expanded records. Applied on, Confirmed on and Outcome on can be added to a submission-tracking view. Gates, hashes, policy versions, source links, resume verification and submission-attempt state belong in agent details.

Configure field visibility/order through a supported Airtable view editor or authenticated UI. Some connectors can change records and fields but cannot change views. In that case complete the supported data work, save the exact remaining UI step in Runs, and report it. A new field is not proof it was positioned next to status.

## Compact values

| Field | Format |
|---|---|
| Posted salary range | `USD 260,000–340,000`; ranges only, with currency and `/h` or `/mo` when applicable. Blank when no reliable range is stated. |
| Additional compensation | Multiple select: Equity, Bonus, Commission, Bonus or commission, Not stated. |
| Location | Short place values, separated by semicolons when each value includes a city/country comma. No JSON, street directions, postal codes or prose. |
| Work arrangement | Remote, Hybrid, On-site, Unspecified. Do not infer remote eligibility merely from a remote salary band. |
| Availability | Open, Closed, Unknown. Store the quote, URL and check time in evidence, not this display value. |
| Description status | Current, Captured, Historical, Missing, Unavailable. Historical never establishes current availability. |
| Blocker | A concise next action. Detailed rationale belongs in evidence/expanded fields. |

Use `scripts/tracker_values.py` for supported deterministic formats; verify unfamiliar source structures rather than inventing a value. Preserve every distinct applicable band separately. Never manufacture a minimum/maximum envelope across different locations, currencies or levels. The compact salary field is a display summary, not enough to establish a career compensation gate. Preserve each band’s location, currency, period, base-versus-total basis and source in Salary details or the exact Drive capture. A mention of equity/bonus can be conditional; the label does not promise a grant. Absence of a mention means Not stated, not No.

Read current evidence before refreshing these values. Reuse verified captures where available; do not repeat the whole Scan or change fit/status decisions merely to reformat fields. Preserve before/after values in History or an indexed private migration artifact. Never put raw source JSON into display columns.

## Manual notes and feedback

Manual notes belongs to the human. Resolve the legacy alias Status notes by field ID; do not create competing note fields. Agents read it with current Lifecycle status at startup and before relevant writes. They must not overwrite, clear, rewrite or use it as an output log.

Respect a manual disposition on that job. When feedback changes, record the observed note/status and its fingerprint under `Evidence versions (JSON).manual_feedback`, plus a meaningful History event. Save observation time; do not invent the actual edit time or author. Read back the record before writing so a concurrent human edit is preserved. Blank notes do not invalidate a human status change.

Use comments such as “wrong function” as a candidate for the feedback process in SCAN-OPTIMIZATION.md. Verify the JD before treating it as a scanner mistake. A personal decline, missing evidence or career mismatch is not automatically a scan exclusion. Ask a targeted clarification only when an ambiguous note blocks the requested decision. Notes do not silently update Career Goals, authorize submissions, waive current review/resume evidence or supply resume facts. A manually selected Queued state still needs the acceptance checks before Prepare.

## Fields that can retire

Do not provision these old migration/display fields in a new installation:

- Legacy lifecycle status, Imported lifecycle status, Legacy pipeline stage, Legacy status / applied on: replaced by the canonical status and actual event dates.
- Migration key, Source record, Raw source record, Migration note: old import provenance; preserve an authorized recoverable archive before removal.
- Inventory job, Lifecycle Events, Work Items, Artifacts: references to the retired multi-table design. Inventory now lives in Applications; History and current Drive references replace the others.
- First-pass decision, First-pass reason: replaced by Scan evidence, Record kind and the canonical workflow states.
- Run ID, Source URL, Job posted text: legacy helpers superseded by versioned Run evidence, Sources/official job links and the posted date with exact source evidence. Verify each mapping before removal.

Existing installations must first check actual values, formulas, views, scripts, integrations and source references; retain exact private before-images and replacement mappings. Some live fields may have user-defined dependencies that the connector cannot inspect. Hide retirement candidates first when deletion/dependencies cannot be verified. Never retire empty resume verification, submission attempt, confirmation or outcome fields just because they have not been used yet: later stages require them.

The safe immediate simplification is the everyday view. Consolidating policy/version/evidence columns further is a separate migration: update every stage reader/writer and verify recovery before deleting any guard. Cosmetic cleanup must not weaken resume integrity, source coverage, human-history preservation or submission safety.
