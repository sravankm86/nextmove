# Scan official job catalogs

Use complete catalog checks with incremental processing. Keep bulk parsing, comparisons, filtering, checkpointing and verification in code. Give the model compact summaries, ambiguous decisions and specific failures, not whole catalogs, descriptions, HTML or spreadsheet readbacks.

## Inputs and reusable state

Load the run ID, mode, live Target Companies and Applications fields, controls, private criteria and prior inventory. Include every Allow company; Exclude wins on duplicate rows. Preserve Pool and user choices. Record instruction, reader, normalizer, criteria and filter versions. Recheck controls and company choices before writes.

Reuse the private source registry and tested readers. Maintain a stable company ID and a source ID per official board/region, with careers URL, catalog endpoint, company-scope rule, reader location/version, pagination contract and validation evidence. Parent-company and VC portfolio jobs do not automatically belong to an allowed employer.

Revalidate the official careers source manifest each run, including dynamic configuration supplying board links. A reliable conditional response may reuse an unchanged manifest. Validate new or changed sources and readers. Confirm retirement/redirection before removing a known source. An unverified manifest or region is a configuration coverage gap, not permission to shrink the plan.

Persist the run plan, manifest, reader versions, page/cursor progress, counts, identity aliases, field hashes, change-version evidence, descriptions and exceptions in an existing authorized private destination. Keep user data, links and credentials outside public Git. Temporary local files alone are not durable state. If durable state/readers are unavailable, report the setup gap and run a baseline; do not claim incremental support. New storage destinations require authorization.

Resume unfinished sources under the same run ID. Reuse completed work unless inputs change or validation fails. Rescan and deduplicate a source when its cursor expires or checkpoint no longer matches pagination.

## Enumeration and change detection

Collect every posting's metadata before filtering. Follow every page/cursor to a verified end. Check advertised counts, unique IDs, final-page behavior, repeated pages/cursors, caps, unexpected empty responses and malformed records. Preserve unresolved records. Search results alone cannot establish coverage; use search/browser diagnosis for source discovery or a specific failure.

An unchanged complete feed may reuse cached inventory only when a current authoritative version/conditional response proves the entire resource unchanged and its cached enumeration passed checks. A page-one 304, unchanged count or unchanged first page does not prove later pages unchanged. Otherwise enumerate every page again.

A change feed may replace enumeration only after validating additions, edits, removals, ordering, catch-up/retention semantics, baseline, watermark and verified end. Detect expired cursors and missing events; fall back to a full source scan. Created-since searches alone are insufficient. Audit the method and evidence.

Save requisition ID, stable source posting ID, canonical URL, title, all locations/work arrangements and observation time.

For every queued candidate, also capture the exact posting's advertised salary, work-location details and job-posted date. Preserve raw salary text and any stated range, currency, pay period, base/total/equity basis and applicable geography in posted_salary/salary_details; do not estimate or borrow another role's band. Store remote/hybrid/on-site mode only when stated, with allowed countries/regions, offices and restrictions in location/location_details/work_arrangement. Store job_posted_at separately from date_found and observation/update dates. Keep relative date text in job_posted_text; do not turn an ambiguous “days ago” value into an invented exact date. Preserve source URL and observation provenance, make missing values explicitly unknown/unavailable, and do not drop a plausible candidate just because salary/date/location metadata is missing. Reuse current verified feed/detail data and code extraction before escalating an individual metadata gap.

Record metadata gaps separately from coverage and fit, and include these fields in metadata change hashes. Deduplicate within a company using a genuine shared requisition ID. Ignore placeholders such as “See Opening ID”, “N/A” and “undefined”; otherwise use a namespaced source ID or canonical URL. Preserve identity-bearing URL parameters, source memberships and locations. Keep contradictory availability unverified. Flag suspected cross-board duplicates and legacy title-only matches; title equality alone does not prove an exact submission or disposition.

Compare normalized metadata and description hashes separately. Track new, metadata-changed, description-changed, unchanged, missing and unclassified records. Version changes require revalidation, not a claim that the employer edited a posting.

Unchanged metadata does not prove an unchanged description. Reuse a description as current only when current feed content matches, a reliable employer version covers description edits, or a conditional detail request confirms it unchanged. Otherwise refresh the required description. An unverified cache reuse must be labeled stale/unverified; do not silently introduce a freshness TTL.

## First-pass filter and description policy

Apply only explicit broad role-family, seniority and geography/work-arrangement criteria to catalog metadata. Exclude clear mismatches; retain plausible adjacent titles and missing, ambiguous or unclassifiable metadata. Deterministic rules must implement explicit criteria. New exclusion rules and uncertain cases require review or retention, not silent rejection. Record the decision, reason and criteria/filter version. Ask for missing criteria or record unapplied filters. Leave fit ratings blank.

Read the company application-restriction fields in Target Companies (see SETUP.md, Company application restrictions). Application quotas and rejection cooldowns do not change Search status or remove jobs from inventory. Continue scanning Allow companies and saving broad matches as Queued while held; annotate a known submission blocker separately from fit and lifecycle status. Do not infer a company-wide cooldown from a generic rejection, clear a hold based only on a past date, or submit during scan.

