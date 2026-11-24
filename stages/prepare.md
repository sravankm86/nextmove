# Prepare: a verified resume and required answers for every queued role

Use WORKFLOW.md, DATA.md and RESUME-FILES.md. Prepare's goal is a verified resume and ready answers to every required application question for each review-approved Queued role. It gets there by one of two paths: **reuse an approved base resume** that already fits the role, or **create a role-specific (tailored) resume** from the closest base. It never edits the master, never creates or reworks a base, and never fills or submits an application.

## Inputs and scope

Process review-approved Queued roles with current accepted full-JD eligibility, qualifications, career and fit evidence (`scripts/stage_state.py:review_ready`). Inventoried, Need review and Duplicate are not preparation-ready; older approvals require revalidation under the current score frame. Before accepting a queued handoff, reread the linked company and pass current companies to review_ready/resume_ready. Proposed, Exclude or permanent-block targeting prevents automatic advancement without erasing the assessment. Revalidate company-evidence changes under Review. Legacy historical outcomes and attempts are read-only under WORKFLOW.md; exclude them from preparation even after a manual label reset.

Resolve and pin these registered Settings resources in the Run:

| Key | Role |
|---|---|
| master_resume | The designated editable master: the only source of resume facts. Never modified by Prepare. |
| resume_guidelines | The user's private resume guidelines in the standard frame (contracts/resume-guidelines-schema.json, blank form templates/resume-guidelines.md). Governs every selection and every tailored version. |
| base_resumes | The library of approved bases: for each, theme/variant, page length, exact PDF and editable source references, content version (hash) and the master version it was built from. |
| resume_output / content_output | Role specific and Audit trail folders under RESUME-FILES.md. |
| answer_bank | Live Answer bank and Application questions table mappings. Approved reusable form answers and Resolved role-specific final answers; DATA.md defines the fields. |

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

Use earlier resumes and externally used versions the user has already recorded in Applications/History or the registered guidelines. Do not require mailbox access, retired submission columns or an application-stage task. If the guidelines require missing history, ask for the exact submitted PDF/date for that company rather than assuming there is none. Save the request in the Run, preserve the current resume and continue independent companies; unknown history is not not_applicable. A guideline/source refresh cannot certify old company-consistency evidence. Apply the guidelines' same-company rule exactly. Typically it requires reusing the exact submitted version within a stated window and, after it, comparing any new version with all earlier submissions and removing inconsistencies first. Save `company_history` with status complete, the number of matching earlier submissions, the evidence reference and compared_versions when matches exist. Any missing date/PDF stays in missing_details and blocks this role; a label alone cannot pass company_history_ready. Record `company_consistency`: `not_applicable` (no earlier submission), `pass` (rule satisfied, with the compared versions) or `conflict` (blocks Ready until resolved). If the rule forces reuse of a specific earlier version, that version is the outcome and steps 3–4 only confirm it still covers the role.

## Step 3: choose the path

1. Pick candidate bases: the base the guidelines assign to this company or company group, plus any whose theme matches the JD's main themes. Resolve variant choices the guidelines define (for example whether the JD values zero-to-one work).
2. Discard any base built from an older master version than the current master. It is stale: report it for offline refresh; it may still guide selection and order for a tailored version.
3. For each remaining base, build a coverage table: every critical requirement and main theme → the base bullet or section that evidences it, or `gap`.
4. **Reuse** when one current base covers every critical requirement and the main themes with no material gap, at the right length. A gap the master itself cannot fill (a real experience gap) does not count against a base: tailoring cannot close it, so record it as an honest gap and reuse. Tailor only when the master holds evidence a role needs that the base leaves out. Record `path: base_reuse` and `coverage: complete`. No new file is needed; a role-named copy is optional and is not proof of readiness.
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

## Step 5: inspect application questions and prepare answers

After verifying the resume, save its link/version/verification and preparation evidence while the role remains Queued. `resume_verified` checks this intermediate resume result; it does not certify Ready. Reuse an unchanged verified PDF on retries rather than regenerating it just because answers are pending.

