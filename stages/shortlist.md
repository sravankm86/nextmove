# Rate discovered jobs

Input: Queued rows from Applications, exact-role application history, private candidate preferences and master CV. Pick unrated rows, optionally by scan run ID. Reevaluate previously rated roles when the posting or candidate criteria change.

Open the official job description URL for each candidate. Verify the requisition and read the full responsibilities and qualifications. If the description is blocked, incomplete, unavailable or for a different requisition, record the issue and leave relevance blank. Verify explicit eligibility requirements separately from fit. Missing evidence is unresolved.

Assess each role on:

- Role family and product domain, including the actual work behind the title.
- Seniority, scope, ownership and leadership expectations.
- Required qualifications and evidence from the candidate's CV.
- Customer, workflow and technical context.
- Candidate preferences for location, work arrangement and compensation when available.

Use consistent anchors:

| Relevance | Meaning |
|---|---|
| High | Strong evidence on the central responsibilities, target seniority and product scope, with no known disqualifying requirement. |
| Medium | Plausible fit with a material gap, adjacent scope or a preference that needs checking. |
| Low | The description shows a clear mismatch with core responsibilities, required qualifications or explicit eligibility criteria. |

Write the rating, concise evidence from the posting and CV, material gaps, eligibility and evaluation date back to the same Applications row. Set Lifecycle status to Reviewed after a full assessment, following LIFECYCLE.md; leave later states and unresolved history intact. Keep unreadable descriptions retryable. Record compensation only from the exact posting, with currency, geography and pay type. Preserve application history. Do not advance already submitted, In process, offered, accepted, rejected, withdrawn, user-declined, closed, duplicate or Submission uncertain exact roles. Resolve Needs review or ambiguous legacy Pending before advancing. Reconsider unavailable roles only after verifying reopening. Advance only verified High matches to CV preparation. Report High, Medium, Low and unrated counts.
