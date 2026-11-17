# Fictional examples

These cases are invented, not private data.

- Curate finds a Series D announcement for a company matching Career Goals: it adds the company as Proposed with Company fit High and a draft Sources row. Scan ignores it until the user sets Allow. A Series B round is counted but not added.
- A user has three applications at one company in the past 30 days: Curate sets Held with Apply blocked until the date the oldest of those three leaves the window. Scan and Review continue; Apply refuses until its own recheck returns No known hold.
- A forum post claims a six-month cooldown after rejection: Curate records it as Community confidence and sets Needs clarification rather than enforcing it.
- A Senior Product Manager posting with basic PM ownership signals becomes Inventoried with eligibility Pending. Scan does not assess its industry against career goals.
- A flat Product Manager title with unclear level remains a plausible candidate; Review resolves full scope. Staff Product Designer is a clear other function and is not inventoried.
- Missing identity stays in minimal Run checks. Missing full JD on an otherwise plausible candidate is a capture gap and blocks Review approval.
- Review verifies a senior PM role but finds a hard industry mismatch: Not pursuing, category career_industry. This is not a scanner false positive.
- Review finds a mislabeled marketing role: Not pursuing, category role_function. Repeated examples can support a tested basic-screen improvement, not a broad ban on Marketing in PM domain titles.
- An eligible role passes hard career constraints and has High resume fit: Queued. Prepare verifies a grounded base/tailored PDF before Ready.
- Prepare finds an approved platform base, built from the current master, that evidences every critical requirement of a queued role: it reuses that exact PDF (path base_reuse) and moves the role to Ready. No new file is created.
- Another queued role needs regulated-workflow emphasis no base covers: Prepare tailors from the closest base, reorders bullets and adjusts the headline per the guidelines, maps every claim to the master, renders and inspects the PDF, then sets Ready. Three such roles in one Run add a new_base_recommended note; the user builds that base offline.
- One board succeeds and another fails: source coverage is Partial even if useful candidates were saved.
- Apply preflights a Ready role on an allowed ATS, finds a required "Expected salary" free-text field with no answer-bank entry, and stops that role as needs_answer with the exact question saved. Other roles continue.
- The first submission on a new ATS family stops at the review screen with a screenshot; after the user writes Approve submit, it is submitted and later roles on that ATS run unattended within the caps.
- A possible Submit followed by a crash keeps its last verified stage with a blocking saved attempt; reconcile before retry.
- An older receipt after rejection is preserved without regressing the outcome.
- A fresh harness recovers the same Settings/Run. A full Run continues independent work and reports blocked work honestly.
