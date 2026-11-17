# Review: three steps

Read WORKFLOW.md and DATA.md. Run owns duplicate discovery and supplies the identity result. Review assesses Inventoried roles and retryable Need review roles; recheck stale unsubmitted approvals before they advance. Preserve Manual notes and human, submitted or terminal outcomes.

Use current linked Companies and saved Curate evidence in both a full Run and a standalone Review. Only human-Allow companies without a permanent block advance automatically; skip out-of-scope existing roles without changing their scores or lifecycle, and record the reason in the Run. Temporary holds, unresearched employer policies and incomplete discovery do not delay fit assessment or queueing. They remain submission controls, not fit criteria.

## Step 1. Extract the job description

Read the complete exact official JD, or an integrity-verified saved copy. Extract the product space, central responsibilities, minimum and preferred qualifications, compensation and work restrictions. Preserve the employer's OR/equivalent alternatives. Distinguish requirements from examples and identify missing evidence.

## Step 2. Assess career fit

Compare the role's overall product space and work with the current Career Goals: what the user wants and does not want. Apply stated compensation, location, title, seniority, work-type and company preferences. Use current factual company evidence from Curate/Company evidence when checking funding, business and company preferences. Reassess it against current goals; Company fit is advisory, not the role Career fit score. If decisive company facts are missing or stale, explain that uncertainty under this table. Pin the decisive company-evidence identity for downstream revalidation. Personal preferences belong in the private goals, not this public frame. Candidate accomplishments and missing experience do not change career fit; assess those in Step 3.

| Career fit | Meaning | Score |
|---|---|---:|
| Unresolved | Decision-critical role facts or preferences are unclear. | 0 |
| Low | An explicit disqualifying preference fails, or the role is outside the desired product space. | 1 |
| Medium | No explicit disqualifier; the role matches some desired work or preferences. | 2 |
| High | No explicit disqualifier; the role matches the desired product space and applicable preferences. | 3 |

Use the user's actual comparisons and units. Missing pay is not a salary failure. A missing candidate specialty is not a career preference failure. Explain the evidence and any unresolved preference or posting fact.

## Step 3. Assess resume fit

Compare the complete editable master and confirmed candidate facts with the whole JD. Identify the critical asks from responsibilities, minimum and preferred qualifications, and judge whether demonstrated direct or equivalent accomplishments make a credible case for an interview. Minimum/preferred labels inform this judgment but do not replace it. A preferred specialty can be critical to the actual work; an incidental tool is not automatically critical. Preserve OR/equivalent alternatives.

Record Met, Not met or Unknown with JD and candidate evidence. Distinguish a confirmed missing capability from unclear evidence. Missing keywords alone do not establish a gap. Do not invent experience, equate broad domain familiarity with a specialist track record or invent numerical shortlist probabilities.

| Resume fit | Meaning | Score |
|---|---|---:|
| Unresolved | Evidence or equivalence for a critical ask is genuinely unclear. | 0 |
| Low | A critical ask or mandatory minimum lacks demonstrated direct or credible equivalent support. | 1 |
| Medium | Critical asks and minimums are supported; remaining gaps are secondary or reasonably transferable. | 2 |
| High | Strong demonstrated match to critical asks, minimums and important preferred qualifications. | 3 |

Explain why each consequential requirement is critical or secondary. Reuse confirmed facts already supplied; do not repeatedly ask about a confirmed gap. Facts removed from Career Goals remain candidate evidence, not preferences. Store their source in private resume/candidate evidence under DATA.md; never add unsupported claims to the master.

Add both scores and use this table. Assess both axes. Unresolved is a rating with score zero, not proof of failure. Do not add a separate veto or substitute an old routing rule.

| Check, in this order | Decision |
|---|---|
| Total 2 with Unresolved | Need review |
| Total 5–6 | Queued |
| Total 3–4 | Need review |
| Total 2 without Unresolved | Not pursuing |
| Total 0–1 | Not pursuing |

Consequently High + Low is Need review, Low + Low is Not pursuing, and Unresolved + Unresolved or Unresolved + Low is Not pursuing. Explain uncertainty even when the total rejects the role. These are score outcomes, not an application authorization.

Agent notes briefly explains both ratings, the critical evidence or gap, and the resulting status. For Need review, state exactly what would resolve it. Keep full findings, source identities and input versions in History/Drive under DATA.md, verify writes and stop after Review. An eval saves predictions separately and does not change Applications unless requested.

This file is the only source for scores and routing. scripts/role_gate.py reads these tables and fingerprints this file automatically. Do not maintain a second scoring configuration or manual Review version. Unknown or malformed rules must stop affected work, not fall back to older defaults.
