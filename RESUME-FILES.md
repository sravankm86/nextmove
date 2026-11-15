# Resume files and versions

Drive stores content. Airtable stores the exact file reference, version and verification. A filename alone never identifies the submitted resume.

## Names

Use readable names with these patterns. Values below are fictional.

| File | Pattern | Example |
|---|---|---|
| Editable master | Name_Master_Resume | Alex_Rivera_Master_Resume |
| Approved base PDF | Name_Base_Resume_YYYYMMDD_vNN.pdf | Alex_Rivera_Base_Resume_20261115_v01.pdf |
| Role PDF | Name_Company_Role_JobID_YYYYMMDD_vNN.pdf | Alex_Rivera_ExampleCo_Principal_PM_R12345_20261115_v01.pdf |
| Role editable source, when created | Same stem as role PDF | Alex_Rivera_ExampleCo_Principal_PM_R12345_20261115_v01.docx |
| Change notes, when a separate file is useful | Same stem plus _Changes | Alex_Rivera_ExampleCo_Principal_PM_R12345_20261115_v01_Changes.md |

Use the user's preferred application name, underscores between words, ASCII letters/digits where practical and a short readable company/role. Remove filesystem separators and control characters. JobID is the real requisition ID; if absent use the first 10 hexadecimal characters of SHA-256 of the canonical Job key and record that mapping. Do not invent a requisition. Use the Run's recorded timezone/date; if none is configured use UTC and record that choice. vNN starts at v01 and increases for changed content; include more digits if needed. Do not use final, final2 or latest as version identifiers. If a filename is already occupied by different content, allocate the next version; Drive allows duplicate names, so check IDs and content too.

## Create and reuse

Never rename or edit the factual master merely to enforce this convention. Keep existing approved files usable by verified reference; apply the convention to new files. Register the master and approved base separately in Settings. Do not create another master from a goals document.

Prepare may reuse an approved base PDF when it fits the role. Store its exact reference/version and record base reuse with no tailoring; a duplicate role-named copy is optional, not proof of readiness. For a tailored version, create a new file, retain prior files and record its parent/master version, job identity, changes and verification. Do not overwrite a file that has been submitted.

Before Ready verify claims against the master, check the full relevant JD, inspect the rendered PDF for layout/readability and store Resume link, Resume file name, Resume version, Resume verified at and change notes on Applications. Evidence versions (JSON) records master/goals/JD/instruction versions and PDF verification. Resume version is a SHA-256 of the exact PDF bytes or a durable provider version tied to verified content; name/date alone is insufficient. If bytes cannot be hashed, record the supported provider version and how content was verified; unresolved version identity blocks submission.

Use the user's requested page count. If unspecified, preserve the approved base length or ask when length materially changes the result; do not silently force every resume to one page. Keep the editable source when created. A factual or visual verification failure blocks Ready.

Apply downloads/uses the exact accepted PDF, verifies the reference/version and records it as Submitted resume version before submission. Later edits require a new version and do not change prior submission history. A mismatch pauses that application. Follow stages/prepare.md and stages/apply.md.
