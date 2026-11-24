# Changelog

## Five-field Answer bank

- Answer bank keeps Question (readable primary label), Answer, Guidance, Source field and an Approved checkbox. Answer ID, Topic, Handling, Approval, Valid until and the Company/Application scope links are retired; any restriction is written in Guidance.
- Application questions drops the Answer rule link; Applications drops Application answers. Blueprint: 119 fields, schema 19.
- `answer_fingerprint` now covers the five bank fields, so saved preparation manifests recompute on the next Prepare check.

## Required answers in Prepare

- Expand Prepare to inspect application questions after resume verification; no external form filling or submission.
- Reactivate Answer bank and Application questions, preserving existing answers and approval states.
- Ready now requires a verified resume, complete form coverage and current Approved/Resolved required answers. Keep Queued and preserve the PDF when answers or inspection are blocked.
- Add live-answer fingerprints, duplicate-question reuse and fail-closed readiness checks.

## First-run readiness

- Separate permanent Manual notes from the verified Feedback inbox, preserving existing notes and receipt identities.
- Preserve incompatible legacy audit maps without crashing recovery or treating them as approval.
- Discover companies new to the list without a recent-funding gate; current user preferences determine company types and applicable maturity rules.
- Checkpoint new-company Allow choices and affected prior approvals; keep missing submission history local to affected resume work.


## Resume-ready endpoint

- End Run after Curate → Scan → Review → Prepare, with the verified resume as Ready.
- Remove Apply/Track, form answers, application-question/submission helpers, mailbox work and application-limit/cooldown management.
- Use seven active tables and six lifecycle states; preserve existing later-stage data and protect historical outcomes.
- Retain Review scoring, objective duplicate checks, feedback/blind replay, source recovery and grounded PDF verification.

Earlier entries below describe historical releases, not the current supported workflow.

## Form answers hold only the submitted value

- `validate_question` rejects a resolved Form final answer that is not one of the recorded options (single or multi-select); free-text fields with no recorded options are unaffected. Explanations belong in Answer bank Guidance.
- README: Needs answer points to the Answer bank and Application questions tables.

## Source registration and selective readers

- Keep documents and evidence in Drive; repair source identity, authority and version tracking in existing Settings. No new tables or job fields.
- Add pure exact-ID artifact readers and source/cache freshness guards. Preserve historical spreadsheet references without a global fallback.
- Distinguish source readability, factual confirmation and mailbox/Track coverage.

## Separate Form answers from Narrative drafting

- Answer bank contains user-approved Form facts, preferences and consent only. Narrative prompts, examples, drafts and approved finals live in Application questions.
- Added Question type, Draft answer, Sources and optional Company scope for reusable Narrative examples; no new table or lifecycle state.
- Agents draft from verified prior answers, the master and user-confirmed context, respect candidate AI policies, and preserve human approval of final responses. Schema, onboarding, guards and regression tests updated together.

## Structured private answer bank

- Answer bank and Application questions replace the active answer Doc; nine tables with existing History, Runs and Settings reused. Source-based compensation stays in Career Goals.
- Shared answer guards validate approval, scope, conflicts, source units, expiration, options and question retry identity. Narrative adaptations remain harness judgments with saved evidence.
- Setup/migration, application preflight, audit, schema counts and private onboarding updated together. Submission defaults remain paused with daily limit zero.

## Every session starts with a connection check

- SETUP.md "Start a session": the agent finds the private base, tests Airtable, Google Drive/Docs, web, browser and mailbox access, asks the user for any missing connection, checks for another active writer, reports each stage as Ready or Blocked and records a `Harness check` History event before running the requested stage.
- AGENTS.md, CLAUDE.md, CODEX.md, README.md and the saved harness prompt point to it, so a newly onboarded agent runs it without a custom prompt beyond the base link.

## Public instructions carry no personal preferences

- Scan, the title screen and Review eligibility read the target role family from private Settings `role_family` (format: templates/role-family.example.json). The repository no longer assumes any role.
- No built-in personal application limit or discovery funding minimum: both come from the user's Career Goals via Settings. `funding_qualifies` requires an explicit minimum.
- The Prepare shortlist estimate is opt-in through Settings `preparation_notes.shortlist_estimate` (off by default).
- Neutral examples in Review, Prepare, DATA.md and the Career Goals template; starter eval reason types that a private registry can replace.
- `check_repo.py` now fails when public instructions name a specific role family or funding minimum, or when any file contains a private Airtable base ID, Google Drive link or personal email address.

## Apply blocks only verified company restrictions

- `company_policy.apply_allowed` now stops a submission only for Held (an enforceable employer rule or the personal limit is reached) or Blocked (permanent). Needs clarification and Not assessed no longer block.
- When the careers site shows a restriction during an application, Apply stops that role and records the rule on the company row (Policy confidence Official) with History.

