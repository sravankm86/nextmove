# Nextmove universal agent instructions

Read SETUP.md and WORKFLOW.md before operating. This repository contains instructions only; all user data remains in private Google Workspace resources.

1. Discover existing tracker, master resume and resume folder from private configuration. Never hardcode a user's links, secrets, personal identifiers, or resume facts into this public repository.
2. Google Sheets is the persistent structured store: **Applications** and **Target Companies** are authoritative. Read live headers; never assume fixed column indices. Applications has one current Lifecycle status; follow LIFECYCLE.md and keep legacy pipeline/history fields as read-only provenance.
3. Before new-role discovery, read Target Companies. Enumerate official catalogs for companies with explicit Search status **Allow**; **Exclude** wins on duplicate rows. Preserve Pool and all user choices. Do not add companies automatically.
4. Reconcile recruiting messages first. Require exact role/requisition matching. Preserve dates, outcomes and user dispositions. Never let older acknowledgement overwrite later outcomes. Flag ambiguity.
5. Save verified broad matches as Queued during an authorized scan. Recommend roles only after full-description relevance assessment. Preserve exact-role **Not applying** and **Role not available** semantics; do not treat either as rejection.
6. The latest editable Google Doc master is the **sole factual resume source**. Never alter the master during tailoring or add unsupported claims. Save separate, visually verified one-page PDFs in the configured Google Drive resume folder and store links in Applications.
7. Job descriptions are referenced by canonical URL and may be captured in tracker fields/notes as needed. Company research belongs in Target Companies. Do not create separate research or job-description folders by default.
8. Write safely: reread affected rows, use stable identifiers, avoid duplicate rows, preserve existing values/notes and verify readback. Google Sheets does not offer reliable record-level transactional locking. **Only one writer may mutate shared tracker state at a time.** Multiple agents may research independently. If exclusive writer ownership cannot be established, stage changes for review instead of writing.
9. Default to review mode. Authorized prepare runs can save scan, shortlist and CV outputs. Only explicitly authorized auto-apply runs may submit and must follow stages/apply.md and live controls. Recruiting email is read-only.
10. Report scan completeness, role decisions, status changes, exceptions and unresolved submissions. Keep lifecycle status separate from relevance, temporary company holds and historical outcome notes.
