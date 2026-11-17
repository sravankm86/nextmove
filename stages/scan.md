# Scan: plausible PM inventory with recall first

Follow WORKFLOW.md and DATA.md. Scan enumerates every official board of every in-scope company and stores plausible senior product-management candidates as Inventoried. It does not judge career fit or resume fit, certify eligibility or set Queued; Review owns those.

## Scope and criteria

Scan only companies where `scripts/company_policy.py:scan_enabled` is true (Search status Allow and hold not Blocked (permanent)). Proposed and Exclude companies are skipped and reported as such; temporary holds, Company fit and policy confidence are not filters. A standalone Scan uses current Companies and saved Curate output; it does not run Curate research or discovery.

Snapshot in-scope company and source IDs in the Run scope, then reread company targeting before each inventory write and pass current Companies records to `application_write`. A company that leaves scope keeps its existing rows.

Derive the role family, designation examples, seniority/experience/scope and explicit function or level exclusions from the current Career Goals revision under CAREER-GOALS.md. Save the extracted criteria, source revision and readiness in Settings and the Run; reuse a verified extraction only while its revision matches. Missing title synonyms can be derived from the function; missing or conflicting essential role intent needs a question, not an invented exclusion.

## Complete source coverage

Validate Curate's draft Sources once the user allows a company, and resolve missing boards, regions or reader configuration. An Allow company without usable Sources is a coverage gap, not zero jobs.

Enumerate every catalog page or cursor to its verified end with repeatable readers and code. Validate counts, unique identities, repeated cursors, malformed or empty pages and caps. Zero jobs needs verified empty coverage; search snippets or page-one counts never prove completeness. Reuse unchanged resources only with equivalent evidence and durable checkpoints. Preserve meaningful URL parameters; title equality is not deduplication.

Source status: Complete when every planned source is verified, Partial when usable observations have gaps, Failed when no source is usable.

## Basic candidate screen

Run checks (WORKFLOW.md) own duplicate discovery: check the identity index before inserting and hand new identity evidence back to Run.

Use broad PM signals: Product Manager/Management/Mgr and technical, inbound, outbound, platform or group variants; Product Lead/Owner; Head/Director/VP of Product; Chief Product Officer; Member of Product Staff; localized equivalents. Abbreviations and mixed functions get a basic contextual check of the title, team, summary or description. `scripts/role_gate.py` separates `title_screen`, `inventory_candidate` and Review's `review_eligibility`; a title alone never admits a role.

- Exclude clearly unrelated functions and clearly junior roles, with recorded evidence.
- Keep direct PM roles whose domain says finance, design or security, unlevelled or flat titles, and roles with uncertain level: they enter Inventoried with Role eligibility Pending for Review.
- Do not require a seniority word, infer company grade from a title, treat a low minimum-years figure as proof of insufficient scope, or turn career preferences into scan exclusions.
- Missing identity stays a Run pending check (URL, reason, next action). Insufficient evidence of plausibility stays pending, not rejected. A missing full JD does not block inventory but blocks Review approval.

## Inventory and handoff

Create or update candidates as Inventoried with stable identity, official posting URL, Scan run and the source snapshot under DATA.md. Save Job evidence: an exact capture with the full description, posting aliases, salary basis, currency, location and level conditions, work restrictions and the true posting date. Display columns follow DATA.md compact job facts; never estimate values or borrow another posting's band.

Reobserving a role updates only source metadata; it preserves human outcomes, Manual notes, review evidence and later states. A changed content fingerprint flags targeted re-review without reopening submitted or terminal roles; an unchanged declined role is not requeued. Scan never closes inventory because a posting disappeared.

Clear rejects become aggregate reason counts, not stored rows; unrelated feed bodies stay transient. Report observed, clear-rejected, plausible, newly inventoried, reobserved, identity-pending and capture-gap counts, plus source coverage and skipped companies. A single Scan stops here; a full Run hands Inventoried roles to Review.

## Improving Scan from Review outcomes

Eligible-PM recall comes first; a smaller inventory is not success. Review records a structured `review.reason_category` with evidence; use it to find Scan mistakes:

| Category | Meaning for Scan |
|---|---|
| role_function, seniority_scope | Possible basic-screen false positive; inspect the evidence |
| career_domain, career_industry, career_vertical, career_stage, career_geography, career_compensation, career_other, fit | Review-owned; never a scan exclusion |
| missing_evidence, availability, duplicate | Not a relevance signal |
| human_choice | The user's disposition, not a role exclusion |
| approved | A positive to protect in regression checks |

For recurring role or scope mistakes, propose the smallest explainable change, preferring better positive aliases and disambiguation over broad negative keywords. Before activating it, replay it against reviewed eligible positives (including eligible Not pursuing roles), known false positives, ambiguous, flat and localized titles, and a sample of source rejects, labelled independently of the rule. Every known eligible regression must be fixed or accepted by the user; without enough evidence keep the current screen and save the proposal. Moving Review-owned reasons (specialization, pay, funding, geography, qualifications) into Scan changes the stage boundary and needs the user's decision.

A validated change needs an authorized Git or Settings update with a version identifier and a History event linking the evaluation. After activation, recheck affected catalog slices, sample rejects, and widen or revert on any eligible false negative.
