# Storage contract

## Authority and discovery

Airtable owns structured state: target-company choices, applications and lifecycle, job metadata, company restrictions, controls, source catalogs and audit/checkpoint records. Google Drive owns all content: the editable master resume, approved PDFs, captured full job descriptions and durable content artifacts. Airtable stores accessible private references, not copies of full document bodies. Existing Drive spreadsheets may remain content sources and migration backups; after verified cutover they are not a second active tracker.

Resolve the private workspace/base and discover live tables, field IDs, types and select choices. Workspace names alone do not identify a base. Use the native Airtable connector when it provides the required operation. Map logical template fields to live fields without assuming names, order or generated IDs. Real base IDs, resource URLs, personal records, credentials and migration snapshots never belong in this public repository.

## Logical tables

| Table | Responsibility |
|---|---|
| Target Companies | Authoritative Allow/Exclude, Pool, company research and current restriction summary |
| Applications | One current lifecycle state per tracked role, independent fit evidence, salary/location/posted-date metadata and resume/content links |
| Company Policies | Optional individual confirmed limits, cooldowns and manual holds when a company needs multiple rules; link to Target Companies |
| Job Inventory | Every observed posting's metadata, identity, availability, first-pass decision and captured-content reference |
| Catalog Sources | One official source/region per stable source ID, with configuration and coverage gaps |
| Scan Audit / Runs | Source coverage, actual run provenance, errors and durable checkpoints |
| Lifecycle Events / Mail Audit | Idempotent transition evidence and mailbox coverage/checkpoints when configured |
| Context Registry / Stage Config | Private resource discovery, command defaults and per-stage readiness |
| Stage Runs / Work Items / Task Attempts | Durable invocation, frozen queue, ownership, progress, retry evidence and handoff |
| Artifacts | Drive content references, producing task, input versions and verification |
| Audit Events | General operation journal: stable operation/event ID, table/record/field scope, actor, before/after values, verified outcome and read scope; policy-based append-only |
| Controls | Live pause/stop and verified migration state; never implicit submission authorization |

Use stable company/job/source/event keys for identity; Airtable record IDs implement links. Historical applications outside the current target list retain company text without automatically creating or allowing a target. Optional Company Policies records must not duplicate quota counting or override confirmed rules silently. Blank restrictions mean unrecorded, not unlimited. Preserve every applicable scope/window and follow SETUP.md for eligibility.

## Data governance

Follow [DATA-GOVERNANCE.md](DATA-GOVERNANCE.md) for all controlled CRUD, including reads, row/field history, identity, relationships, archival and honest enforcement reporting. Scan Audit and Lifecycle Events serve specific domain purposes; neither replaces the general Audit Events journal. Airtable record IDs are immutable identities; primary display fields and merge keys do not enforce SQL uniqueness. Existing migrated text fields are provenance until a verified typed/link migration is completed.

## Reads, writes and fidelity

Keep bulk I/O, normalization, pagination, hashing and verification in code. Return compact summaries to the model. Paginate all relevant Airtable records; a first page is not a complete tracker. Select only needed fields. Do not reload document bodies merely to compare metadata. Respect connector batch and payload limits and provider rate limits; bounded requests are not multiple competing writers.

One coordinator owns mutations. Reread affected records, reconcile human edits and write only intended changed fields. Airtable record links and upsert operations do not replace exclusive ownership or prove an atomic compare-and-set. Use stable unique merge keys; never deduplicate by title alone. Retry uncertain writes only after checking actual persisted records. Avoid rewriting unchanged descriptions, statuses, notes or fit history.

Read back every changed record/field and compare canonical values and relationships in code. Check expected keys, permitted status changes, preserved fields and final totals. A successful response, count or sample alone is insufficient. Preserve date-only values as dates; unknown times and historical events stay unknown. Keep original status/combined date text as provenance. Legacy Reviewed/Rated requires supported two-axis reassessment or review-owned Needs review.

A content reference must resolve to the full captured description to count as captured; an employer URL or summary alone is insufficient. Preserve description status and freshness evidence separately. Moving metadata does not validate old content or repair prior scan gaps. An imported audit is historical evidence, not a new scan.

## Migration, limits and cutover

During an authorized migration, snapshot live source schema and records, import companies/applications before auxiliary inventory, link by stable keys, preserve source provenance and verify each batch. Record verified counts, mappings, errors and the next checkpoint durably. Keep source Sheets unchanged. Declare cutover only after all requested records and relationships are verified, and record Airtable as the sole active structured store in private configuration/controls. Do not dual-write or delete the backup implicitly.

Use actual available capacity information and service errors. Do not assume that a Free label proves a particular enforced limit, split bases to evade limits, silently omit history, or purchase an upgrade. If capacity/quota blocks progress, stop affected writes, reconcile in-flight batches, save a checkpoint and report exact verified/remaining counts and the service error. Resume using the same identities after capacity is restored.

Migration changes storage only. It does not install workers/readers, resolve scan or metadata gaps, create mailbox access, enable scheduling, or authorize submissions. Preserve live pause/stop controls; apply only under the separate explicit authorization in stages/apply.md.


## Harness-independent state

[COMMANDS.md](COMMANDS.md) defines manual stage execution across fresh harness sessions. Airtable must hold operational scope, queue membership, instruction/input versions, decisions, attempts, checkpoints, verification, errors, next owner and ownership release. Drive stores the referenced content; Git stores portable instructions and reusable public code. No chat, provider-specific session, ephemeral workspace or unseen scheduler may be the sole source of progress. Each harness must verify authenticated access and write capability itself. Register unresolved inputs honestly; metadata discovery is not full content verification or permission to submit.


## Fresh installs and storage profiles

SETUP.md composes contracts/core-schema.json (eleven core tables) and contracts/state-schema.json (six execution tables), resolves generated IDs and verifies aliases/types/links. Existing schemas are preserved and mapped; these files are not a migration command. Native computed fields are never input values in upserts. Audit event identity and affected-row identity have separate mappings.

Full Airtable metadata inventory remains the default. SCALING.md documents a separate opt-in Drive-catalog profile with a verified complete artifact and Airtable candidate/operational index. Register the choice privately; do not change an existing profile, silently weaken coverage or delete rows. Both profiles keep operational progress, choices, lifecycle and decisions authoritative in Airtable and content/evidence in Drive.

