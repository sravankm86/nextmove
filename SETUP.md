# Set up a private Nextmove instance

This guide is executable by a capable setup agent and readable by a human. Start with [AGENTS.md](AGENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), [DATA-GOVERNANCE.md](DATA-GOVERNANCE.md) and [the checklist](docs/SETUP-CHECKLIST.md). The goal is verified private resources and explicit stage readiness, not an installed model service.

A request to set up Nextmove authorizes creating the missing private folders, base/tables and configuration described here. Reuse identified resources. It does not authorize purchases, account creation using invented identities, moving existing files, public sharing, importing/migrating a tracker, real job discovery or application submission. Use existing session authorization rather than repeatedly asking for the same permission.

## 1. Establish accounts, scope and capabilities

The human supplies or signs into their own Google and Airtable accounts and identifies the intended workspace/account. Collect current career goals, explicit role/seniority/geography criteria, timezone, target-company choices and designated editable master resume. Record missing inputs; never invent facts, a user preference or a master resume.

Discover the selected harness's actual tools. Determine whether it can read Git instructions, inspect/create Airtable schemas, read/write Drive content, fetch official catalogs and perform its assigned stage's document/browser/mail operations. [CONNECTORS.md](CONNECTORS.md) gives a capability matrix and connection procedure.

Logins, OAuth consent, MFA and connector installation may require the human. If workspace creation or an action is not available in the agent's tools, give the exact manual step using the official application, retain the setup plan and continue unaffected work. Do not claim an unavailable operation succeeded, ask the user to paste passwords, bypass login challenges or replace an inaccessible existing destination.

For a new user, create or select a private Airtable workspace in the intended account. If no workspace-creation tool exists: the human opens Airtable, creates/selects their workspace, grants the appropriate access to the connection and resumes setup with its verified identity. Workspace names need not be unique; verify returned IDs/account before creating the base.

## 2. Create the base and bootstrap the journal

Create or reuse a private base named Nextmove in that workspace. Record the real returned URL/ID privately. An Airtable workspace without a base/tables is not sufficient.

Read both [core-schema.json](contracts/core-schema.json) and [state-schema.json](contracts/state-schema.json). Create Audit Events early so subsequent controlled setup operations can be journaled. The base/journal cannot audit their own creation before they exist: capture the visible plan and actual tool results, then persist an honest bootstrap record once the sink is available. Leave unknown event times blank. Do not claim universal audit coverage or invent historic intents.

Use [DATA-GOVERNANCE.md](DATA-GOVERNANCE.md) for subsequent controlled reads, writes and readback. Schema inspection needed to find the journal is the narrow documented bootstrap exception. A shared integration identity must not be attributed to an invented human actor.

## 3. Build and map all seventeen logical tables

The JSON contracts are blueprints, not connector-specific request bodies. Inspect the live tool schema, supported types and batch limits before mutation.

1. Create the eleven core scalar tables and six orchestration scalar tables, with supported first/display fields. Preserve existing tables, selections, rows and legacy provenance.
2. Resolve returned table IDs. In a second pass, create links from both contracts using those IDs. Inverse link fields may be generated automatically; do not create duplicate inverse relationships blindly.
3. Add common immutable record-ID and native system metadata fields. Some connectors support computed fields only through separate field-creation calls. Never send values to computed fields during record creation/upsert.
4. Merge the orchestration contract's additional application/inventory fields by logical mapping. Do not add duplicates just because a display name differs.
5. Discover field IDs/types/select choices, validate intended cardinality and persist the logical-to-physical map privately. Native record identity is not display-field uniqueness or an atomic lock.
6. Read the schema back and compare every required table, field, enum, link target and mapping. Report missing capabilities/types instead of silently using incompatible text fields.

Audit Events has two identities: its own computed Record ID and the affected row's **Record ID reference**. Existing installations may have a text field named Record ID for the affected row; map it explicitly and preserve its meaning. Never write a target record ID into the journal's own computed identity.

Common fields in core-schema.json apply across tables; existing native metadata aliases can be mapped instead of duplicated. Created/Updated at fields used by workflow records are recording metadata, not a substitute for system metadata or business event dates. The selected runtime must implement validation and journaling; tables alone do not install those behaviors.

CSV files in [templates](templates/) are logical import headers and reference examples. They do not create Airtable links/types. Map decision to Search status, preserve Pool and require explicit Allow choices; new unknown companies are not automatically allowed. Keep Applications lifecycle separate from fit, eligibility and stage-execution status.

## 4. Create or reuse private Drive destinations

For a new user, create a private **Nextmove** root with **Resumes** and **Content** children. Resumes holds approved generated PDFs; Content holds captured descriptions, catalog artifacts and reusable content where needed. Do not create additional Research or Job Descriptions folders by default.

If the user already has appropriate destinations, register them instead of moving files or forcing this layout. Existing goals/master documents may remain in their original folders; content authority comes from the registry, not a filename guess. Preserve sharing and parents. No anonymous/public sharing is required.

Register a current goals document, using [templates/profile.md](templates/profile.md) only as a blank structure for user-provided information. The user designates the factual editable Google Doc master. An empty placeholder or an old PDF must not be marked verified master content. The latest designated master is the sole resume-fact source.

Use supported native Docs/Drive creation workflows where needed. Verify created folders/files through returned metadata/readback, exact IDs and intended access. Metadata access does not prove content was read or a folder is writable.

## 5. Populate private context, defaults and controls

Use [setup-seed.json](contracts/setup-seed.json) for required resource keys and safe seed values. Resolve private references from actual tool responses; never paste another user's IDs or real links into this repository.

