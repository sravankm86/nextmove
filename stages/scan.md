# Scan: plausible PM inventory with recall first

Follow WORKFLOW.md. Read explicit Allow/Exclude choices, every configured official board/region and the versioned scan/role policy. Resolve the current Career Goals source revision and extract/verify its role-family, designation examples, desired seniority/experience/scope and explicit function/level exclusions under CAREER-GOALS.md. These determine broad scan criteria; Scan does not assess broader career fit or resume fit and cannot set Queued. Role-policy values are source-versioned extracted preferences, not an independent preference authority or user-authored procedures. At startup verify the source revision, refresh affected role-policy values and save criteria/readiness plus unresolved inputs before applying a screen. A current verified extraction may be reused; stale or untraceable Settings values may not silently override the document.

## Complete source coverage

Enumerate every official catalog page/cursor without storing unrelated rows to verified end. Validate counts, unique identities, repeated cursors, malformed/empty pages, caps and source-manifest gaps. Zero requires verified empty coverage. Search snippets or unchanged page-one counts do not establish completeness. Reuse unchanged complete resources/change feeds only with validated equivalent evidence and durable checkpoints.

Use repeatable official feeds/readers and code for parsing, identities, broad title screening, hashes and verification of saved values. Preserve meaningful URL parameters and genuine source memberships. Title equality is not deduplication.

## Basic candidate screen

Deduplicate using exact company-scoped employer role IDs or canonical job links against existing records. Do not compare every regional variant or merge different posting IDs by description similarity. Preserve migration identity gaps for one-time reconciliation.

Use broad PM keywords, aliases, localized and unlevelled titles. Check official title, team/function, summary or readily available description for plausible product-management work and senior scope. Exclude clear unrelated functions and clearly junior roles. Do not infer company grade from title, demand Senior in every title, or treat low minimum years alone as proof of insufficient scope.

Basic semantics must have recorded evidence or an explicit ambiguity reason; a keyword hit is not final eligibility. Plausible candidates with uncertain PM boundaries or level enter Inventoried with Role eligibility Pending for Review. Do not perform full career/domain/industry/vertical/geography alignment, resume scoring or exhaustive seniority adjudication here. Capture geographic/work restrictions as data, not career-fit exclusions. Explicit company Exclude remains binding.

If identity cannot be established, keep a minimal Run pending check with URL, reason and next action rather than inventing a role. Missing title can be resolved from official summary; insufficient evidence for even plausibility stays pending, not silently rejected.

## Inventory and handoff

Follow DATA.md for compact display fields: salary ranges only, explicit additional-compensation labels, short place values and the permitted work-arrangement values. Keep location-specific salary conditions and exact source text in evidence; no raw JSON or explanatory paragraphs in display columns. Preserve Manual notes and any manual disposition on reobservation.

Create or update candidates as Inventoried, recording stable identity, official posting URL and source provenance in History plus a verified Scan run and basic-semantic metadata snapshot under DATA.md. Save Job evidence and an exact indexed source capture containing full description/provenance, employer posting aliases, salary basis/currency/location/level, work restrictions and true posting date. Keep compact display values on Applications; save explicit gaps in Agent notes/Run. Never estimate metadata or borrow another posting's band. Missing full description does not discard an otherwise plausible candidate; Review must obtain it before approval.

Role eligibility starts Pending; Scan does not certify final eligibility or hard career checks. Reobserving a role updates only permitted source/metadata deltas; preserve human outcomes, existing review evidence, notes and later states. Changed evidence flags targeted re-review without reopening submitted/terminal roles. Unchanged rejected roles are not requeued every scan.

Clear rejects produce aggregate reason counts, not a raw shadow catalog. Capture candidate descriptions in registered Drive content; unrelated feed bodies remain transient. Sources holds cursor/coverage; Runs holds scope, counts, gaps and handoff; Applications holds candidate/review/application state.

Verify writes and all planned sources. Company/source Complete requires every planned source verified; Partial means usable observations with coverage gaps; Failed means no usable verified source. Report source coverage separately from capture gaps and unresolved candidates. Review pending does not by itself make completed Scan coverage incomplete. A full Run remains Partial if required later work is blocked.

Report observed, clear-rejected, plausible, newly inventoried, existing/reobserved, identity-pending and capture-gap counts separately. A single Scan stops; a full Run hands Inventoried roles to Review.

Do not maintain availability or close old inventory based on source absence. A currently returned official feed record or an existing exact official capture can establish provenance without a separately accessible landing page. Missing identity/basic-semantic evidence still blocks admission. Keep real source IDs, observation times and content fingerprints in source History metadata; no Applications.Sources or Last seen at column is used. Changed content triggers affected re-review; a fresh observation alone is not a content update. Maintain Agent notes without erasing still-relevant unresolved actions or human feedback.

## Role signals and recall

Goals supply preference values only; Git defines all interpretation and stage logic under CAREER-GOALS.md. Natural prose and incomplete preferences are supported.

Eligible-role recall is primary. Scan stores plausible PM candidates; Review establishes final eligibility and career fit. A smaller inventory is not itself success, and Inventoried does not mean eligible or approved.

