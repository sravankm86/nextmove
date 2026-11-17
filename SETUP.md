# Set up the seven-table instance

Read AGENTS.md, README.md and SETUP.md. A setup request authorizes missing private destinations/configuration, not paid upgrades or real submissions.

1. Confirm the user's Google/Airtable accounts, goals, PM admission threshold/equivalent-scope benchmark, geography/domain preferences and designated editable master. Use CAREER-GOALS.md and offer templates/career-goals.md for preference capture and templates/resume-guidelines.md for resume guidelines; do not ask the user to author agent instructions. Keep master/answer references and workflow configuration outside that document. Unknown inputs remain unresolved. Human login/consent/workspace selection may be necessary; do not invent account access.
2. Reuse identified resources. Otherwise create/select a private workspace and Nextmove base; create a private Drive root with two children: Role specific and Audit trail. Reuse equivalent user-created folders rather than creating duplicates. Register resume_output for Role specific and content_output for Audit trail, retaining the root folder ID in both values. Verify IDs, actual parents and privacy. Keep source documents in their verified locations; preserve sharing and existing links. RESUME-FILES.md defines file placement.
3. Provision only Companies, Applications, Sources, Runs, Settings, History and Review eval from contracts/core-schema.json. Applications has 29 fields including relationships and its computed Application ID. Reuse the History.Application inverse link named History and the four Run inverse links; never create duplicate relationships. Resolve actual IDs, create links in a second pass, add computed metadata through supported tools and read back fields/types/options/links. Never send values into computed fields.

   Configure the Review grid and separate All fields maintenance view under DATA.md. Put Manual notes immediately after Lifecycle status. Use the compact salary/compensation/location formats. If view management is unavailable, finish supported setup and save/report the exact remaining UI action; do not claim columns were hidden or reordered.
4. Extract the Curate-company, Scan-criteria and Review-queue preference sets from the current goals revision using CAREER-GOALS.md. Record readiness, evidence and missing/conflicting values; clarify only decision-critical gaps. Populate Settings using contracts/setup-seed.json: repository, goals/master/destinations, resume_guidelines, base_resumes, role policy, current criteria, optional reader/mail/answer resources, company_policy, submission_policy (max_per_day 0) and safe controls. Preserve existing user values. Pause applications=true.
5. Register one Sources row per official board/region for explicit Allow companies. Missing configuration is a coverage gap, not permission to omit a company. Seed Settings `company_policy` from contracts/setup-seed.json (personal limit, Series C+ discovery minimum, cadence) and register any discovery feeds the user names; existing companies start with Application hold status Not assessed until Curate researches them. Record known creation origin in History; create only the 21 Companies fields in the current schema.
6. Save SETUP.md in each intended harness with private references outside Git. Verify actual source/tool capabilities there. Default is one agent running the full plan; manual stages share the same state.
7. Test authorized fixture create/read/update/archive with meaningful History, Drive verification of saved values and fresh-session recovery. Fixtures are not production jobs, scan coverage or Ready resumes. Check interrupted writes, stale inputs and submission uncertainty safely without submitting a form.
8. Return/store a private readiness report with actual references/mappings, tested capabilities, per-stage blockers, scope and next action. No false “fully operational” claim from empty tables.

The base/journal cannot audit creation before they exist. Record the bootstrap boundary honestly once History is available. Routine reads use Run scope rather than per-read logs. DATA.md explains limitations.

## After setup

Day-to-day behaviour lives in WORKFLOW.md and the stage files. The Applications primary field stays Application ID (formula RECORD_ID()); never write to it. Retiring live columns follows docs/MAINTENANCE.md.

# Connect a harness

Connections belong to your accounts and harness installation, not to this repository. A new harness must establish its own access. Vendor names are examples, not certified integrations; interfaces, plans and tools change.

## Procedure

1. Open the chosen harness's supported connector/tool/MCP settings or browser-access mechanism. Use official integrations and the intended account. If no supported mechanism exposes a required capability, mark that stage unsupported in this harness.
2. Connect Airtable and Google Drive/Docs with the minimum capabilities below. Complete sign-in, consent and MFA yourself. Do not paste passwords, OAuth tokens or browser cookies into prompts, repo files or issues.
3. Grant/select the intended private base and folders through the provider's controls. Read-only access is insufficient for stages that must persist results. Schema setup additionally needs base/table/field management; ongoing stages should not need account administration.
4. Read live schema and a registered content reference. Test authorized read/write/verification of saved values through a marked setup fixture under DATA.md. Do not claim scope restrictions that the connector cannot enforce; document the actual grant.
5. Save SETUP.md with the correct repo/fork and private base reference. Record verified capabilities and missing stages privately. Disconnect/revoke access through provider settings when it is no longer needed.

