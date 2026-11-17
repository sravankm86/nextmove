# Prepare: a verified resume for every queued role

Use WORKFLOW.md, DATA.md and RESUME-FILES.md. Prepare's goal is one verified resume for each review-approved Queued role. It gets there by one of two paths: **reuse an approved base resume** that already fits the role, or **create a role-specific (tailored) resume** from the closest base. It never edits the master, never creates or reworks a base, and never submits.

## Inputs and scope

Process review-approved Queued roles with current accepted full-JD eligibility, qualifications, career and fit evidence (`scripts/stage_state.py:review_ready`). Inventoried, Need review and Duplicate are not preparation-ready; older approvals require revalidation under the current score frame. Before accepting a queued handoff, reread the linked company and pass current companies to review_ready/resume_ready. Proposed, Exclude or permanent-block targeting prevents automatic advancement without erasing the assessment. A temporary hold does not prevent preparation. Revalidate company-evidence changes under Review, not by changing fit from a hold label.

Resolve and pin these registered Settings resources in the Run:

| Key | Role |
|---|---|
| master_resume | The designated editable master: the only source of resume facts. Never modified by Prepare. |
| resume_guidelines | The user's private resume guidelines in the standard frame (contracts/resume-guidelines-schema.json, blank form templates/resume-guidelines.md). Governs every selection and every tailored version. |
| base_resumes | The library of approved bases: for each, theme/variant, page length, exact PDF and editable source references, content version (hash) and the master version it was built from. |
| resume_output / content_output | Role specific and Audit trail folders under RESUME-FILES.md. |

A missing or inaccessible master or guidelines blocks Prepare for all roles; record the exact gap and ask.

## Reading the guidelines

The guidelines use one standard frame: numbered sections with stable IDs, each holding typed fields (select, multi-select, boolean, number, range, date, list, table) and a natural-language Instructions field. The same frame can be a document today and a configurable form later; Prepare reads it the same way either way:

