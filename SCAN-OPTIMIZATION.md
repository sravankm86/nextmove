# Improve Scan from Review outcomes

Use existing Applications, Runs, Settings and History; no new feedback table, general task engine or model API is required. This is an agent-run improvement loop, not an installed background trainer.

## Capture the right signal

Review keeps Decision category and Assessment summary on Applications and exact reason/evidence/version metadata in History and indexed Drive content under STAGE-STATE.md. Scan run/Review run identify the fixed context; never recreate retired reason/version columns. Include scan/review policy versions, JD hash/reference, goals/master versions where relevant, and actual outcomes. Keep scan evidence separate from final eligibility evidence.

Manual notes is the inline human-feedback input. Observe changed note/status fingerprints and preserve the original wording under TRACKER.md; never clear the field after processing it. Classify human dispositions as human_choice unless independent JD evidence establishes a different category. Feedback does not itself activate a new exclusion rule.

| Category | Interpretation for Scan |
|---|---|
| role_function, seniority_scope | Potential basic-screen false positive; inspect transferable evidence |
| career_domain, career_industry, career_vertical, career_stage, career_geography, career_compensation, career_other | Review-owned preferences; do not automatically add scan exclusions |
| fit | Review assessment, not proof of wrong PM family/level |
| missing_evidence | Unresolved, not a negative training label |
| availability, duplicate | Source freshness/identity problem, not semantic relevance |
| human_choice | Human disposition, not an inferred role exclusion |
| approved | Review-approved positive to protect in regression checks |

Not queued is not a single negative class. Preserve uncertainty, human outcomes and changes to criteria. Do not delete rejected candidates to hide false positives or lower counts; apply only an explicit retention policy with recoverability.

## Evaluate a proposed change

At a Review handoff, summarize counts/reasons by company/source and scan version; small samples are qualitative evidence, not statistical certainty. Store compact findings/proposed changes in the Run checkpoint and a meaningful History event. Local execution is an accelerator; durable evidence stays in Airtable/registered Drive.

For recurring clear role/scope mistakes, propose the smallest explainable keyword or semantic adjustment. Prefer positive alias coverage and evidence-based disambiguation over broad negative keywords. Career screening remains in Review unless the user explicitly changes the stage boundary.

Before activation, replay against reviewed eligible positives (including eligible Not aligned roles), known false positives, ambiguous/flat/localized titles and a stratified independent sample of source rejects/near-misses. Compare baseline/proposed candidate counts, PM/scope recall, false positives, queue yield and unresolved cases. Label independently of the rule under test; do not treat old scan decisions as gold. Separate a held-out check from examples used to tune the rule. If rejected examples were not retained, re-enumerate official sources and disclose closed-posting gaps; do not silently create a raw shadow inventory.

Primary target is eligible-PM recall, not queue yield. Every known eligible regression must be fixed or explicitly accepted by the user; unknown cases cannot be counted as safe exclusions. Without adequate evidence keep the current screen and save the proposal. A low queue rate caused by career preferences does not justify narrowing Scan.

## Activate and monitor

A validated behavior change needs an authorized instruction/Settings update, a version identifier and a History event linking evaluation evidence. Do not self-modify hidden prompts. Version references must be durable and recoverable by another harness. Git updates require repository write capability; otherwise hand off the concrete proposal.

Apply active criteria on the next scan, recheck affected catalog slices and preserve prior row provenance. Changed evidence permits targeted re-review; unchanged rejections do not churn through the queue. Sample rejects after changes. A discovered eligible false negative requires widening/reverting the rule and rechecking the affected scope. Do not claim true precision/recall without suitable independent labels and disclosed uncertainty.
