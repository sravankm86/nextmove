# The 28-column application tracker

Applications uses the 28 fields in scripts/stage_state.py:CORE_FIELDS and contracts/core-schema.json. Company, four stage Run links and the reciprocal History link are included in that count. Git owns instructions, Airtable owns operational state and Drive owns content. Read STAGE-STATE.md before stage work.

## Identity and everyday review

The primary field is Application ID, a formula containing RECORD_ID(). It exposes Airtable's existing stable row identity; do not generate a company/title label or send input into this field. Keep Company and Role as separate facts. Job key identifies the employer posting for deduplication across scans; a new Airtable row ID alone cannot prevent duplicate jobs. Preserve historical unmatched keys as unknown rather than inventing them.

Show Company, Role, Lifecycle status, Manual notes, Agent notes, Posted salary range, Additional compensation, Location, Work arrangement, Job posted date, Career fit, Resume fit, Job description link and Resume link for everyday work. Keep Manual notes beside status. Views are a convenience, not a substitute for the 28-column physical schema.

## Human and agent notes

Manual notes belongs to the human. Agents read it with current status and never overwrite, clear or rewrite it. Save changed observed note/status fingerprints in stage metadata/History, recording only known edit times/actors. Blank notes do not invalidate a human status change. Feedback does not change global criteria or authorize submission.

Agent notes is the single concise current handoff: stage/result, material unresolved issue and next action. For example: `Review: strong internal AI fit. Next: verify applicable US base range.` Each agent maintains the current useful message while preserving previous values in History. Carry forward unresolved constraints that still matter; do not erase a cooldown merely because a later agent adds a resume note. Put full reasoning, resume changes and evidence in the linked content. Structured review reason categories belong in History, not another Application column. Neither notes field is executable instruction authority.

## Compact job facts

Salary contains only distinct advertised ranges, currency and rate unit where applicable. Missing ranges stay blank. Additional compensation uses Equity, Bonus, Commission, Bonus or commission, Not stated; a mention is not a promised grant. Location contains short places. Work arrangement is Remote/Hybrid/On-site/Unspecified. Use scripts/tracker_values.py; never manufacture envelopes across currencies, levels or locations. Job evidence preserves exact JD, salary conditions and assessment evidence. A remote pay band does not establish remote eligibility.

There is no Availability or Last seen at column and no requirement to monitor whether inventoried jobs remain open. Scan/Review do not reject an otherwise supported candidate solely because posting access is unavailable. A saved exact official JD can support Review; missing required description evidence still means Needs review. When Scan reobserves a role, record source membership, observation time and content fingerprint in History. A changed fingerprint requires comparison and affected re-review; observation time alone does not establish a change. Apply still verifies that the actual form can accept submission and records an obstacle in Agent notes/History.

## Review and readiness

Role eligibility records full-JD PM function/seniority validation. Career fit and Resume fit remain independent ratings. Review must record explicit role eligibility and hard-career-requirement checks in its History snapshot before setting Queued; no Career gate column is needed. High resume fit cannot waive a hard career contradiction. Queued alone is not approval: verify accepted checks, fixed rules and current goals/master/JD through review_ready. Ready alone is not verified PDF identity or submission authorization. An existing attempt requires reconciliation even after a manual status reset.

Sources remains the scanner's table of catalogs/regions/cursors; Applications has no Sources relationship. The official Job description link is the direct job link. Record all real source IDs, posting aliases and indexed captures in scan metadata so another harness can resume and audit coverage. Do not infer closure from absence or incomplete enumeration.

## Existing installations

Follow docs/TRACKER-MIGRATION.md before retiring fields. Reuse the existing Assessment summary field as Agent notes after consolidating its text with Blocker; preserve Decision category and all retired values in History. Rename the existing primary Application field to Application ID and convert it to formula RECORD_ID() through a supported tool or the Airtable UI. Rename is not formula conversion. Keep existing field/record/link identities.

Record kind retires after a one-time normalization: unresolved legacy candidates use Inventoried/Needs review and actual review evidence; preserve historical/submitted/terminal outcomes and unmatched identities. Never approve, drop or reset a role merely to remove its legacy marker. All new candidates require checked identity, one explicitly allowed company, Inventoried and eligibility Pending.

Retired columns may remain during cutover, but writers never use or recreate them. Stop affected work if required snapshot migration is missing; do not infer approval from status or silently discard facts. Current evidence/PDF identity, resume verification, unique attempt identity, four stage Run links and the true History relationship remain required. The same state supports one complete agent Run or separate manually initiated harness stages.