## Verified feedback inbox and blind Review replay

- Manual notes now feeds evals: capture exact feedback, deduplicate by stable identity, verify eval/snapshot/History, then clear only unchanged text. Ambiguous and obsolete feedback remains in inactive/pending cases.
- Added Capture feedback and Review eval command routes, the private eval registry, label-free input preparation, frozen-input prediction validation, recall/coverage/theme scoring and regression comparisons. Fresh blind review is separate from production writes; no automatic preference or rule promotion.
- Supporting data stays private in versioned Audit trail files. Existing human labels/splits and the 13-field eval table remain intact; partial feedback is captured without a guessed verdict.

## Prepare: resume choice, shortlist estimate and gaps in Agent notes

- A Ready role's Agent notes now say which resume was used and why, an estimated shortlist chance on a 1–10 scale (the agent's judgment, not a measured probability) and the main gaps.
- Base reuse no longer counts gaps the master cannot fill: tailoring is reserved for roles where the master holds evidence the chosen base leaves out.

## Review eval table (schema 12)

- Seventh table, Review eval: a frozen golden answer key built from the user's graded Manual notes (verdict, reason, reason type, Train/Holdout split), plus each eval's prediction and an Agree / False queue / Missed / Deferred match. Notes that no longer fit current criteria are archived and left out. DATA.md "Review eval" holds the rules.
- `scripts/review_eval.py:score` reports status match, false queues, missed roles and deferrals; an eval never changes Applications. stages/review.md is unchanged, so the Review fingerprint is unchanged.
## Lean Companies table

- Retired Origin, Company fit, Latest funding and Funding date; Companies now has 21 fields. Setup, schema generation, stage instructions and repository checks use the reduced profile.
- Funding stage remains structured. Financing details, creation origin and advisory company assessments stay in versioned Company evidence and History; Review uses current goals and verified facts. No Scan scope, Review scoring, employer-policy or application-hold rules changed.

## Review: pay, expired roles and resume-fit judgment

- Review opens the live posting first; an empty, missing or closed posting is set to Not pursuing with a plain "Role expired" note. A technical block falls back to the saved JD.
- Pay is taken from anywhere in the posting (including pay-transparency footers); the highest band in the user's currency is used even when the applicable band is uncertain, and an ambiguous base-or-total figure at or below the bar fails either way.
- Resume fit: unprovable traits count as met; missing specialist domains, customer segments or personas, engineering backgrounds, languages or citizenship requirements in the minimum or preferred qualifications mean Low; concept-level matches score Medium; user-confirmed gaps are not re-asked. Scores and routing are unchanged.
- Roles at a company the user has set to Exclude become Not pursuing with a plain note (fit scores unchanged); Proposed-company roles are still skipped until the user decides.
- Missing pay follows the user's Career Goals rule when one exists (for example the company's other pay bands or the title's seniority) instead of always staying unresolved.

## Readable Agent notes

- DATA.md "Writing Agent notes" is the single standard: one to three plain-English sentences explaining why the agent set the current status, what is unclear and what happens next, with examples for every status. Stage files point to it and use plain-English examples.
- `scripts/stage_state.py:agent_note_problems` flags notes that are empty, too long or code-like; `tests/test_agent_notes.py` checks the documented examples against it.

## Simpler submission guard rails

- New lifecycle status **Needs answer** (between Ready and Applied): Apply sets it when a required question has no answer in the answer bank, and returns the role to Ready once every waiting question is answered.
- The answer bank is a private Google Doc linked from Settings.answer_bank. When a required question has no answer, Apply skips that role, adds the question to the Doc's Specific questions table, notes it on the role and in the run summary, and uses the answer on the next run.
- Apply's guard rails are now just the `Pause applications` switch and one daily limit (`Settings.submission_policy.max_per_day`). Expiry, per-run/weekly caps, allowed-site lists, supervised first submissions, pacing and the configurable circuit breaker are gone. Fixed rules stay: no passwords or account creation, stop on unanswered required questions, never retry or continue after an unclear submission, company limits and holds.

## Reject Low on either Review axis

- A supported Low career or resume fit now means Not pursuing before numeric routing. Other thresholds and Unresolved scores are unchanged. Explicit reassessment can include Queued and Not pursuing applications; Manual notes remains human-owned.

## Cleanup