1. Open the exact Job description link and follow its official Apply link for this posting. Inspect the entire accessible application: all pages, required fields, choice options and conditional questions relevant to the user's approved answers. Do not fill the external form, upload files, check consent boxes or submit. Read any policy before treating an approved policy answer as applicable. A login, inaccessible step, upload prerequisite, unknown conditional branch or technical error is incomplete inspection, not zero questions. Save the exact blocker and continue independent roles. The verified resume satisfies the resume-file requirement in the handoff; any other required attachment remains a blocker until available.
2. Capture exact prompts, stable employer field keys, options, required/optional flags, question type, posting/form identity, inspection time and evidence in a per-application manifest in History/Drive. Cover ordinary required fields such as contact details too. Distinguish **Form** questions (a factual answer or choice supplied by the user) from **Narrative** questions (an essay or descriptive response). A complete inspection with no required questions needs explicit evidence and an empty list.
3. Search both live tables before creating anything. Match meaning, scope, options and intent, not wording alone; an approved general rule can cover a company paraphrase only when its guidance allows it. Honor any restriction written in Guidance and resolve conflicts. A bank answer is usable only with a nonempty Answer and **Approved** ticked. A role-question answer is usable only with nonempty Final answer and Status **Resolved**, linked to this application. A draft, cached status, source pointer without an answer or another role's resolved answer is not acceptance. Read the current source when an approved answer references it; a changed fact requires an updated Draft and human approval, not silent reuse.
4. For a missing Form answer, create/reuse one **Answer bank** row with **Approved** unticked; give it a short readable Question label, put the exact employer prompt and options in Guidance, and write any company or role restriction there unless the answer is safely general. Leave Answer blank or save an explicitly unapproved candidate; do not infer private facts from the resume or invent user choices. For a missing Narrative answer, create/reuse one **Application questions** row linked to this application with Question type **Narrative**, Status **Needs answer**, exact Question/Options and a grounded Draft answer when possible. Reuse relevant prior answers and current master/context as drafting sources; keep source references. Never overwrite a human Final answer. Human confirmation is required before a new/changed answer is ticked Approved or set Resolved; the agent does not approve its own draft.
5. Prevent duplicates before every create. Reuse an existing same-scope question/intent and answer record, including an unanswered one. Preserve materially different options, claims and company-specific questions; do not merge distinct meanings or silently broaden an approved rule's scope. Narrative reuse across roles creates a new current-application draft with the source linked, not an automatically Resolved copy. Existing resolved Form rows in Application questions may still satisfy their linked role; no mass migration is required. Store question identity decisions and before/after values in History.
6. For every required question, record the matched table/record ID, exact answer fingerprint, the answer mapped to the offered options and evidence that the match/mapping is valid. Build and validate the manifest with `scripts/application_answers.py`. Reread both tables before Ready and verify each referenced answer still exists with its required status and unchanged content/scope. Reinspect affected forms when questions, options, the selected resume, relevant facts or approval inputs change. A new invocation must verify current form coverage; old question snapshots do not prove the current form is unchanged.

If anything is missing, retain the verified resume and keep the role **Queued**. Agent notes states the missing answer or inspection blocker; the Run lists exact rows/questions and next action. Optional unanswered questions do not block Ready. Do not reopen protected submitted/terminal history. Existing unsubmitted Ready roles need this new question check before their Ready handoff is reused; keep their resumes and prior evidence.

## Writes and handoff

Save Resume link, Resume version (SHA-256 of the exact PDF bytes, or a verified provider version), Resume verified at and Preparation run once the resume is verified. Move the role to Ready only when that verified resume exists and every required answer passes the Approved/Resolved checks above. For reuse, these point to the exact base PDF. Save the preparation snapshot under DATA.md: `path`, `base` and `base_version`, `base_master`, `guidelines` version, coverage table, `company_consistency`, and for tailored versions the change notes, `grounding`, `guideline_check`, filenames and visual verification. Keep longer evidence in Audit trail and change notes beside the role resume in Role specific. `scripts/stage_state.py:resume_ready` requires both complete resume-path evidence and `preparation.application_questions` with complete form coverage and current live answers. Pass normalized live `answer_bank` and `application_questions` rows, and the freshly inspected per-role `current_inputs.form_hash` plus `current_inputs.answer_check_date` in the user's timezone. A nonempty Resume link alone never passes.

Agent notes explains the result in plain English under DATA.md "Writing Agent notes" and says which resume was used and why, and the main gaps a recruiter would notice. When Settings `preparation_notes.shortlist_estimate` is true, it also gives an estimated shortlist chance on a 1–10 scale: the agent's judgment of how competitive the resume is for this posting, not a measured probability, written as "shortlist chance about 7/10". Example: `Ready: your analytics base was reused because it leads with the experimentation work this role centers on. Shortlist chance about 7/10. Gaps: no direct healthcare-industry experience.` Consume Feedback only through the verified feedback-inbox procedure in DATA.md; prior values and historical restrictions stay in History. Runs records counts by path (reused, tailored, blocked), stale bases, `new_base_recommended` themes and blockers.

Before advancing, verify that the accepted review still matches the current goals, role policy, master, guidelines and job description. A changed master, guidelines or JD requires re-preparation, not silent reuse. Preserve submitted and terminal history. Both a single Prepare command and a full Run stop here. Hand the user the exact verified PDF link/version, the reuse or change summary, approved/resolved required answers, honest gaps and any blockers. The user fills and submits the application.