Populate Context Registry with the repository/fork, structured store, career goals, master, resume destination, content destination, optional approved base, source registry and scan policy. Record real reference, version/hash, required stages, verification state and specific notes. Keep missing mailbox, reader artifacts, answer bank and submission policy explicitly unresolved. A missing optional reader cache allows baseline setup; it does not justify a false incremental claim.

Create five Stage Config rows from [commands.json](contracts/commands.json), link required context records and copy current stage paths, queue rules and pinned instruction revision into private configuration. Queue and policy values must be parsed as structured data; the string “false” must never be treated as truthy authorization.

Seed Controls with Pause applications=true, Stop all=false, honest audit coverage, manual/single-harness execution policy and setup readiness. If a control already exists, reread and preserve the user's value rather than resetting it. Submission cap remains zero, domain scope empty and authorization absent until explicitly configured.

No live Stage Runs, Work Items or application candidates should be fabricated by setup. Set up a source row per official board/region with stable company/source identity; if a company lacks known sources, record the setup gap. Capture reader/pagination contracts and durable locations before claiming supported incremental execution. Do not hardcode this repo author's targets or private criteria.

All operational scope, queues, decisions, versions, attempts, cursors, errors, verification and handoffs belong in Airtable. Drive holds the referenced content. A local config copy may be a bootstrap cache, not the only authoritative memory. If using config.example.yaml, keep the filled copy outside the repo; keep secrets in the connector's supported credential store.

## 6. Connect every executing harness

Use [CONNECTORS.md](CONNECTORS.md). One harness's OAuth grant, MCP connection, private filesystem or browser session does not appear automatically in another.

Save [HARNESS-BOOTSTRAP.md](HARNESS-BOOTSTRAP.md) as supported persistent/project instructions or a reusable task template, replacing repository and private base placeholders locally. Claude Code users can start from [CLAUDE.md](CLAUDE.md); other harnesses must load AGENTS.md explicitly if they do not discover it. Do not assume any provider supports all stage tools.

Read content through the registry and confirm actual access in that harness. Verify write capability with an authorized private setup fixture, not a real application or submission. Keep capability results per stage in private setup readiness. A plain chat with no tools is insufficient.

For one harness executing an explicit stage sequence, save the ordered execution plan as described in ARCHITECTURE.md. For manual cross-harness execution, use the same state and stage contracts. Neither arrangement changes fit, evidence, audit or submission rules.

## 7. Verify setup before reporting readiness

Complete [docs/SETUP-CHECKLIST.md](docs/SETUP-CHECKLIST.md). At minimum verify:

- All schema mappings, links, select choices, safe controls and private context references.
- A controlled create/read/update/readback/archive sequence with intent/outcome logging on a clearly marked private Context Registry setup fixture. Preserve the fixture/audit; do not use real applications or erase evidence to tidy up.
- A small authorized Drive content write/readback and artifact reference, plus a fresh-session recovery of registered inputs and saved fixture state. Do not upload real snapshots to a new archive for this test.
- Stage-specific access and a fictional or separately authorized smoke test. A readback test is not a completed production scan, reviewed queue, Ready resume or application.
- Recovery design for interrupted writes, stale inputs and uncertain submissions; test with fixtures/local simulation without submitting a form.
- The exact stage readiness, tested harness identity and remaining gaps. Do not infer universal audit coverage from a successful journal write.

No model APIs or scheduler are necessary for these interactive checks. If consent, login or a stage-specific capability remains missing, mark only the affected readiness Blocked/Needs verification and return the actionable next step. Do not declare the entire workflow operational because empty tables exist.

Return a **private setup report**: actual Drive/workspace/base links and verified IDs, logical schema map, context resources, safe controls, harness capabilities tested, audit scope/limits, stage readiness, unresolved blockers and bootstrap instructions. Store the report/reference in Controls or an authorized private artifact. Do not publish it in Git or a public issue.

## Company application restrictions

Read [docs/COMPANY-RESTRICTIONS.md](docs/COMPANY-RESTRICTIONS.md) before recording/evaluating quotas or rejection cooldowns. Preserve separate Search status, Pool, lifecycle and fit. Blank restrictions are unknown, not unlimited. A generic rejection does not create a company-wide ban; a past blocked-until date does not itself prove capacity or authorize submission.

## Existing tracker migration

Migration requires explicit authorization for the source/destination and cutover. Preserve originals, raw combined statuses/dates, user dispositions, actual event times and identity ambiguities. Legacy Reviewed/Rated is not automatically Shortlisted; unsupported positive assumptions become review-owned Needs review. Verify every changed field/link and final totals; uncertain writes are reconciled before retry.

Import core companies/applications before auxiliary inventory. Recheck actual capacity and follow [SCALING.md](SCALING.md) if an alternative storage profile is explicitly chosen. Archive does not reclaim Airtable rows. Physical deletion, paid upgrades and platform changes require their own authorization. Stop at real service limits, save a durable checkpoint and report verified/remaining counts. Do not silently truncate catalogs or split bases to evade limits.

## Ongoing operation

Use [COMMANDS.md](COMMANDS.md). Default scan description policy is all, source coverage is complete, and recovery budgets are unset unless the user explicitly chooses a tradeoff. No source TTL, sampling, page cap or candidate-only archive change is implicit.

Keep one writer, reread human edits, respect controls and verify handoffs. Application eligibility remains separate from career/resume fit. Apply defaults to preflight; real submissions require current scoped authorization, approved answers/resume, supported site, availability, quota/cooldown checks and live pause/stop gates. Tracker mail remains read-only. Setup is not standing authorization to run stages or submit.

