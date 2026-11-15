# Recall-oriented candidate inventory and review

Eligible-role recall is primary. Scan stores plausible PM candidates; Review establishes final eligibility and career fit. A smaller inventory is not itself success, and Inventoried does not mean eligible or approved.

## Scan: basic plausibility

Enumerate every official page. Broad signals include Product Manager/Management/Mgr, technical/inbound/outbound/platform variants, Group PM, Product Lead/Owner, Head/Director/VP Product, Chief Product Officer, Member of Product Staff and localized equivalents. Abbreviations and mixed functions need basic contextual checks.

Use official title, function/team, summary or available description for basic semantics. Exclude clearly unrelated functions and clearly junior roles. Do not require a seniority word or reject direct PM roles because their domain says finance, design or security. Do not turn career preferences into scan exclusions. Clear other functions without plausible PM ownership remain excluded.

A plausible candidate becomes Inventoried with scan evidence/policy version and final Role eligibility Pending. Ambiguous level or mixed function belongs in Review if plausible. Unknown identity/availability or insufficient evidence of plausibility stays a minimal Run pending check. Missing full JD alone need not prevent inventory, but blocks final review acceptance.

scripts/role_gate.py separates title_screen, inventory_candidate and review_eligibility. Titles alone establish neither a full semantic screen nor final approval.

## Review: final eligibility and career alignment

Verify exact identity, current official availability and the full responsibilities/qualifications. Require actual PM ownership plus documented experience above the configured threshold OR evidence-backed equivalent senior scope. Low minimum years alone do not prove low scope; titles/pay do not map universally to grades.

For scope boundaries examine autonomy, strategy ownership, multi-team/PM-team influence, product complexity and accountable outcomes. Cite evidence for the claimed comparison; missing evidence remains unresolved. Threshold/benchmark live privately in Settings, never personal facts hardcoded in Git.

Then assess domain, industry, vertical, company stage, geography and current career goals, distinguishing hard exclusions from soft preferences. Assess resume fit against the editable master separately. After eligibility and hard career gates pass, High on either career/resume axis supports Queued; both Low is Not a fit; unresolved cases are Needs review. Hard career contradictions are Not aligned. Scan cannot queue, and Prepare consumes only current review-approved Queued roles.

## Feedback and measurement

See SCAN-OPTIMIZATION.md. Record non-queue reasons and versions; aggregate scanner mistakes separately from career mismatches, uncertainty and availability. Validate proposed scan changes against independent labels, current reviewed positives and sampled rejects before activation. Accepted-only review cannot measure recall. Unresolved cases are not negatives.

Report transient observations/rejects, inventoried candidates, review-pending, verified eligible and queued counts separately. Old reference retention is a regression check, not true recall. Real/private job data and experiment artifacts stay outside public Git.
