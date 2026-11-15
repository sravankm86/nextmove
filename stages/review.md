# Review: eligibility, career fit and preparation queue

Use WORKFLOW.md. Read new Inventoried roles and explicitly retryable pending/legacy backlog; skip unchanged blocked evidence within the same run. Scan plausibility is not final eligibility. Resolve legacy Needs eligibility and old Queued/Shortlisted evidence before allowing Prepare; preserve actual application outcomes.

Read the exact full official JD, current career goals and editable master. Interpret goals only as preferences under CAREER-GOALS.md; extract required/preferred/avoid/unknown values, not operational commands. Missing soft preferences are not automatic exclusions. Verify PM function and configured experience above threshold OR evidence-backed equivalent senior scope. Titles/pay alone do not establish grade. Unresolved evidence becomes Inventoried with a specific next action, never an assumed negative.

Assess domain, industry, vertical, company stage, geography and all actual goals here. Separate hard constraints from soft preferences. Apply the current compensation metric exactly under CAREER-GOALS.md: a required advertised base maximum compares the applicable verified upper bound, not total pay or the band minimum. Missing required salary evidence stays Inventoried. Respect either-IC-or-manager preferences without treating Product Manager as proof of people management. Assess career fit and resume fit independently, citing JD/goals/master versions and rationale. The master is the candidate-fact source; goals and requirements are not evidence of experience.

## Decisions

Read Manual notes under DATA.md. A short displayed salary range or an Equity/Bonus label is not sufficient compensation evidence: verify the applicable original band, currency, period, base-versus-total basis and location. Keep the display concise and full evidence recoverable. Respect a human decline without treating it as a global scanner rejection.

- Clear non-PM or below-scope candidate: Not pursuing, Role eligibility Excluded, reason category role_function or seniority_scope.
- Eligible role with a hard career contradiction: Not pursuing, explicit failed hard-career check and precise career reason category/evidence in the review snapshot.
- Eligibility and hard career constraints pass, with High career fit OR High resume fit: Queued for Prepare. Persist full current review acceptance/evidence.
- Both fit axes Low: Not pursuing, reason fit; no invented hard career exclusion.
- Missing, borderline or unresolved evidence: Inventoried with blocker/next action. Do not exclude a role merely because its live page is unavailable when a sufficient exact official JD was already captured. Missing full-JD or required salary evidence still needs review; duplicates require canonical identity.

A high resume fit cannot waive a hard career contradiction. Queued is the sole approved preparation queue; do not create new Shortlisted states. Company cooldowns are later submission blockers, not fit rejection.

## Feedback without recall loss

Keep a concise assessment/next action in Agent notes on Applications; preserve any still-relevant unresolved issue. Store structured review.reason_category and explicit review.role_eligible / review.career_requirements_pass checks in the complete History snapshot. No Career gate, Decision category, Assessment summary or Blocker field is used. Save source quotes, full reasoning, per-job JD hash, explicit acceptance and fixed policy/content versions in indexed evidence and a History stage snapshot under DATA.md. Link Review run. Migrating old columns never removes these requirements. Distinguish scanner false positives (role_function/seniority_scope), career mismatches (career_domain/career_industry/career_vertical/career_stage/career_geography/career_compensation/career_other), fit, missing_evidence, availability, duplicate and human_choice. Pending evidence, closures and human choices are not automatically scanner mistakes.

Follow stages/scan.md to aggregate outcomes and propose versioned improvements. Never turn all non-queued examples into negatives or silently move career screening into Scan. Record meaningful changes in History, verify saved values and save Run handoff. Single Review stops; a full Run advances accepted Queued roles to Prepare.

Review never requires posting availability monitoring. Apply checks its actual form later. Migrate old availability-only holds to targeted Inventoried, not automatic approval. A current recorded approval requires both explicit checks true, at least one High fit, exact current inputs and the matching Review run; lifecycle alone cannot establish acceptance.

## Final scope evidence

Use scripts/role_gate.py:review_eligibility with the current goals-derived exclusive experience threshold. More than the configured years OR an explicit evidence-backed equivalent senior scope can pass. Low stated minimum years alone do not prove insufficient scope. Title, pay and company prestige do not establish grade; mixed or ambiguous evidence stays Inventoried with a specific next action. Scan plausibility is not final eligibility.

For equivalent-scope boundaries examine autonomy, strategy ownership, multi-team/PM-team influence, product complexity and accountable outcomes. Cite actual evidence for the comparison; titles, pay and company prestige do not establish a universal grade. Threshold/benchmark are versioned private preferences, never personal facts hardcoded into Git.
