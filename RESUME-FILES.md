# Resume files and versions

Drive stores content. Airtable stores the exact file reference, version and verification. A filename alone never proves the exact Ready artifact.

## Folder placement

Setup creates or reuses two folders directly inside the designated private main folder:

- Role specific: customized resume PDFs, editable counterparts and role-specific change notes. Use the registered resume_output folder.
- Audit trail: run reports, job captures, assessment evidence, process metadata, manifests, verification results and preserved column archives. Use the registered content_output folder.

Keep Career Goals, the factual master and approved reusable base at their registered locations; moving them is unnecessary. Reuse equivalent existing names, including longer user labels. An existing Archived resumes folder is optional user organization, not another mandatory setup destination. Do not automatically archive or alter submitted files.

For an authorized cleanup, inspect each file and its current parents, save a move manifest in History, change only the verified parent and read back the result. Moving a Drive file preserves its ID and links. Never delete, overwrite or change sharing just to organize folders. Missing or ambiguous destination mappings block affected writes rather than falling back to a cluttered main folder.

## Names

Use readable names with these patterns. Values below are fictional.

| File | Pattern | Example |
|---|---|---|
| Editable master | Name_Master_Resume | Alex_Rivera_Master_Resume |
| Approved base PDF | Name_Base_Theme_YYYYMMDD_vNN.pdf (Theme optional for a single base) | Alex_Rivera_Base_Platform_20261115_v01.pdf |
| Role PDF | Name_Company_Role_JobID_YYYYMMDD_vNN.pdf | Alex_Rivera_ExampleCo_Principal_Analyst_R12345_20261115_v01.pdf |
| Role editable source, when created | Same stem as role PDF | Alex_Rivera_ExampleCo_Principal_Analyst_R12345_20261115_v01.docx |
| Change notes, when a separate file is useful | Same stem plus _Changes | Alex_Rivera_ExampleCo_Principal_Analyst_R12345_20261115_v01_Changes.md |

Use the user's preferred application name, underscores between words, ASCII letters/digits where practical and a short readable company/role. Remove filesystem separators and control characters. JobID is the real requisition ID; if absent use the first 10 hexadecimal characters of SHA-256 of the canonical Job key and record that mapping. Do not invent a requisition. Use the Run's recorded timezone/date; if none is configured use UTC and record that choice. vNN starts at v01 and increases for changed content; include more digits if needed. Do not use final, final2 or latest as version identifiers. If a filename is already occupied by different content, allocate the next version; Drive allows duplicate names, so check IDs and content too.

## Create and reuse

Never rename or edit the factual master merely to enforce this convention. Keep existing approved files usable by verified reference; apply the convention to new files. Register the master and approved base separately in Settings. Do not create another master from a goals document.

Bases are created and reworked offline by the user as a one-off workflow, following their private resume guidelines (standard frame: contracts/resume-guidelines-schema.json, blank form templates/resume-guidelines.md); these instructions do not create bases. Register each approved base in Settings.base_resumes with its theme/variant, length, PDF and editable references, content hash and the master version it was built from. A base built from an older master is stale for reuse until refreshed.

Prepare (stages/prepare.md) either reuses an approved base PDF that fully covers the role, recording its exact reference/version and base reuse with no tailoring (a duplicate role-named copy is optional, not proof of readiness), or creates a tailored role version from the closest base under the registered resume guidelines. For a tailored version, create a new file, retain prior files and record its parent base, master and guidelines versions, job identity, changes and verification. Do not overwrite a file that has been submitted.

Before Ready verify claims against the master, check the full relevant JD, inspect the rendered PDF for layout/readability and store Resume link, Resume version, Resume verified at and Preparation run on Applications. The preparation snapshot/result records the real filename, grounded changes/base reuse, master/goals/JD/policy versions and PDF verification under DATA.md. Resume version is a SHA-256 of the exact PDF bytes or a durable provider version tied to verified content; name/date alone is insufficient. If bytes cannot be hashed, record the supported provider version and how content was verified; unresolved version identity blocks Ready.

Use the user's requested page count, then the length rules in the registered resume guidelines. If neither specifies, preserve the approved base length or ask when length materially changes the result; do not silently force every resume to one page. Keep the editable source when created. A factual or visual verification failure blocks Ready.

The Ready handoff contains the exact verified PDF link/version, an editable source when created, grounded changes or base reuse, and any honest gaps. The workflow stops there. The user handles all later steps. Preserve previously used versions and historical evidence; later resume edits create a new version without changing those facts.