- Read values by `section.field` ID, never by heading wording. Validate them with `scripts/resume_guidelines.py:validate`; an invalid value is a blocker to report, not something to guess.
- Only `document.status` Approved governs Prepare. A Draft version is not used until the user approves it.
- Structured values take precedence over a section's Instructions. Instructions refine within that section; a contradiction between them is a question for the user.
- A blank field falls back to the defaults in this file. Where no default exists and the choice changes the resume, ask.
- An older free-text guidelines document is mapped into the frame first (record the mapping and get the user's approval), not interpreted ad hoc.

| Prepare step | Sections used |
|---|---|
| Step 2 same-company consistency | `company_consistency` |
| Step 3 choose the path | `selection`, `bases`, `variants`, `company_grouping`, `length` (one-page versions) |
| Step 4 tailored resume | `fact_source`, `length`, `page_one`, `layout`, `structure`, `positioning`, `language`, `confidential_content` |
| Verification | `files.pre_approval_checks`, plus a `guideline_check` entry for every applicable field | An empty base library means every role goes to the tailored path, which still needs a structural starting point from the guidelines. Public instructions contain no user's bases, companies or wording: all of that lives in the private guidelines and master.

## Step 1: role requirements

From the accepted Review evidence (not a fresh assessment), list the JD's critical requirements (minimum qualifications and central responsibilities) and its main themes. Note the user's requested page length for this application if one is recorded (for example a one-page variant for a referral); otherwise use the guidelines' default.

## Step 2: same-company consistency

Find every earlier submission to the same company (Applications, attempts and known external applications in History). Apply the guidelines' same-company rule exactly. Typically it requires reusing the exact submitted version within a stated window and, after it, comparing any new version with all earlier submissions and removing inconsistencies first. Record `company_consistency`: `not_applicable` (no earlier submission), `pass` (rule satisfied, with the compared versions) or `conflict` (blocks Ready until resolved). If the rule forces reuse of a specific earlier version, that version is the outcome and steps 3–4 only confirm it still covers the role.

## Step 3: choose the path

1. Pick candidate bases: the base the guidelines assign to this company or company group, plus any whose theme matches the JD's main themes. Resolve variant choices the guidelines define (for example whether the JD values zero-to-one work).
2. Discard any base built from an older master version than the current master. It is stale: report it for offline refresh; it may still guide selection and order for a tailored version.
3. For each remaining base, build a coverage table: every critical requirement and main theme → the base bullet or section that evidences it, or `gap`.
4. **Reuse** when one current base covers every critical requirement and the main themes with no material gap, at the right length. Record `path: base_reuse` and `coverage: complete`. No new file is needed; a role-named copy is optional and is not proof of readiness.
5. **Tailor** otherwise, starting from the closest base (fewest gaps, right theme and length). If no base is reasonably close, or several queued roles share a theme no base covers, still tailor this role but record a `new_base_recommended` note with the shared theme for the user. Creating or redoing a base is an offline, one-off user workflow outside these instructions.

## Step 4: tailored resume (only on the tailor path)

Follow every applicable field and Instructions in the registered guidelines (sections listed above). Where a field is blank, use these defaults:

- **Facts only from the master.** Name, contact, titles, employers, dates, education, team sizes and every metric stay identical to the master. Never invent, inflate, merge or reword a fact so its meaning or number changes. Never turn a JD requirement, a goal or an area the user marks as outside their expertise into a claimed skill or highlight.
- **Allowed edits.** Select, order and trim bullets; adjust the headline, summary emphasis and skills keywords toward the role's themes; expand or compress earlier roles where the guidelines allow. Each change must make a mapped critical requirement or theme easier to see.
- **Structure, length and layout** exactly as the guidelines define (section order, bullets per role, page target and maximum, single-column ATS-safe layout, fonts, date format). Never exceed the stated maximum; do not force a different length without the user's request.
- **Positioning and language** per the guidelines' theme for this role: level-appropriate ownership language, plain verbs, no internal jargon, abbreviations spelled out once.
- **Files.** Create the editable source (for example a Google Doc) and a text-based PDF in Role specific, named and versioned under RESUME-FILES.md, with the base as parent. Never overwrite an existing or submitted file; changes create a new version.

Then verify before Ready, and record each result:

1. **Grounding:** every claim (bullet, headline, summary statement, skill) maps to a master passage; numbers and dates match exactly. Any unsupported or altered claim → `grounding: fail`.
2. **Guideline check:** one pass/fail entry per applicable `section.field` (plus each section's Instructions), recorded with the guidelines version.
3. **Coverage:** the updated coverage table shows each critical requirement evidenced or an honest `gap` that remains (never filled by invention).
4. **Rendered PDF:** open and visually inspect every page for layout, overflow, page count, fonts and readability; confirm the PDF is text-based.

Any failure blocks Ready; fix and create a new version, or record the blocker and ask.

## Writes and handoff

On success set Resume link, Resume version (SHA-256 of the exact PDF bytes, or a verified provider version), Resume verified at and Preparation run on Applications, then move the role to Ready. For reuse, these point to the exact base PDF. Save the preparation snapshot under DATA.md: `path`, `base` and `base_version`, `base_master`, `guidelines` version, coverage table, `company_consistency`, and for tailored versions the change notes, `grounding`, `guideline_check`, filenames and visual verification. Keep longer evidence in Audit trail and change notes beside the role resume in Role specific. `scripts/stage_state.py:resume_ready` refuses Ready unless the path's evidence is complete.

Agent notes states the outcome in one line, for example `Prepare: reused the platform base (full coverage).` or `Prepare: tailored from the startup base; 2 bullets reordered, headline adjusted. Next: Apply preflight.` Never overwrite Manual notes or erase unresolved company restrictions; prior values stay in History. Runs records counts by path (reused, tailored, blocked), stale bases, `new_base_recommended` themes and blockers.

Before advancing, verify that the accepted review still matches the current goals, role policy, master, guidelines and job description. A changed master, guidelines or JD requires re-preparation, not silent reuse. Preserve submitted and terminal history. A single Prepare command stops at its handoff; a full Run advances only verified work to Apply preflight.