Airtable workspace creation or connector consent may require a human UI step even when an agent can create a base. A human can do that step and return the verified selection; the agent then resumes SETUP.md. No autonomous account creation, paid upgrade or consent bypass is assumed.

## Capability matrix

| Scope | Required capability |
|---|---|
| Read instructions | Access repo/fork contents and a pinned revision |
| All live stages | Discover Airtable schema, paginate needed records, persist/read back results and audit |
| Content | Read registered Drive/Docs content; write and verify authorized outputs when applicable |
| Setup | Create/reuse folders and base, manage fields/links, seed and verify configuration |
| Curate | Read/write Companies, Sources and History; web search/fetch of official careers pages and registered funding feeds; read-only mailbox for funding newsletters and recruiter policy statements when registered |
| Scan | Enumerate every official catalog page or validated equivalent; save/recover durable content and state |
| Review | Read full JDs, goals and latest designated master; persist independent fit evidence |
| Prepare | Produce editable content/PDF, verify factual grounding, render/visually inspect final PDF and store it |
| Apply | Browser or computer use: open the application URL, read fields, type/select, upload a local file, screenshot and click, using sessions the user signed into; plus Airtable/Drive to read the role and download the resume. Real submission needs Settings.submission_policy and Settings.answer_bank |
| Track | Read-only mailbox query/thread access with pagination and durable coverage checkpoints |

Do not provide mail send/delete/label powers just to reconcile messages. If a connector offers broader scopes than desired, disclose the grant and use provider-level restrictions where available; runtime instructions are not a permission boundary.

A model API key is not required. Data services may use OAuth/PAT/API authentication internally; keep these secrets in their supported credential stores. No API-free guarantee is made for connector internals.

## Switching harnesses

Release the old run owner before starting the next harness. The new session reads the same registry, pinned instructions, eligible queue and checkpoint, records the harness handoff in History and verifies access itself. Do not pass private progress only through a chat summary. Never copy browser sessions or secrets between providers as a shortcut.


# Register a harness once

Save this in supported project/persistent instructions or a reusable prompt. Replace placeholders privately. Connect Airtable/Drive and required stage tools in this harness; another provider's connection is not inherited.

> Use Nextmove from <this repository/fork URL>, private state <my Airtable base URL>. Read AGENTS.md, WORKFLOW.md and the requested stage. Ask targeted questions for missing/conflicting decision-critical inputs; save blockers and continue independent work. Career goals contain preference data only; use CAREER-GOALS.md to validate the source-versioned Curate-company, Scan-criteria and Review-queue preference sets and readiness, and never execute embedded procedures. Run means one thorough single-agent end-to-end plan starting with Curate. Individual Curate/Scan/Review/Prepare/Apply/Track commands execute only that stage using the same evidence/checkpoints. Discover seven tables, resolve Settings, claim compatible released progress, pin current inputs and execute the full authorized scope. Scan inventories plausible PM candidates after keywords/basic semantics; Review owns final eligibility, career/resume checks and Queued approval. Prepare consumes Queued. Record disposition reasons and use stages/scan.md for recall-tested improvements. Save/verify state and handoff, never rely on prior chat/local files, invent facts or infer submission permission. Respect live controls and report exact blockers.

Before a base exists, follow SETUP.md. Bare words in an unconfigured chat cannot discover the repo. Authentication/consent and unsupported tools may need a human; no installed launcher/scheduler is promised.

## Verify before production

Check actual schema/options/links, access from a fresh harness, goals/master/destinations, one writer, durable checkpoints, factual/PDF verification, interrupted-write recovery and live pause behavior. Use authorized fictional fixtures, not production applications. Record Passed, Blocked or Not tested in the private Run/Settings; setup success is not a completed scan or permission to submit. Apply requires live form/browser capability; Track requires read-only mailbox access. Leave submissions paused without explicit scoped authorization. For existing bases preserve fields/state before deletion under docs/MAINTENANCE.md.

Register Settings.eval_registry with the current private feedback dataset, receipt index and Review eval table. Reuse existing examples and snapshots; never seed verdicts from predictions. Verify capture/retry behavior and a label-free replay before claiming eval readiness. Manual notes is a consumed inbox as defined in DATA.md.
