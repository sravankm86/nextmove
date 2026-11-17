# Curate: company list, employer policies and application holds

Follow WORKFLOW.md and DATA.md. Curate is the first stage of every Run and owns the Companies table. It keeps the company list aligned with Career Goals and keeps each company's application hold current. It never sets Allow or Exclude on its own, never changes role fit, never deletes a company and never submits anything.

Curate has three parts. Run them in this order; each one checkpoints separately in the Run so a later segment or another harness can resume.

| Part | When | Writes |
|---|---|---|
| 1. Hold recompute | Every Run and every single Curate command | Application hold status, Apply blocked until, Agent notes |
| 2. Policy research | Companies whose employer policy is Not assessed, unverified or due for reverification | Policy fields, Policy confidence, Policy verified at, Restriction details / source |
| 3. Funding discovery and re-evaluation | When `company_policy.discovery.cadence_days` has elapsed since the last successful discovery checkpoint, or on explicit request | New Proposed rows, Company fit, funding fields, draft Sources |

Scan, Review and Prepare do not wait for parts 2 and 3. Part 1 must finish before Apply. A blocked or partial Curate leaves Scan to run on the current Allow list; report the gap rather than stopping unrelated work.

## Three separate questions

| Question | Field | Owner |
|---|---|---|
| Should Scan read this company's boards? | Search status: Proposed / Allow / Exclude | Human. Curate only proposes. |
| Does the company match Career Goals? | Company fit: High / Medium / Low / Unresolved | Curate |
| May we submit an application right now? | Application hold status and Apply blocked until | Curate computes; Apply recomputes before Submit |

Do not merge these. A hold or cooldown never lowers Company fit or role fit, and never changes Search status. Scan reads exactly the companies where `scripts/company_policy.py:scan_enabled` is true: Search status Allow and hold not Blocked (permanent).

## Startup

Read Settings `company_policy`, the current Career Goals revision (company preferences, stage/size, domains, location and any personal application limit) under CAREER-GOALS.md, live controls and the Companies, Applications, Sources and History tables. An explicit personal limit in Career Goals overrides the Settings default; the default is 3 applications per company in any rolling 30 days. Record the resolved limit and its source in the Run's input versions.

## 1. Hold recompute

For every company that is not Exclude, build its event list from saved evidence and call `compute_hold` in `scripts/company_policy.py`:

- `submission`: each distinct Applied row (Applied on, or the exact History submission time when known), known external/manual applications recorded in History, and later-rejected or withdrawn applications. Deduplicate Duplicate rows and repeated receipts by Job key / attempt key.
- `uncertain_attempt`: every saved unresolved Submission attempt key. It occupies capacity but is never treated as Applied.
- `rejection`: actual employer rejection times from History (Track records them). Use Occurred at, not Recorded at.

The function applies the personal limit to every company, then the employer quota and rejection cooldown only when the policy is enforceable and company-scoped. Write the returned status and Apply blocked until (UTC ISO8601), and put the reasons in Agent notes, for example `Held: personal limit 3/30d reached; reopens 2026-12-01. Employer rule: Official 3/30d.` Save before/after values in History.

Rules the function enforces, which agents must not bypass by hand:

- Date-only events without a Restriction timezone are placed at the latest instant of that date anywhere, so estimates err toward waiting longer.
- Only Rolling windows are computed. Calendar or Fixed windows, mixed or unconfirmed scope, or a rule with Community / Not found confidence → Needs clarification, with the exact question saved in the Run.
- Role family / Exact role rules do not hold the whole company; Apply checks the affected roles.
- Blocked (permanent) is preserved untouched. Only the user removes it.
- Not assessed means the employer policy has not been researched. Apply treats it as blocking.

An elapsed Apply blocked until does not authorize submission. It is an estimate until Apply recomputes it.

## 2. Employer policy research

For each company whose Policy confidence is blank, or whose Policy verified at is older than `policy_research.reverify_after_days`, look for published limits on applications per period and waiting periods after rejection. Search in this order and stop at the first authoritative answer:

1. The company's official careers site, candidate FAQ, application terms or application-form text. → **Official**
2. A recruiter's written statement for this user (from Track mail evidence or Manual notes). → **Recruiter**
3. An explicit statement by the user in chat, Manual notes or Career Goals. → **User**
4. Candidate reports such as forums or review sites. → **Community**. Record them in details but they are not enforced; the hold becomes Needs clarification until the user confirms.
5. Nothing found after checking the sources above. → **Not found**; leave the numeric fields blank. Blank means no known employer rule, never zero or unlimited.

Record in Restriction details / source: the quoted rule, its URL or message identity, retrieval date, trigger, scope, window type, reset boundaries and exceptions. Save captures over a few lines as Drive content in the Audit trail and link them from Company evidence. Set Max applications, Application window (days), Application window type, Rejection cooldown (days), Restriction scope and Restriction timezone only from what the source states. Do not infer a cooldown from a generic rejection email or a common industry practice. If a rule has several windows or scopes, record each in details and set scope Mixed. Then rerun part 1 for that company.

This part can be large on the first pass (every company starts Not assessed). Work through the whole eligible list in checkpointed segments; never stop at a fixed count and call the stage complete.

## 3. Funding discovery and re-evaluation

Discovery finds companies that recently raised money and may match Career Goals. It reads only the feeds registered in `company_policy.discovery.feeds` (official press pages, VC portfolio/news pages, funding news sites, regulatory filings, newsletters in the read-only mailbox). Each feed keeps its own checkpoint (last item identity and time) in the Run and Settings. The first run looks back `first_run_lookback_days`. No feeds registered means discovery is Blocked, not Complete; ask the user which feeds to register.

For each funding event:

1. Normalize the company identity (legal/brand name, official domain) and the Company key. If the company already exists in any Search status, update its funding fields and Agent notes only; never re-propose an Exclude.
2. Admission gate: the round must satisfy `funding_qualifies(stage, min_funding_stage)`; the default minimum is Series C, and later private rounds, Late private and Public companies qualify. Unknown stage does not qualify; keep it in the Run as unresolved rather than adding a row.
3. Score Company fit against Career Goals company preferences only (domain/product area, stage and size, location/work arrangement, stated avoids). High/Medium/Low need concrete evidence; missing decisive facts → Unresolved. A Low fit is recorded in the Run aggregate counts, not added as a row.
4. Create the row with Search status **Proposed**, Origin Discovered, Company fit, Funding stage, Latest funding (round · amount · lead, compact), Funding date, Company evidence and Application hold status Not assessed. Agent notes states why it fits and what the user must decide.
5. Find the official careers board and supported reader (for example Greenhouse, Lever, Ashby, Workday) and draft a Sources row linked to the company with Latest coverage Unverified. Scan ignores it until the user changes Search status to Allow.
6. Research its employer policy (part 2) so it is ready if approved.

Re-evaluation: for existing Allow companies, when a discovered event shows acquisition, shutdown, major layoffs, a change of business, or new facts that change Company fit, update Company fit and Agent notes and add a Run question proposing the change. Never change an Allow or Exclude yourself.

## Human decisions

The user approves a Proposed company by setting Search status to Allow, or declines it by setting Exclude (with an optional reason in Manual notes). Declined companies keep their row so discovery does not propose them again. Curate reports pending Proposed rows in every handoff, grouped by Company fit.

A permanent block (for example a lifetime application limit already reached, or a user decision not to apply again) requires explicit user confirmation, saved in History. Curate may propose it as a Run question; once confirmed, set Application hold status Blocked (permanent). The company keeps its Search status and Sources, but Scan stops reading it. Unblocking is a user action.

## Writes, notes and handoff

Manual notes is human-owned: read it and never overwrite it. Agent notes holds the current decision, evidence summary and next action; prior values go to History. Link touched companies to the Run with Curate run. Save meaningful field changes, policy evidence, proposals and user decisions in History.

Handoff reports separately: holds recomputed (counts per status and any changes), policies researched by confidence level, discovery feeds read with coverage, new Proposed companies by fit, re-evaluation proposals, Needs clarification questions and the next action. Curate is Complete only when every non-Exclude company's hold is recomputed, every due policy is researched or explicitly blocked, and every due feed is read to its verified end.
