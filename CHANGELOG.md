# Changelog

## Simpler submission guard rails

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
