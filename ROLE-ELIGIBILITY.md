# Recall-oriented inventory admission

Eligible-role recall is the primary objective. Reduce irrelevant stored rows through verification, not by narrowing title keywords or silently dropping uncertainty. Candidate screening is not admission; a small inventory is not itself a success metric.

## Transient screen

Enumerate every official page. Broad signals include Product Manager/Management/Mgr, technical/inbound/outbound/platform variants, Group PM, Product Lead/Owner, Head/Director/VP Product, Chief Product Officer, Member of Product Staff and localized equivalents. PM/CPO/GM abbreviations and mixed-function titles need description checks.

Do not require a seniority word: flat titles can describe senior scope. Do not reject a direct PM merely because its domain says finance, design or security. Conversely, Product Marketing Manager, Product Designer or Product Security Engineer are not PM just because Product appears.

scripts/role_gate.py finds verification candidates. Its output never authorizes inventory. Unexpected aliases require evidence-based investigation rather than silent new exclusions.

## Verified admission

Verify exact identity, current official availability, full responsibilities and qualifications. Require actual PM ownership plus either documented experience above the configured threshold or explicit evidence of equivalent senior scope.

A title/pay band is not a universal company-grade mapping. Low posted minimum years alone do not prove insufficient scope. Ambiguous boundaries/equivalence remain pending. Record source quotes, policy/content versions and reasoning; regex evidence snippets are not a fabricated assessment.

For an experience-boundary case, evaluate actual autonomy/product strategy ownership, multi-team or PM-team influence, product/platform complexity, and accountable business/customer outcomes. Cite the relevant responsibilities for each claimed scope dimension. This is a reasoned comparison against the user's benchmark, not a claim about the employer's internal level. Strong evidence can support equivalence; missing evidence cannot. Do not park a case indefinitely without the targeted next check or an explicit human-decision blocker.

Threshold and benchmark are user configuration in Settings/goals, not personal facts hardcoded in Git. Missing criteria blocks admission. Clear failures get aggregate reason counts, not inventory rows. Unresolved cases get a minimal pending-check entry, not claimed admission. Retry unchanged evidence only when a blocker resolves or the user requests it.

## Career screen before Queued

A verified admission becomes Inventoried. Then assess domain, industry, vertical, company stage, geography and other actual goals using the role and employer evidence. Company identity alone does not establish desired work.

Hard contradictions fail; unknowns remain unqueued. Soft preferences can be scored/disclosed rather than invented as exclusions. On pass persist evidence/version and move to Queued; on clear failure retain the admitted role as Not aligned. Detailed Review can reuse current career evidence.

## Measurement

Report transient candidates, verified admissions, pending checks and career-queued counts separately. Prior first-pass labels are a regression reference, not independent ground truth for changed criteria.

Measure admitted precision and eligible-role recall only with suitable independent labels. Include rejected near-misses, missing titles and ambiguous functions in validation. Accepted-only review cannot estimate recall. Keep unresolved sample cases explicit; do not count them as negatives or claim perfect metrics. Real job data and private experiments do not belong in public fixtures.

Audit a stratified sample of transient rejects, emphasizing unfamiliar aliases, flat titles, mixed functions and scope boundaries. A discovered eligible false negative requires widening the screen and rechecking the affected catalog slice before claiming coverage. Record unresolved checks and their next actions so improved storage precision cannot conceal lost recall.

