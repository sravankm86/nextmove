# Catalog scale without hidden discovery loss

A large company's catalog can contain thousands of roles outside your search. Enumerating them is necessary for coverage; persisting every row in a limited operational database is a separate choice. Airtable views only hide rows and do not reclaim capacity.

## Storage profiles

| Profile | Airtable | Google Drive | Tradeoff |
|---|---|---|---|
| Full Airtable inventory (default) | Every posting's metadata, candidate state, hashes/checkpoints and coverage | Captured content and artifacts | Easy direct inspection; high row/write volume |
| Drive catalog with Airtable candidate index (opt-in) | Candidates and ambiguity queue, historical tracked roles, source/run summaries, decisions, versions, artifact manifests and checkpoints | Complete unfiltered metadata catalogs, retained content and reusable artifacts | Lower Airtable row count; requires readers that verify and re-filter complete artifacts |

In the opt-in profile, Drive catalogs are versioned evidence artifacts, not a second editable application tracker. Airtable remains authoritative for operational workflow, lifecycle, choices and decisions. An artifact manifest records run/source identity, schema/reader/filter versions, content hash, row/key counts, accessible URL, pagination completion and capture status. Every planned source must be represented, including failures. Excluded rows need not become individual Airtable records, but remain recoverable from the complete catalog. Re-filter all affected records when criteria change; inspect description changes independently of title changes. Do not claim efficient delta lookup if the runtime only supports replaying whole artifacts.

Register the selected profile privately as `inventory_storage_profile`. Existing deployments retain their current profile until an explicit choice and verified migration. If no profile is registered, default to full Airtable inventory. The optional profile is an implementation contract, not an installed exporter/reader.

## Filters and evaluation

A title keyword AND a seniority word may remove most rows but miss roles with alternative titles, missing level, non-English text or firm-specific job families. Role families such as investing/portfolio operations need their own explicit criteria. Senior/Principal can also conflict with a user's actual leadership-level criteria. Retain ambiguity rather than treating absence of a keyword as proof of irrelevance.

Evaluate a proposed filter on the saved complete catalog before changing policy. Report retained counts, row reduction, true/false positives/negatives against a declared reference, missing-metadata cohorts and concrete missed-title examples. Previous first-pass decisions are a proxy, not independent ground truth. New criteria can invalidate that reference. True precision/recall requires independently assessed relevance labels, including sampled rejected roles; evaluating only retained rows cannot estimate recall.

Do not publish a user's real companies, job titles, private snapshots or experiment results as fixtures. Use fictional examples. A benchmark does not authorize deleting current inventory or changing search criteria.

## Safe migration after an explicit decision

1. Inventory active/historical applications and all incoming references; preserve tracked roles regardless of a new title rule.
2. Write complete unfiltered catalogs and required content to an authorized private Drive destination. Verify full readback, hashes, stable keys, counts and accessible references.
3. Persist the catalog manifest, source coverage, state checkpoints and chosen profile in Airtable. Test fresh-harness recovery, criteria re-filtering and missing artifact handling.
4. Compare candidate sets under the unchanged criteria. Explain differences and gaps; do not rename storage reduction as improved relevance.
5. Separately plan capacity reclamation with dependency checks and audit evidence. Archiving rows still occupies Airtable capacity; physical deletion requires explicit authorization under DATA-GOVERNANCE.md. Do not delete until the replacement is verified and rollback/recovery is concrete.

Check actual record, attachment, automation, API and Drive limits. Do not silently split bases to evade limits, buy upgrades, set page caps or replace full descriptions with summaries. Honor provider rate limits and preserve resumable checkpoints.