- Removed finished-migration code and docs: tracker_migration.py, table_retirement.py, legacy run-progress readers, lifecycle label mapping, field-aliases.json, config.example.yaml, table CSV templates, the unreferenced examples file and the old Review gates (general PM, qualification majority, base-maximum, queue_allowed) superseded by the three-step score.
- `apply_ready` now means Ready, no open attempt and a verified resume; `scored_review` takes only the two ratings. `approved_base_resume` folds into `base_resumes`; submission defaults live only in the policy.
- DATA.md, scan.md, SETUP.md, WORKFLOW.md and docs/MAINTENANCE.md rewritten without legacy sections. MAINTENANCE lists the remaining live columns to retire in the UI.

## Apply: browser agent under a standing authorization

- Apply is written for browser-use or computer-use agents: preflight every Ready role (identity check, field map, resume hash), then submit only within the user's standing authorization in Settings.submission_policy, evaluated by `scripts/submission_policy.py:submission_gate`.
- Guardrails: policy off by default with zero caps; expiry; per-run/day/week caps counting uncertain attempts; allowed ATS list; the first submission per ATS waits for a human go-ahead, later ones run unattended; pacing; circuit breaker on failures or any uncertain submission; no credentials, account creation or CAPTCHA; answers only from the answer bank (template added); hard stops for anything unexpected.
- Company holds, apply_ready and live controls still apply on top.

## Prepare: reuse a base or tailor under the resume guidelines

- Resume guidelines use one standard frame (`contracts/resume-guidelines-schema.json`): 15 sections with stable IDs, typed fields (select, multi-select, boolean, number, range, date, list, table) and a natural-language Instructions field per section, ready to become a configurable form. `scripts/resume_guidelines.py` validates values and renders the blank template (`templates/resume-guidelines.md`) or a filled document. Prepare reads values by `section.field` ID; only an Approved version governs.
- Prepare now produces one verified resume per Queued role by one of two paths: reuse an approved base that covers every critical requirement and main theme (built from the current master), or tailor a role version from the closest base following the user's private resume guidelines.
- New Settings resources `resume_guidelines` and `base_resumes` (the legacy `approved_base_resume` reads as a one-entry library). Prepare applies the guidelines' same-company consistency rule before choosing a path.
- `scripts/stage_state.py:resume_ready` now requires the recorded path and its evidence: complete coverage and matching base hash for reuse; claim grounding, guideline check and pinned guidelines version for tailored versions.
- Creating or reworking bases stays an offline user workflow; Prepare only reports stale bases and recommends new themes.

## Curate handoff compatibility

- Align example configuration, company evidence, live targeting and company snapshot recovery across Curate, Scan and Review. Temporary holds remain independent of fit; human targeting is rechecked before new inventory/advancement. Preserve existing application state when a company leaves scope.
- Current candidate/readiness writers require live named company records; old cached Allow IDs cannot bypass permanent blocks. Register decisive company evidence for targeted approval revalidation, without making hold timestamps fit inputs.

## Curate: company management upstream of Scan (schema 11)

- New first stage, [Curate](stages/curate.md): recomputes every company's application hold, researches employer application limits and rejection cooldowns, and on its cadence proposes newly funded Series C+ companies that fit Career Goals. Run order is now Curate → Scan → Review → Prepare → Apply → Track.
- Companies grows to 25 columns: Search status gains Proposed; hold gains Blocked (permanent); new Agent notes, Origin, Company fit, Funding stage, Latest funding, Funding date, Company evidence, Policy confidence, Policy verified at and a Curate run link. Notes is renamed Manual notes (human-owned). Runs gains Run type Curate and the Curate companies inverse link (21 columns).
- `scripts/company_policy.py` is the single implementation of hold math, used by Curate and by Apply's pre-submit check. A default personal limit of 3 applications per company in any rolling 30 days applies on top of employer rules. Only Official, Recruiter or User policies are enforced; Community reports need confirmation. Not assessed now blocks Submit.
- Discovered companies are never auto-allowed; the user moves Proposed to Allow or Exclude. A permanent block needs user confirmation and stops Scan for that company. Holds never change fit.

## Keep the existing pending label

- Retain Need review as the canonical pending state and existing Airtable option. Remove the proposed choice rename. Scores and routing thresholds are unchanged; historical Needs attention outputs refer to the same pending state.

## Career preferences and resume suitability

- Career fit evaluates desired product space and explicit preferences; resume fit evaluates critical asks across the whole JD against demonstrated candidate evidence. Keep experience and capability facts outside Career Goals.
- Both ratings use Unresolved 0, Low 1, Medium 2, High 3. The Review table is the sole routing source, including the total-two exception. Replace the pending label with Needs attention and preserve the existing Need review storage alias until an in-place rename.
- Revalidate old approvals when these inputs change; evaluation predictions do not modify Applications.

- Split salary display into numeric Starting salary and Max salary (schema 10; 29 Application fields). Preserve all bands and units in evidence; decision-policy versions remain unchanged.

