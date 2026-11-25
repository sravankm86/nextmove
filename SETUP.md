# Start a session: connection check

Every harness starts here. Discover actual tools and private references; another session's access is not inherited.

1. Find the private base from this harness's saved project instructions. If absent, ask for its link; if no base exists, follow setup below. Never guess account identifiers.
2. List the base's tables and read Settings. Map the seven active tables by ID, preserve extra legacy tables/fields and check Stop all and Active writer before writes.
3. Verify access using small reads of registered content needed for this stage: current Career Goals, master, resume guidelines and base library as applicable. Read every document tab. Open one configured official careers page for web capability. Prepare also needs both answer tables and read-only inspection of official application forms. A required login is a per-role inspection blocker for the user to resolve; never request mailbox access. Submit uses only a browser session the user already signed in to or an account stored in the harness's credential store; never ask for passwords or codes in chat.
4. Follow DATA.md "Registered sources and small artifact reads" for revision/hash checks. A changed goals document requires refreshing affected goal-derived criteria before reuse; changing a pointer does not refresh an extraction.
5. Ask concise questions for missing connections or decision-critical inputs, explaining which stage is affected. The user completes authentication, consent and MFA in provider settings; never request tokens/passwords/cookies in chat. Continue independent work.
6. Check Settings Active writer for another agent. Never seize a run on timeout; verify release before writing. Report each requested stage as Ready/Blocked with exact gaps and record one Harness check event when writes are possible. Then execute the requested stage; a full Run ends at Ready.

# Set up the seven-table instance

Use the user's intended accounts. Preserve existing values and references; a new-install blueprint is not authorization to delete live fields.

1. Resolve the private main Drive folder and create/reuse its two children: **Role specific** for role resumes/editable sources/change notes and **Audit trail** for job captures, assessments, reports and process metadata. Verify parent IDs and privacy, then register resume_output/content_output with folder_id and root_folder_id. Do not move existing goals/master/base documents unnecessarily.
2. Create or select the intended private Airtable base. Workspace creation/consent may require a human UI step. Discover actual schema capabilities; use contracts/core-schema.json as a logical blueprint, not a raw connector payload. Create the seven tables, scalar/computed fields and relationships with their reciprocal names. Application ID is formula RECORD_ID(); never write a formula result. Writers enforce business keys and link cardinality because display labels are not constraints.
3. Populate Settings from contracts/setup-seed.json with verified repository, structured_store, source/master/guideline/base references, output destinations, reader artifacts, role/company/execution/history policies, role_family and Stop all. Do not copy private defaults from another user. Missing optional resources are gaps only for dependent work. Register Settings.answer_bank with the two live answer-table IDs. Legacy mail/submission references and controls remain untouched and inactive; existing answer tables are reactivated without deleting data.
4. Extract Curate-company, Scan-criteria and Review-queue preferences from current Career Goals under CAREER-GOALS.md. Save source passages, units, exceptions, revision/hash and per-stage readiness. Blank is not unrestricted. Clarify only consequential gaps. Define Settings.role_family from the user's intended function (templates/role-family.example.json), and the discovery criteria, public catalogs/search sources and cadence in company_policy.discovery. No default role or funding minimum is shipped.
5. Add each official careers board (one URL per line, with region when relevant) to the company's Careers URLs for human-Allow companies. Missing configuration is a coverage gap. Newly discovered companies remain Proposed until the human chooses Allow/Exclude. Existing temporary application holds are not active research or preparation tasks; respect legacy permanent blocks without recreating retired fields.
6. Register the accurate editable master, private Approved resume guidelines using contracts/resume-guidelines-schema.json and templates/resume-guidelines.md, and the optional offline-created base library. Pin exact versions and each base's master version. Goals never supply resume facts. Missing guidelines/master or an inadequate starting point blocks affected preparation.
7. Register Settings.eval_registry with the existing private feedback catalog, receipt index, Review eval table and snapshots/report references. Never seed expected answers from predictions. Verify capture/retry and label-free replay under DATA.md before claiming eval readiness.
8. Configure a Review grid with Manual notes immediately after Lifecycle status and Feedback beside it and compact fields under DATA.md, plus an All fields maintenance view. If tools cannot manage views, save/report the exact UI action; do not claim it happened. Views are not a privacy boundary.
9. Verify Draft/Approved and Needs answer/Resolved fixtures, complete versus blocked form coverage, answer-change invalidation and duplicate-question recovery. Preserve live answer approvals and do not claim form coverage from table access. Verify authorized fictional create/read/update/archive fixtures, meaningful Audit log entries, Drive hash/readback, fresh-session recovery, interrupted-write reconciliation, stale-input checks and PDF inspection. Fixtures are not production scan coverage or Ready resumes. Record Passed, Blocked or Not tested per capability, with exact remaining work. Never claim account readiness from static tests or empty tables.

