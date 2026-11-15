# Role and application lifecycle

Applications holds business state; Runs holds execution progress. Keep candidate plausibility, final eligibility, career fit, resume fit, availability and outcomes separate.

| Status | Meaning |
|---|---|
| Inventoried | Passed Scan keywords/basic semantics; final eligibility and career review are pending |
| Queued | Review approved current full-JD eligibility, hard career constraints and fit; ready for Prepare |
| Not aligned | Review found a hard career-goal mismatch |
| Not a fit | Review found clear role/scope failure or both fit axes Low; reason category distinguishes them |
| Needs review | Missing/borderline evidence with a blocker and next action |
| Ready | Master-grounded resume/PDF verified; not submission authorization |
| Applied | Human reports submission or definite agent completion; receipt not implied |
| Confirmed | Exact-role employer receipt/success evidence |
| In process | Actual recruiter engagement, assessment, interview or scheduling |
| Offer / Accepted | Explicit evidenced events |
| Rejected / Withdrawn | Explicit employer rejection or candidate withdrawal |
| Not pursuing | Human chose not to apply; not a scanner negative |
| Closed | Verified availability/cancellation outcome |
| Submission uncertain | Possible submission; reconcile before retry |
| Duplicate | Verified identity duplicate preserving canonical reference/history |

Needs eligibility and Shortlisted are legacy read/migration aliases, not newly emitted statuses. Preserve their original values/history. Revalidate legacy Needs eligibility and old unreviewed Queued before using Inventoried/Queued under the new contract. A legacy Shortlisted becomes Queued only if current review evidence satisfies the new gate; no blanket rename. Never reset submitted/terminal records.

Only Scan creates new candidate inventory; only Review approves Queued. Prepare consumes Queued, not Inventoried. New candidate rows require recorded basic semantic evidence, not keyword hits alone. Unknown identity/availability remains pending in Runs. Missing full description blocks Review approval, not necessarily candidate capture.

Hard career constraints cannot be rescued by resume fit. Soft preferences/unknowns are not invented hard negatives. Every review disposition has a reason category and input/policy versions for SCAN-OPTIMIZATION.md.

Separate actual event dates from recording time. Preserve older non-regressing events in History. Absence from incomplete scans is not closure. Company cooldowns are submission blockers, not fit exclusions. Instruction updates alone do not install triggers or migrate live records; apply verified deltas with provenance during authorized work.
