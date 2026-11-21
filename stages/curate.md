# Curate: company targeting and evidence

Use WORKFLOW.md, CAREER-GOALS.md and DATA.md. Curate maintains company facts and proposes companies; humans control Allow/Exclude. It does not manage applications or research application limits/cooldowns.

## Scope and inputs

Read current Companies, Sources, company snapshots in History, Career Goals and Settings.company_policy.discovery. Freeze company IDs and current goals/company preference versions in the Run. Preserve existing targeting, notes, historical records and source identities. Never automatically change an existing Allow or Exclude decision. Respect any permanent block retained in a legacy base without recreating retired hold fields in new setups.

## Company evidence

Refresh missing, conflicting or changed facts needed for Review: official company identity, product/customer space, funding maturity and verified current parent when applicable. Prefer official announcements, investor/company pages, filings and reputable reporting with attributable evidence. Search results are leads, not proof. Separate retrieval time from the reported event date, historic fundraising from current parent status, and investment type from verified maturity. Never infer a labelled round from an amount or call inaccessible research complete.

Store the compact Funding stage and a Company evidence link. Full sources, exact round labels, amounts/dates where useful, parent history, uncertainty and advisory company-fit reasoning belong in the versioned evidence and History, not extra columns. Review independently applies current goals to these facts; Curate's advisory assessment is not a role score. A company may be a direct employer, a discovery source, or both, as the current goals specify. For investment firms, distinguish their own staff roles from portfolio-company jobs. Never attribute portfolio jobs to the investor or interpret fund sizes/raises as operating-company funding rounds. Apply each company-stage requirement only to the company types the goals cover; do not fabricate a startup stage for an investment firm.

## Discovery

Use the current goals and registered public sources in Settings.company_policy.discovery. Discovery means finding matching companies absent from the current list, regardless of funding-announcement age. A funding-news lookback is a source-retrieval window, not an admission rule. Preserve any applicable maturity minimum from current goals.

Register each source by stable key, official URL or explicit public-search plan, reader strategy, checkpoint and access verification. Official investor portfolios/company directories, company announcements, filings and reputable funding reporting can complement each other. Read sources, not just snippets, before accepting company facts. Missing essential preferences or all inaccessible sources block discovery; one failed source stays a reported gap while others proceed.

Enumerate every page/item of each configured catalog to its verified end. For exploratory web searches, retain the queries and visited sources and label coverage exploratory; never claim exhaustive internet coverage or invent a total. Record those two coverage types separately. A normal scheduled cadence may defer an unchanged source only with a verified checkpoint; an explicit user request to discover companies runs discovery now. There is no default hidden cap on discoveries.

Verify employer identity, company fit and official careers boards/regions. Deduplicate against current company keys and source identities. Qualifying companies become Proposed with provenance. Existing human Allow/Exclude choices remain unchanged. A Proposed company's draft Sources do not enter Scan until human Allow and verification. Report one batch of proposals for human choices; the checkpoint can pause only that new-company branch while existing Allow companies continue.

## Persist and hand off

One writer rereads affected rows, preserves Manual notes and captures only Feedback through the verified procedure, writes intended deltas and verifies them. Use merge_company_state for company metadata and link the event to the Run, never to a fake application. Preserve earlier funding/company/origin sections when changing one part.

Run checkpoint stages.curate tracks company research and discovery separately, coverage, refreshed/unchanged/unresolved counts, Proposed companies, pending questions and next actions. Discovery cursors in Settings.company_policy.discovery.checkpoints advance only after verified complete coverage. An interrupted page/write resumes from verified state without duplicate proposals. Incomplete required parts mean Partial/Blocked. Save company evidence identities for downstream revalidation; standalone Scan/Review can use this handoff without rerunning Curate. Report results and release ownership when the invocation ends.
