# Portable stage commands

Read AGENTS.md, DATA-GOVERNANCE.md, STORAGE.md and WORKFLOW.md. The user chooses one active harness. Use it for one stage, or explicitly request a recorded ordered plan in that harness under ARCHITECTURE.md. A human may instead switch harnesses between stages. No scheduler, model API or cross-harness launcher is required. See [HARNESS-BOOTSTRAP.md](HARNESS-BOOTSTRAP.md) for one-time registration in each harness. Machine-readable routing is in [contracts/commands.json](contracts/commands.json).

## Command meaning

Only dispatch when the user actually requests a stage. Quoted examples, setup discussions or mentions of a command are not stage execution requests.

| Command | Stage and default scope | Persistence |
|---|---|---|
| Scan | Every current Allow company and its official sources, including regional boards | Prepare mode: inventory, Queued matches, metadata and coverage audit |
| Review (Assess / Role fit / Shortlist) | All Queued and explicitly retryable review-owned pre-submission records | Prepare mode: independent career/resume fit and evidence-backed decisions |
| Prepare (Resume preparation) | All eligible Shortlisted with current review inputs | Prepare mode: master-grounded resume, changes, verified PDF/version and Ready |
| Apply | Ready queue, constrained by live controls and separate authorization | Default review/preflight; submit only under a valid explicit private authorization |
| Track | Configured read-only recruiting mailbox and saved coverage checkpoint | Prepare mode: exact-role updates, events and mail audit |

An explicitly requested single-harness plan records stage order, scope, current pointer and stop conditions privately under ARCHITECTURE.md. Each stage uses the same queue, audit, acceptance and handoff rules. Do not advance on Partial/Blocked unless the plan explicitly permits unaffected work, and never infer submission authorization. A bare command still stops after one stage.

A registered non-submission command is a request to execute and save that stage, not merely describe a plan. Do not ask the user to repeat known criteria, role IDs or links stored in the registry. Default scope is the whole eligible queue, not just the latest scan, first page or convenient batch. An explicit scope in the current request takes precedence and must be saved. Bare Apply does not create a standing authorization, unpause applications, choose answers or waive eligibility.

## Recover context in a fresh session

1. Locate the repository and the user's exact existing base from the saved bootstrap. Discover live tables, field IDs, types and controls. The minimal schema discovery needed to locate Audit Events is the documented nonrecursive bootstrap boundary; log it as soon as the endpoint is available. Do not use that exception for unlogged business data reads.
2. Use DATA-GOVERNANCE.md for controlled reads and mutations, including intents/outcomes and verification reads. No unattended gateway is assumed. A manual harness may perform a bounded audited sequence directly with its authenticated tools if it can honor the protocol. Keep universal audit coverage marked Partial; manual orchestration does not make UI/API access globally audited.
3. Read Stage Config, Context Registry, Controls and relevant Stage Runs under audit. Load only required content, using the registered Drive references. Verify actual access and current input versions/content hashes at execution time. Located metadata is not proof that content was read or approved.
4. Resolve broad career criteria from the current goals document and company-specific choices, including Notes. Do not carry old spreadsheet row-number overrides or stale local criteria forward. The latest designated editable master is the sole resume-fact source; prior tailored PDFs are artifacts, not authority.
5. Check the stage's actual capabilities: complete official catalog access and durable reader/state handling for Scan; full JD/master access for Review; honest document/PDF production and visual checks for Prepare; an authorized supported application browser for Apply; read-only mailbox access for Track. Never assume another harness's connectors, filesystem, sessions or tools are available here.
6. If a required resource is absent/inaccessible, record the exact blocker in Airtable when audit/write access permits. If Airtable itself is inaccessible, return a clearly unpersisted blocker; do not claim a saved checkpoint. Do not create a replacement base, invent resume facts or export private inputs into Git.

## Recover or establish the run

Resume exactly one compatible unfinished Stage Run of the requested stage when its prior owner has released it and input/instruction versions remain valid. Record a new Task Attempt for the new harness; preserve old attempts. Never silently combine ambiguous runs or reuse another stage's attempt.

Running ownership is advisory, not a database lock. With manual sequencing, the operator runs only one active harness. An expired lease alone does not prove the old harness stopped; require evidence or operator resolution before takeover. Claim and read back owner/run/attempt before business mutations, heartbeat at safe checkpoints and release ownership on exit. No competing dispatcher is installed.

When there is no compatible unfinished run, create a new run with its unique key, command, scope, instruction commit and actual input versions. An explicit New Scan/New Review/etc. creates a fresh invocation, but must not abandon or conceal active work. A completed prior run is not resumed as if new work was already done.