## Ordered fit scores

- Career and resume fit both use Low 1, Medium 2, High 3. Total thresholds remain 6 for Queued, 4–5 for Need review and below 4 for Not pursuing.
- Correct the numeric contract, Review table, regression coverage and registered field descriptions without inventing new job assessments.


## Three-step Review and nine lifecycle states

- Review is a portable JD → career fit → resume fit frame. Personal preferences stay in the private Career Goals document.
- Need review separates assessed uncertainty from new inventory; Duplicate records objective Run-owned identity resolution.
- New score routing replaces old OR-fit, preferred-majority and provisional-salary acceptance. Old input pins and outcomes remain recoverable.

Older entries describe historical releases, not current routing instructions.


## AI-first roles across business domains

- An explicit AI-first domain preference overrides broad business-domain exclusions. Evaluate requested domain knowledge from actual minimum/preferred qualifications instead of inferring it from the product or customer.
- Preserve independent critical qualifications, product-layer and hard career restrictions; do not turn preferred domain experience into a mandatory veto. No Scan or schema change.


## Clear Drive destinations and critical qualification guard

- Setup creates or reuses Role specific and Audit trail inside the private main folder, with verified Settings mappings and ID-preserving cleanup.
- General senior PM review still requires overall JD alignment and all critical minimums. Generic tenure flexibility cannot imply prior engineering, coding, specialist or leadership experience. Readiness guards require explicit checks.
- Scan improvements remain recall-first: exact reobservation and contextual function disambiguation, without automatically converting career rejections into scan exclusions.


## Confirmed specialties and skill boundaries

- Review distinguishes security specialties, AI application platforms from infrastructure, and AI-assisted prototypes/data queries from application coding.
- Apply explicit domain exclusions and unclear-outbound preferences without repeatedly asking resolved questions. Keep narrower unproven requirements honest.
- Strict funding-stage requirements have no inferred exceptions; missing official evidence remains a verification gap. Scan's recall-first role screen is unchanged.

## General senior PM preference

- An explicit user preference can accept general senior PM roles on seniority and compensation, including disclosed generic tenure stretch. A missing team or AI assignment is no longer an invented blocker.
- Role-level preferred AI signals can establish High career fit. Specialist and incomplete postings cannot silently use this exception.
- Preserve independent restrictions, salary checks, factual resumes and submission controls. No new columns or lifecycle states.

## Qualifications and resume-fit review

- Review checks all minimum qualifications and a majority of preferred qualifications against actual evidence, applies private resume-fit exclusions and rejects verified failing base-pay ceilings first.
- Salary-only provisional queueing supports preparation; submission requires the pay check resolved.
- Senior scope can use applicable pay plus meaningful PM ownership. Duplicate prevention uses exact role IDs or job links, with no regional similarity matching.
- Agent notes explains concrete decision reasons and specific clarification needs; no database columns or lifecycle states added.

## Consolidated instructions and interview endpoint

- Eleven operational instruction files with a README map and one owner for each rule; redundant documents and deprecated markers removed.
- Seven recruiting statuses ending at Interviewing. Confirmation is evidence under Applied; uncertainty stays blocked through saved attempt identity.
- Minimal six-table blueprint: 95 physical columns including reciprocal links. Existing deployments require verified field preservation and consolidation before deletion.
- Legacy Run progress remains readable without changing frozen accepted input pins. No change to role recall, hard career requirements, resume integrity or submission authorization.

## Current instruction release

- Six active tables, one Applications table for Inventoried candidates and the reviewed Queued list.
- Single-agent full runs by default; the same saved state and checks support manually switched stages.
- Career Goals contains preferences only. Scan derives broad role criteria; Review owns full eligibility, career/resume assessment and Queued approval.
- Review reasons support tested scanner improvements that protect recall. Career mismatches are not automatic scanner errors.
- Exact compensation interpretation, IC/manager preferences, evidence versions, truthful resume preparation and explicit submission controls.
- Clear resume filenames, retained versions and PDF verification; no blanket one-page requirement.
- Shared clarification rules, complete setup/user responsibilities, field aliases, release checks and meaningful change history.
- Schema version 4 adds scan/review feedback and resume file/version fields; CSV templates match the generated schema.

## Earlier designs

Previous revisions used a full raw job catalog and separate task, attempt, artifact and configuration tables. Those are legacy migration sources, not the current workflow. Earlier status meanings, scanner career filters, manual-only execution and routine per-read journal requirements have been superseded.

Existing installations require a verified migration. Publishing these instructions does not certify account readiness, delete legacy data, install a scheduler or authorize submissions. MIT licensing and private-data boundaries remain in force.
