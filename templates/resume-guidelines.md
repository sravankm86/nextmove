# Resume guidelines

Standard frame `nextmove.resume-guidelines` v1. Fill the Value column; keep section and field IDs unchanged. Options lists the allowed choices for select fields. Instructions holds natural-language guidance for the section; structured values take precedence. Facts always come from the registered master; this document decides selection, order, wording and layout.

## 1. Document `document`

Identifies this guidelines version and what it governs.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Version | `version` | text |  |  |
| Effective date | `effective_date` | date |  |  |
| Status | `status` | select | Draft / Approved / Superseded |  |
| Applies to | `applies_to` | multi select | Base resumes / Role-specific resumes |  |
| Change summary | `change_summary` | text |  |  |

**Instructions:** _(natural language, optional)_

## 2. Fact source and allowed edits `fact_source`

Where facts come from and what a resume may change.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Fact source | `fact_source` | select | Registered editable master only |  |
| Allowed edits | `allowed_edits` | multi select | Select bullets / Reorder bullets / Trim bullets / Adjust headline / Adjust summary emphasis / Adjust skills keywords / Expand or compress earlier roles |  |
| Prohibited edits | `prohibited_edits` | multi select | Change any fact, number or date / Rephrase a fact so its meaning changes / Add claims not in the master / Present a job requirement as experience |  |
| Bases require a confirmed final master | `bases_require_final_master` | boolean |  |  |

**Instructions:** _(natural language, optional)_

## 3. Selection strategy `selection`

How Prepare chooses between reusing a base and tailoring.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Strategy | `strategy` | select | Reuse a covering base, otherwise tailor from the closest base / Always tailor from the closest base / Reuse only; block when no base covers the role |  |
| Reuse threshold | `reuse_threshold` | select | Covers every critical requirement and main theme / Covers every critical requirement |  |
| Tailor from | `tailor_from` | select | Closest base / Master directly |  |
| New base trigger | `new_base_trigger` | select | Several roles share a theme no base covers / Never recommend |  |
| Roles needed to recommend a new base | `new_base_min_roles` | number |  |  |

**Instructions:** _(natural language, optional)_

## 4. Base catalogue `bases`

The precanned bases the user maintains offline.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Bases | `catalogue` | table | see below | |

**Bases** `catalogue`: One row per base.

| base_id | name | theme | default_pages | one_page_version | status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

**Instructions:** _(natural language, optional)_

## 5. Variant rules `variants`

Choices between variants of the same base.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Variants | `rules` | table | see below | |

**Variants** `rules`: One row per variant.

| base_id | variant | choose_when |
|---|---|---|
|  |  |  |

**Instructions:** _(natural language, optional)_

## 6. Company grouping `company_grouping`

Which base each company starts from.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Groups | `groups` | table | see below | |
| Unlisted companies | `unlisted_companies` | select | Assign per role and record with the application / Ask the user / Use the default base |  |
| Default base | `default_base` | text |  |  |

**Groups** `groups`: One row per base.

| base_id | companies |
|---|---|
|  |  |

**Instructions:** _(natural language, optional)_

## 7. Same-company consistency `company_consistency`

Keeps resumes sent to one company consistent.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Window (days) | `window_days` | number |  |  |
| Within the window | `within_window` | select | Reuse the exact submitted version / Allow another version if consistent with earlier submissions |  |
| After the window | `after_window` | select | Allow another version after comparing with every earlier submission and removing inconsistencies / Always reuse the first submitted version |  |
| Submitted files editable | `submitted_files_editable` | boolean |  |  |

**Instructions:** _(natural language, optional)_

## 8. Confidential content `confidential_content`

How sensitive content is handled.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Policy | `policy` | select | User curates the master; no automatic exclusion / Exclude content tagged confidential in the master |  |

**Instructions:** _(natural language, optional)_

## 9. Length `length`

Page targets and one-page versions.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Default pages | `default_pages` | number |  |  |
| Maximum pages | `max_pages` | number |  |  |
| Target fill | `target_fill` | text |  |  |
| One-page versions kept for | `one_page_versions_for` | list |  |  |
| One-page use cases | `one_page_use_cases` | multi select | Founder-led teams / Referrals / Recruiter request / Online form limit |  |
| One-page rules | `one_page_rules` | text |  |  |

**Instructions:** _(natural language, optional)_

## 10. Page one `page_one`

What a reader who stops after page 1 must already see.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Must show on page 1 | `must_show` | list |  |  |

**Instructions:** _(natural language, optional)_

## 11. Layout and ATS `layout`

Formatting that keeps resumes readable and ATS-safe.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Columns | `columns` | select | Single column / Two columns |  |
| Standard headings | `headings` | multi select | Summary / Experience / Education / Skills / Certifications / Projects |  |
| Disallowed elements | `disallowed_elements` | multi select | Tables / Text boxes / Icons / Photos / Key content in headers or footers |  |
| Allowed fonts | `fonts` | multi select | Calibri / Arial / Helvetica / Garamond / Georgia |  |
| Font size (pt) | `font_size_pt` | range |  |  |
| Date format | `date_format` | text |  |  |
| Outputs | `outputs` | multi select | Text-based PDF / Editable Google Doc / Word document |  |
| Bullet length | `bullet_length` | select | One line / One to two lines / Up to three lines |  |
| Bullet pattern | `bullet_pattern` | select | Action, scope and result / Free form |  |

**Instructions:** _(natural language, optional)_

## 12. Structure `structure`

Section order and per-section content rules.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Sections in order | `sections` | table | see below | |

**Sections in order** `sections`: One row per resume section.

| order | section | content_rule | default_state |
|---|---|---|---|
|  |  |  |  |

**Instructions:** _(natural language, optional)_

## 13. Positioning `positioning`

What each base leads with and the evidence behind it.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Positioning by base | `by_base` | table | see below | |

**Positioning by base** `by_base`: One row per base.

| base_id | lead_with | evidence | avoid |
|---|---|---|---|
|  |  |  |  |

**Instructions:** _(natural language, optional)_

## 14. Language `language`

Tone and wording rules.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Positioning level | `level` | select | Senior / Staff / Principal / Staff or Principal / Director |  |
| Style rules | `style_rules` | multi select | State what was owned, decided and changed, not task lists / Plain, specific verbs / No filler words / Spell out abbreviations once / No employer-internal terms or internal product comparisons |  |
| Never present as highlights or skills | `not_highlights` | list |  |  |

**Instructions:** _(natural language, optional)_

## 15. Files and verification `files`

Where versions are stored and what is checked before approval.

| Field | ID | Type | Options | Value |
|---|---|---|---|---|
| Storage | `storage` | select | Registered Role specific folder |  |
| Naming | `naming` | select | RESUME-FILES.md |  |
| Base registration | `base_registration` | select | Settings base_resumes |  |
| Checks before approval | `pre_approval_checks` | multi select | Every fact checked against the master / Rendered PDF inspected / Guideline checklist passed / Same-company consistency checked |  |

**Instructions:** _(natural language, optional)_