Default description policy: all. Capture a full description or an accessible private reference to its full content for every posting, reusing verified unchanged content. A public URL or summary is not a captured full description. Retain descriptions supplied by feeds automatically.

The user may explicitly choose candidates: individually fetch descriptions only for first-pass passes and ambiguous/unclassified records. Still inventory every posting and retain feed-supplied text. Mark clear exclusions without full text “Not requested — metadata exclusion”, not failed retrieval. This preserves catalog coverage and broad discovery under the metadata rules, but reduces archival depth: metadata mistakes can hide a relevant role, and criteria changed after closure may be impossible to reassess. Re-filter exclusions when criteria/filter versions change and fetch newly relevant descriptions while available. Never enable this policy silently.

Distinguish full/revalidated, reused but unverified, summary only, failed retrieval, not attempted, policy-not-requested and confirmed closed records. Do not shortlist without a verified full description. An available broad match may be saved before description assessment, with the gap reported. Conflicting official availability is held out of new Applications writes.

## Runtime and recovery

Prefer bounded code concurrency for HTTP work, honoring provider limits and Retry-After. Use one coordinator. Model workers, when requested or needed for a specific exception, receive disjoint sources and compact evidence, contracts and failures. They return durable artifacts, counts and errors; they do not mutate shared tracker state. Wait for results or explicit interrupted/deferred checkpoints before finalizing coverage.

Avoid one model/tool turn per job, repeated discovery, whole-page dumps, and repeating identical permanent failures without new evidence. Use reasonable transient retries and pagination guards.

Recovery budgets are optional and disabled by default. A user-selected attempt/time/model-escalation budget limits recovery effort, and may leave recoverable sources Partial/Failed until another run. On exhaustion checkpoint progress and record “Budget exhausted”. Never claim Complete, false zero or omit a source because of a budget. Honor stop controls at checkpoints.

## Delta writes and verification

Follow ../STORAGE.md. Save the full metadata inventory in Airtable Job Inventory. Keep captured full descriptions in Drive with accessible private references; keep hashes, source/reader metadata, checkpoints and exceptions in the mapped Airtable tables. Retain reusable reader artifacts in the configured durable content/runtime location. Map optional fields during authorized setup; do not assume columns or overwrite unrelated data. Do not export private tracker/profile snapshots to a new archive by default.

Use LIFECYCLE.md as the current status contract; legacy pipeline values are history, not a second active state. Never reset a tracked role to Queued on a new scan. Only the coordinator writes. Reread affected rows and match stable identities. Upsert every verified first-pass match into Applications; new rows get lifecycle status Queued, company, title, salary details, work location/arrangement, job-posted date (or explicit missing status), URL, date found, run ID and first-pass reason. Match exact tracked roles instead of duplicating them. Preserve historical status, notes, fit decisions, submissions and exact-role Not applying/Role not available semantics. Queued does not mean submitted or CV-ready.

Write only inserted/changed fields. Update last-seen observations in compact batches; do not rewrite unchanged descriptions or fit/history columns. Reevaluate affected inventory when criteria change, preserve historical fit decisions, and set review_pending and next_owner Reviewer on affected pre-submission assessed roles (including Not a fit), with the reason/version change, instead of resetting their current lifecycle. The coordinator may compare master-version metadata without sending full resume contents through Scanner. Do not score fit during scan.

Use payload-aware batches and durable write checkpoints. Verify every write in code against actual readback: compare canonical values or hashes computed from returned content, expected keys, counts and permitted transitions. A success response, count, cached input hash or sample alone is insufficient. Read full changed descriptions back to verify storage when necessary, keeping payloads outside model context. Verify preserved fields on affected existing rows. Reconcile uncertain writes before replay; report every verified-match saved-row gap.

Keep prior observations on partial/failed runs. Mark inventory missing only after complete current coverage of all known sources, including authoritative removals from a validated change feed. Do not automatically translate missing observations into historical Applications status changes. Verify current role availability before submission or an availability-based closure/reopening. Other lifecycle changes require their exact event evidence under LIFECYCLE.md; a public posting's existence is not proof of an application outcome.

## Audit and completion

Return one audit row per source and a company rollup:

- Complete: every configured source reached a verified end, or equivalently validated unchanged/change-feed coverage; enumeration checks passed and no configuration gap remains. Zero requires verified empty coverage.
- Partial: usable postings or verified sources exist, with unresolved gaps.
- Failed: no catalog verified and no usable postings collected. Record the cause, including missing configuration.

Coverage applies to published jobs on configured official sources at scan time. Description/freshness/metadata gaps are separate from catalog coverage and fit.

Report company/source coverage, raw source observations, company-scoped/unique counts, new/changed/unchanged/missing records, first-pass decisions, description statuses, saved/matched/deferred rows, identity warnings, saved-row gaps and unresolved exceptions. Record description policy, recovery budget, cache/change-feed evidence and criteria version. Do not claim cached content was checked this run without validation. Missing posting metadata must be reported without substituting date found, estimating salary or inferring work arrangements. For a scan-only request, stop after saving and verifying the audit.
