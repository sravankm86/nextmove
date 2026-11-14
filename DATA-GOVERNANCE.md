# Data governance and operation history

## Requirement and present boundary

Audit all controlled CRUD operations, including reads, with record and field scope. Preserve reconstructable changes and stable identities. Treat this as a requirement, not a claim that Airtable enforces it.

Airtable gives every record a unique immutable record ID. Its primary display field need not be unique. Native record revision history shows changes and actors but is plan-retained; the documented Free retention is two weeks. It is not an all-read access journal. The Web API does not expose record revision history for export. A custom Audit Events table remains editable by sufficiently privileged collaborators; it is not an immutable audit system.

The instructions and schema do not install a gateway, permissions, transaction hooks, scheduling or a universal UI/API interceptor. Do not claim complete CRUD coverage until every permitted access path and failure case is verified. Creating logs today cannot reconstruct unknown prior edits or readers. Record bootstrap observations honestly with their actual recording time and known scope.

## Audit Events contract

Keep this operation journal separate from scan coverage, mailbox audits and lifecycle business events.

Each operation has a unique operation ID and idempotent event keys for intent and outcome. Record:

- UTC recording time; actual occurrence time only when known.
- Authenticated collaborator/integration identity plus the worker/channel and run ID. Do not invent a human actor behind a shared integration.
- Stable base/table/record IDs, immutable entity identity and affected field IDs/names. Names alone may change.
- Operation type, purpose/source, intent and Succeeded/Failed/Uncertain outcome.
- For creates, initial persisted values; for updates, changed fields with explicit before/after values including null/cleared values; for archives, prior state and archive metadata.
- For reads, requested fields, query/filter scope, returned record IDs, page/cursor scope, count and outcome. Log aggregate reads as aggregate scope; do not fabricate a per-record read where IDs were not returned.
- For schema changes, previous/new field or table definitions, actual tool outcome and verification. Computed or reverse-linked fields are derived effects; distinguish them from human business edits.

Populate the Application link on application audit events using the actual record ID, so the row exposes its related history. Keep the generic Table ID and Record ID even when linked fields are also present.

Use an array in Field changes (JSON), for example:
`[{"field_id":"<private field ID>","field_name":"Lifecycle status","before":"Queued","after":"Shortlisted"}]`.
Filter Audit Events by Table ID and Record ID for one row, or inspect its linked Application events. Field IDs identify column history within those changes. Keep audit payloads private and out of model context; never log credentials. Keep document/mail bodies in Drive and retain accessible evidence references rather than duplicating full content.

## Controlled access protocol

1. Check authorization, live controls, exclusive writer ownership and configured audit readiness. Discover live schema. Persist and verify an audit intent before a controlled data read or mutation; its intended field/query scope must be known.
2. Perform the read, paginate completely as required and persist the returned scope/outcome. Large read scopes may use bounded journal chunks under the same operation ID. Stop processing undisclosed results if outcome logging fails; checkpoint the coverage gap.
3. For mutation, the audited preflight reads current values, versions, identities and linked targets. Enforce the expected prior state, reconcile concurrent edits and compute only intended changes. Persist the before/expected-after intent before modifying business records.
4. Perform a payload-aware write. Read back and compare actual persisted changed and preserved values/relationships. Include verification-read scope in the operation's journal. Append a verified outcome; do not overwrite intent as if it were a committed result.
5. On uncertain writes or journal failure, stop dependent work and reconcile actual records before retrying. Airtable's separate business and audit writes are not atomic. An audit intent is evidence of an attempt, not a committed change. Do not claim exactly-once or transactional enforcement.
6. Audit inspection and audit journal I/O use a documented nonrecursive bootstrap boundary; they cannot be used to conceal ordinary business reads or mutations. A deployment requiring audit-system self-access auditing needs a separate protected platform log.

Keep journal entries append-only by writer policy, retain failed attempts, and correct errors with another linked entry. Owners can still alter the table unless separately restricted. Hard deletion is disabled for normal workers. Archive records using Archived at and preserve references; physical purges require a separate explicit instruction, dependency assessment and durable pre-delete evidence. Never cascade-delete company/application history by default.

## Identity and relational rules

- Use immutable Airtable record IDs as technical primary identities. Expose Record ID = RECORD_ID() for reliable row identification. Use separate namespaced business keys for idempotent discovery and cross-system matching.
- Check company_key, job_key, source_id, run_id, policy/event/operation keys for duplicates within their documented scope. Titles, display names and URLs with discarded identity parameters are not safe keys. Multiple legitimate application attempts need distinct attempt identities; never collapse them silently.
- Historical applications may lack a job key or current target-company link. Keep their immutable record identity and provenance, flag unresolved matching and never invent a relationship or automatically allow a company.
- Link entities by real record IDs, validate referenced targets and enforce intended cardinality in the writer. One application normally has at most one canonical company and inventory job; a company's reverse link can contain many applications. Airtable's multiple-record field does not itself enforce one-to-many cardinality.
- Normalize current canonical entities, mutable company policies and append-only events separately. Distinguish intentional historical snapshots from accidentally duplicated current state. Design source membership junctions when a canonical posting belongs to multiple boards; do not overwrite source provenance.
- Use typed dates, numbers and enums for operational fields. Preserve raw original values separately and surface parse failures. Existing text run/source references and legacy audit counts are not declared normalized merely because migration succeeded; typed/link backfills require verified changes and their own audit.
- Keep recorded/system timestamps separate from application, confirmation, rejection and posting event dates. Never infer missing historical times from record creation or latest modification.
- Validate required fields, enum choices, current-state transitions, archived targets and all scoped key/link rules before writes. Reconcile human edits. Record the actual scope of an integrity check; inspecting a few tables does not prove every inventory row valid.

Airtable does not provide SQL PRIMARY KEY/UNIQUE/FOREIGN KEY/CHECK constraints and transactions for these business rules through this setup. Writer checks reduce errors but other access paths can bypass them. Do not equate upsert with uniqueness enforcement, linked records with restricted deletes, or single-writer instructions with a database lock.

## Coverage, retention and architecture decision

Private Controls must distinguish requirement, configured schema, functioning access layer, permission coverage, last tested evidence and remaining gaps. Keep submissions paused and do not enable workers that cannot honor their audit requirement.

Strict all-path CRUD/read auditing and database-enforced constraints require a controlled deployment: for example PostgreSQL with primary/unique/foreign-key/check constraints, transactional change logging, protected audit storage and an access layer plus database auditing that covers reads and privileged access. PostgreSQL alone does not automatically log every read or make administrator changes tamper-proof. An Airtable interface/sync must not become an unaudited write path. Evaluate retention, costs, access paths and recovery before a separate authorized migration.

Official references:
- https://support.airtable.com/articles/3516802427-record-level-revision-history-in-airtable
- https://support.airtable.com/articles/8978269981-the-primary-field-in-airtable
