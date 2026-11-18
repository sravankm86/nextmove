# Curate: company targeting and evidence

Use WORKFLOW.md, CAREER-GOALS.md and DATA.md. Curate maintains company facts and proposes companies; humans control Allow/Exclude. It does not manage applications or research application limits/cooldowns.

## Scope and inputs

Read current Companies, Sources, company snapshots in History, Career Goals and Settings.company_policy.discovery. Freeze company IDs and current goals/company preference versions in the Run. Preserve existing targeting, notes, historical records and source identities. Never automatically change an existing Allow or Exclude decision. Respect any permanent block retained in a legacy base without recreating retired hold fields in new setups.

## Company evidence

Refresh missing, conflicting or changed facts needed for Review: official company identity, product/customer space, funding maturity and verified current parent when applicable. Prefer official announcements, investor/company pages, filings and reputable reporting with attributable evidence. Search results are leads, not proof. Separate retrieval time from the reported event date, historic fundraising from current parent status, and investment type from verified maturity. Never infer a labelled round from an amount or call inaccessible research complete.

Store the compact Funding stage and a Company evidence link. Full sources, exact round labels, amounts/dates where useful, parent history, uncertainty and advisory company-fit reasoning belong in the versioned evidence and History, not extra columns. Review independently applies current goals to these facts; Curate's advisory assessment is not a role score. Investment firms used for portfolio discovery remain sources rather than being misclassified as hiring employers.

## Discovery

Use registered feeds and cadence in Settings.company_policy.discovery, including its verified minimum funding stage from Career Goals. No repository funding default. Missing required preferences or feed configuration blocks discovery only; record the gap and continue independent company research. A configured cadence permits verified deferred discovery, never fabricated new coverage.

Enumerate every page/item in each selected feed's checkpoint interval. Use repeatable readers where available. Verify candidate companies and official careers boards, including regions, before recording them. Deduplicate against current company keys and source identities. Only evidence-backed qualifying discoveries become Proposed, with known origin and source references preserved. Existing Allow/Exclude choices remain unchanged. Draft Sources for Proposed companies are not scan-eligible until human Allow and board verification.

## Persist and hand off

One writer rereads affected rows, preserves Manual notes except through verified feedback capture, writes intended deltas and verifies them. Use merge_company_state for company metadata and link the event to the Run, never to a fake application. Preserve earlier funding/company/origin sections when changing one part.

Run checkpoint stages.curate tracks company research and discovery separately, coverage, refreshed/unchanged/unresolved counts, Proposed companies, pending questions and next actions. Discovery cursors in Settings.company_policy.discovery.checkpoints advance only after verified complete coverage. An interrupted page/write resumes from verified state without duplicate proposals. Incomplete required parts mean Partial/Blocked. Save company evidence identities for downstream revalidation; standalone Scan/Review can use this handoff without rerunning Curate. Report results and release ownership when the invocation ends.