## Scan: basic plausibility

Derive role family, designation examples, seniority/role-experience/scope and explicit function/level exclusions from current Career Goals. Pin source revision and extraction version. Validate scan readiness under CAREER-GOALS.md; missing title synonyms may be derived broadly from the function, not demanded from the user. Missing or conflicting essential role intent requires clarification, not arbitrary exclusions.

Enumerate every official page. Broad signals include Product Manager/Management/Mgr, technical/inbound/outbound/platform variants, Group PM, Product Lead/Owner, Head/Director/VP Product, Chief Product Officer, Member of Product Staff and localized equivalents. Abbreviations and mixed functions need basic contextual checks.

Use official title, function/team, summary or available description for basic semantics. Exclude clearly unrelated functions and clearly junior roles. Do not require a seniority word or reject direct PM roles because their domain says finance, design or security. Do not turn career preferences into scan exclusions. Clear other functions without plausible PM ownership remain excluded.

A plausible candidate becomes Inventoried with scan evidence/policy version and final Role eligibility Pending. Ambiguous level or mixed function belongs in Review if plausible. Unknown identity or insufficient evidence of plausibility stays a minimal Run pending check. Missing full JD alone need not prevent inventory, but blocks final review acceptance.

scripts/role_gate.py separates title_screen, inventory_candidate and review_eligibility. Titles alone establish neither a full semantic screen nor final approval.

## Improve Scan from Review outcomes

Use existing Applications, Runs, Settings and History; no new feedback table, general task engine or model API is required. This is an agent-run improvement loop, not an installed background trainer.

## Capture the right signal

Review keeps the concise current handoff in Agent notes on Applications and a structured review.reason_category with exact checks/evidence/version metadata in History and indexed Drive content under DATA.md. Scan run/Review run identify the fixed context; never recreate retired reason/version columns. Include scan/review policy versions, JD hash/reference, goals/master versions where relevant, and actual outcomes. Keep scan evidence separate from final eligibility evidence.

Manual notes is the inline human-feedback input. Observe changed note/status fingerprints and preserve the original wording under DATA.md; never clear the field after processing it. Classify human dispositions as human_choice unless independent JD evidence establishes a different category. Feedback does not itself activate a new exclusion rule.

| Category | Interpretation for Scan |
|---|---|
| role_function, seniority_scope | Potential basic-screen false positive; inspect transferable evidence |
| career_domain, career_industry, career_vertical, career_stage, career_geography, career_compensation, career_other | Review-owned preferences; do not automatically add scan exclusions |
| fit | Review assessment, not proof of wrong PM family/level |
| missing_evidence | Unresolved, not a negative training label |
| availability, duplicate | Historical access/form or identity problem, not semantic relevance; no closure monitoring |
| human_choice | Human disposition, not an inferred role exclusion |
| approved | Review-approved positive to protect in regression checks |

Not queued is not a single negative class. Preserve uncertainty, human outcomes and changes to criteria. Do not delete rejected candidates to hide false positives or lower counts; apply only an explicit retention policy with recoverability.

## Evaluate a proposed change

At a Review handoff, summarize counts/reasons by company/source and scan version; small samples are qualitative evidence, not statistical certainty. Store compact findings/proposed changes in the Run checkpoint and a meaningful History event. Local execution is an accelerator; durable evidence stays in Airtable/registered Drive.

For recurring clear role/scope mistakes, propose the smallest explainable keyword or semantic adjustment. Prefer positive alias coverage and evidence-based disambiguation over broad negative keywords. Career screening remains in Review unless the user explicitly changes the stage boundary.

Before activation, replay against reviewed eligible positives (including eligible Not pursuing roles), known false positives, ambiguous/flat/localized titles and a stratified independent sample of source rejects/near-misses. Compare baseline/proposed candidate counts, PM/scope recall, false positives, queue yield and unresolved cases. Label independently of the rule under test; do not treat old scan decisions as gold. Separate a held-out check from examples used to tune the rule. If rejected examples were not retained, re-enumerate official sources and disclose closed-posting gaps; do not silently create a raw shadow inventory.

Primary target is eligible-PM recall, not queue yield. Every known eligible regression must be fixed or explicitly accepted by the user; unknown cases cannot be counted as safe exclusions. Without adequate evidence keep the current screen and save the proposal. A low queue rate caused by career preferences does not justify narrowing Scan.

## Activate and monitor

A validated behavior change needs an authorized instruction/Settings update, a version identifier and a History event linking evaluation evidence. Do not self-modify hidden prompts. Version references must be durable and recoverable by another harness. Git updates require repository write capability; otherwise hand off the concrete proposal.

Apply active criteria on the next scan, recheck affected catalog slices and preserve prior row provenance. Changed evidence permits targeted re-review; unchanged rejections do not churn through the queue. Sample rejects after changes. A discovered eligible false negative requires widening/reverting the rule and rechecking the affected scope. Do not claim true precision/recall without suitable independent labels and disclosed uncertainty.