Snapshot all eligible work into Work Items before consuming the queue. Use a stable key from run identity, entity/source identity and input versions, not role title. Paginate the full queue and deduplicate stable identities. Persist expected item count and expected current application state. Scan plans include every company and known source, even if source configuration is missing; add newly discovered boards with an audited scope change. For Track, save mailbox/window/cursor scope. Empty eligible scope is No work, not an invented successful scan or mailbox reconciliation.

Pin one immutable instruction revision per attempt. If the repository changes during execution, do not silently mix revisions. If goals, JD, master, controls or human choices change, invalidate only affected work, save the reason and follow the stage contract. Never reuse stale positive assessment or readiness evidence.

## Execute the whole stage

Process bounded batches, keeping bulk I/O, filtering, hashing and verification in code and compact summaries in model context. Save queue membership, attempts, versions, completed items, pending items, errors, counts and cursors in Airtable at each safe checkpoint. Local files may accelerate work but cannot be the only state.

Persist content in the configured Drive locations and record its exact reference, version/hash, provenance and verification in Artifacts and the applicable application. Keep full descriptions accessible through Drive references; an employer URL or summary alone is not captured content. Reusable readers must be available in versioned Git or an authorized Drive artifact; a vanished local script is a setup gap requiring baseline/recovery, not proof of incremental support.

Work Items normally link to one Stage Run and one canonical application/company/source where applicable. Task Attempts link to their run and optionally bounded item; Artifacts link to their producer and applicable application. Validate linked targets and cardinality in the single writer. Do not infer SQL constraints from the link fields.

On a crash, reconcile persisted outputs before retrying, including cases where the business write succeeded but its work-item checkpoint did not. Audit keys and work keys are idempotent; an attempted operation is not proof of a committed result. Reusing an artifact requires matching actual input versions and accepted verification.

For Apply, create a distinct submission attempt before a supported authorized submission, record the submitted resume version and exact-role result, and reconcile uncertainty before any retry. Pause, cooldowns, unresolved answers, missing authorization and unsupported sites remain gates. No missing email means no submission proof. Never blind-retry a form to finish a queue.

Continue through all batches of the authorized scope until verified completion or a real stop, budget, capability/access failure or unresolved blocker. A completed batch is not a completed stage. Do not introduce hidden page/item/time limits to save tokens.

## Verify and leave the handoff

Read back actual changed state and artifacts as required by the stage. Persist acceptance checks for every item. A successful harness message is not acceptance.

Stage status and Application lifecycle are separate. A valid completed fit decision can be Not a fit or a borderline Needs review. Missing required evidence or unfinished processing remains blocked/partial. Do not turn an execution failure into a rejection or reset an application because a task retried.

Use these execution states consistently:
- Pending: planned and not started.
- Running: currently owned, with heartbeat and attempt.
- Complete: all planned processing, required evidence, audit and readback have passed.
- Partial: some usable verified output exists and work/gaps remain.
- Blocked: required access, evidence, authorization or operator resolution is unavailable.
- Failed: execution failed without usable completion; preserve cause and checkpoint.
- Interrupted: execution stopped with resumable progress.
- Cancelled: explicitly stopped by the user.
- No work: verified empty eligible queue for this invocation.

Set the final run state from persisted item outcomes. Complete requires every planned item accounted for, expected/completed counts reconciled and no unresolved processing gap. Scan also obeys source/company Complete/Partial/Failed definitions and reports description/metadata gaps separately. Do not hide omitted rows in a handoff count.

Save Handoff (JSON) with run/attempt IDs, stage, instruction/input versions, scope/counts, exact outputs and artifact references, verified decisions, remaining work, blockers, next owner/command and ownership release. Include no secrets or large content bodies. Preserve the source/run/evidence relationships. The next harness reads state directly; the user need not paste this report.

Finish with a short human-readable result and next command. Stop after a single-stage request. Recording Next command does not launch it. Only an explicit recorded multi-stage plan may advance to its next authorized stage after acceptance and live-control checks; log that boundary before continuing.

## State and readiness boundaries

Context Registry is the private resource directory; Stage Config defines command defaults; Stage Runs records invocation/scope/ownership; Work Items freezes membership and progress; Task Attempts records executions; Artifacts records content references and verification. Existing Runs/Scan Audit, Mail Audit, Lifecycle Events and Audit Events retain their domain/audit roles. Private physical IDs and input content never belong in public Git.

Schema setup and populated resource references establish a portable contract, not an end-to-end tested integration in Codex, Gemini, Claude, Muse or any other harness. Required resource/capability checks occur per harness and stage. Missing answer-bank/submission policy or mailbox access can block Apply/Track while Scan remains usable. Preserve all live audit and submission controls.

