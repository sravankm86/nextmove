# Meaningful history and integrity

Log meaningful mutations/business events and run-level read scope. Do not create a row for every routine read/page. This deliberately relaxes the former all-CRUD/read-audit requirement; it is not universal access auditing.

History records stable event/operation identity, actor/harness, affected table/record/field, before/after values, evidence, actual known event time and recording time. Keep receipts, non-regressing older outcomes, failures, uncertainty and corrections even without a current-state transition.

Normal job changes retain exact deltas and an application link. Bounded migrations may use verified private per-record delta artifacts with hashes, ID index, Run and accessible History manifest. Preserve old versions/references. Audit-system I/O is nonrecursive; intents are attempts, not committed results.

Airtable business/history writes are not atomic. Reconcile actual persisted state before retry; uncertain writes stop dependent work. Native IDs are technical identities, while business keys, link cardinality, current states and human edits are validated by the writer. Display fields/upserts/ownership labels are not SQL constraints or locks.

Keep availability, admission, career alignment, fit and application outcomes separate. Goals define preferences; the master defines candidate facts. Preserve known dates and scoped company rules. Submit requires a distinct attempt identity, resume version and explicit live authorization; uncertainty blocks retry.

No automatic purge, retention window, paid upgrade or public archive is implied. Filters/Archived flags do not reclaim capacity. Retirement requires authorization, dependency checks, durable verified backup and recoverable mappings. One-off old raw backups are not active inventory.

Migration cannot audit itself before its sink exists. Record bootstrap honestly; never fabricate prior events or bypass automatic approval rejection. Target only authorized private destinations. Owners can edit logs and direct UI/API access can bypass writer rules; strict all-path auditing/SQL enforcement needs a separately designed protected platform.