The base/journal cannot audit its own creation before it exists. Record that bootstrap boundary once the Audit log is available. Routine reads are not logged. No automatic data purge, schema deletion, permission changes or paid upgrade.

## Existing installations

Map and preserve live field IDs. Nine active tables and nine statuses define future writes; add the Needs answer, Apply manually and Applied Lifecycle options if the live field lacks them; add Settings submission_policy disabled (contracts/setup-seed.json) until the user enables it; extra historical tables, select options and submission fields may remain. Do not change live options or remap old outcomes to fit the smaller blueprint. WORKFLOW.md "Existing installations" defines protected rows and the one-time migration from Runs, Sources and History. docs/MAINTENANCE.md governs any separately authorized retirement.

# Connect a harness

A tool-capable harness such as Codex or Claude Code executes the instructions through its own integrations. Plain chat cannot do this. Vendor examples are not certified integrations; capabilities vary by plan and installation.

Use official connectors/tools/MCP with supported credential storage. Grant the intended private base/folders and the capabilities below. Read-only access cannot persist a completed live stage. Do not claim provider-enforced scope restrictions that the connector cannot enforce.

| Scope | Required capability |
|---|---|
| Instructions | Read repo/fork at a pinned revision |
| All live stages | Discover Airtable schema, paginate needed rows, write and verify state and Audit log entries |
| Content | Read registered Drive/Docs by exact ID; write/verify authorized output artifacts |
| Curate | Public company/funding research and repeatable feed readers; company/source state |
| Scan | Enumerate every configured official catalog page or validated equivalent |
| Review | Full exact JD, current goals/master/company evidence and evidence persistence |
| Prepare | Grounded editable resume/PDF production, every-page visual inspection, official application-question inspection, both answer tables and exact output/answer versions |
| Submit (optional) | Browser automation on official portals with the user's signed-in session or stored account, file upload, screenshots saved to Audit trail; Settings submission_policy.enabled |
| First-time setup | Folder/base/field/link management and safe seed/readback |

A model API key is not required. Data connectors may use APIs internally. Authentication/consent/MFA and unsupported UI actions require the human. Keep credentials out of chat, Git, issues and artifacts. Revoke connections through provider settings when no longer needed.

## Register a harness once

Save this in the harness's supported project instructions or reusable prompt, replacing placeholders privately:

> Use Nextmove from <my repository/fork URL>, with private state <my Airtable base URL>. Start each session at SETUP.md, then read AGENTS.md, WORKFLOW.md and the requested stage. Run means Curate → Scan → Review → Prepare and stops after Prepare marks each role Ready (verified resume plus approved/resolved required answers), Needs answer or Apply manually. Individual commands execute only their stage. Discover seven active tables and Settings; preserve legacy data. Validate the stage's source identities, access and writer release. Queued, including a human's choice, authorizes Prepare; fit gates apply before agent queue admission. Ask targeted questions for consequential gaps and continue independent work. Save and verify evidence and Audit log entries so another harness can recover without this chat. Inspect required application questions, answer Form questions from the master, role resume or Career Goals when grounded, save only remaining gaps as unapproved Answer bank rows and Narrative answers as Needs answer, and verify approval/resolution before Ready. Never invent resume facts or run later recruiting tasks. Fill and submit applications only on my explicit Submit command under stages/submit.md.

Before setup, bare commands cannot discover an unknown repo/base. No installed launcher or external scheduler is promised.

## Switching harnesses

Release the old writer before another starts. The next harness verifies its own connections and recovers each role's evidence from Airtable/Drive. Never pass private state only in a chat summary or copy browser cookies/secrets between providers. One agent can run the full sequence; manually initiated stages use the same evidence and acceptance checks.

When upgrading an old feedback inbox, add Feedback to Companies and Applications without renaming or clearing Manual notes. Preserve notes and existing receipt identities; migrate only known corrections. Repair legacy history formats before recovery testing; unsupported field-change maps are preserved but never treated as complete stage evidence. Register only source URLs actually opened; an accessible source is not proof that its catalog has been enumerated.
