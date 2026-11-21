# Nextmove

Nextmove is a set of instructions for tool-capable AI harnesses such as Codex and Claude Code. It maintains company/funding evidence, finds plausible roles in the function you target, reviews their fit and prepares truthful, verified resumes. The workflow ends at Ready; you handle applications and everything afterward.

One agent can run the whole sequence. You can also start each stage manually in a different harness. Both use the same saved state, evidence and safeguards. This repository is not a hosted app, scheduler or automatic launcher for other harnesses.

## The workflow

| Stage | Work | Result |
|---|---|---|
| [Curate](stages/curate.md) | Refresh company/funding evidence and propose matching companies new to your list that meet your preferences. | Current evidence; Proposed companies await your Allow/Exclude. |
| [Scan](stages/scan.md) | Enumerate every configured official board and region for allowed companies. Use broad role keywords and basic semantics. | Plausible candidates for your target roles become Inventoried. |
| [Review](stages/review.md) | Extract the JD, score career fit against Career Goals, then score resume fit against the master. | Total score routes Queued, Need review or Not pursuing, with explained ratings. |
| [Prepare](stages/prepare.md) | Reuse an approved base resume that fully covers the role, or tailor a role version from the closest base under your resume guidelines. Verify every claim against the master and inspect the rendered PDF. | Ready with an exact resume file/version. |

The six active statuses are **Inventoried, Need review, Queued, Ready, Not pursuing and Duplicate**. Ready means a verified resume is available at an exact link/version. [WORKFLOW.md](WORKFLOW.md#six-lifecycle-states) defines the lifecycle. Inventory and the preparation queue are states in the same Applications table. A manually selected status does not create review approval or verify a PDF.

Curate hands human-approved companies and factual company evidence to Scan/Review. Only human-Allow companies receive new inventory or automatic advancement; any legacy permanent block is respected. A standalone Scan or Review reads that saved handoff without launching company research. Draft boards become eligible only after human Allow and still need verification. Review assesses company facts against current goals rather than copying Curate’s saved advisory assessment; changed funding/business evidence revalidates affected approvals. A partial Curate does not stop independent scanning/review, but stays visible in full-Run completion.

## Architecture

~~~mermaid
flowchart LR
    User[Human preferences and company choices] --> Agent[One active AI harness]
    Git[GitHub instructions] --> Agent
    Agent <--> Airtable[Seven Airtable tables: saved state]
    Agent <--> Drive[Google Drive: content and evidence]
    Agent --> Boards[Official careers catalogs]
    Funding[Company and funding evidence] --> Agent
    Airtable --> Next[Same agent or manually chosen next harness]
    Drive --> Next
~~~

Git owns procedures. Drive owns Career Goals, the factual master, resume guidelines, base/role resumes, job captures and reports. Airtable owns company targeting, candidate state, source coverage, fixed inputs, checkpoints, feedback and history. Each harness uses its own authenticated connections; connections do not transfer between providers. No mailbox connection, application-site login or answer bank is required.

The private main Drive folder has two working children: **Role specific** for customized resumes and change notes, and **Audit trail** for captures, assessments, run reports and process metadata. Setup creates or reuses them and registers their IDs in Airtable. Source documents keep their verified locations; existing links remain valid.

| Airtable table | Responsibility | Minimal target columns |
|---|---|---:|
| Companies | Proposed/Allow/Exclude targeting, funding stage and company evidence | 11 |
| Applications | Job facts, review/resume state, Manual notes, Feedback and Agent notes | 26 |
| Sources | Official board/region, reviewed reader and pagination/coverage checkpoint | 13 |
| Runs | Frozen inputs, ownership, progress and handoff | 20 |
| Settings | Private references, versions, controls and verification | 6 |
| History | Meaningful field changes, decisions, events, failures and uncertainty | 13 |
| Review eval | Golden answer key from your graded notes, and each eval's prediction and match | 13 |

The 102-column new-install target includes required reciprocal relationships. [DATA.md](DATA.md) explains storage and recovery; [core-schema.json](contracts/core-schema.json) is the machine-readable blueprint.

Review scores and decisions are maintained only in [stages/review.md](stages/review.md). The code reads its tables and automatically records a fingerprint of the exact instructions used. Users do not synchronize a second scoring file or bump a Review version.


## Where to find each rule

There are 10 operational instruction files. Each concern has one owner; maintenance and public-project policies are separate.

| Question | Read |
|---|---|
| What should a harness load first? | [AGENTS.md](AGENTS.md) |
| Commands, lifecycle, ownership, clarifications and stage handoff? | [WORKFLOW.md](WORKFLOW.md) |
| Accounts, Drive folders, Airtable setup, connectors and saved harness prompt? | [SETUP.md](SETUP.md) |
| Fields, identity, compact values, notes, evidence, history and recovery? | [DATA.md](DATA.md) |
| How are end-user career preferences interpreted? | [CAREER-GOALS.md](CAREER-GOALS.md) |
| Scan criteria, pagination and recall-tested improvement? | [Scan](stages/scan.md) |
| Final role/seniority, compensation and fit decisions? | [Review](stages/review.md) |
| Resume production and verification? | [Prepare](stages/prepare.md), with [file/version rules](RESUME-FILES.md) and the [resume guidelines frame](templates/resume-guidelines.md) |
| Company list, funding evidence and discovery? | [Curate](stages/curate.md) |
| Retiring live columns and release checks? | [Maintenance](docs/MAINTENANCE.md) |

Agents read the entry point, workflow and requested stage, then relevant reference sections. They do not load the entire repository or bulk catalogs into model context. Standard public files such as SECURITY.md, CONTRIBUTING.md and LICENSE are not additional stage procedures.

## What you provide

- Your own Airtable and Google accounts, sufficient service capacity and the intended private destinations.
- Separate authenticated connections in every harness, plus official-page readers and PDF generation/visual inspection tools. You handle sign-in, consent and MFA; unsupported capabilities remain blockers.
- Your target role family in private Settings `role_family`: a name and title patterns ([example](templates/role-family.example.json)). Nextmove ships no default role or funding minimum; each user sets their own.
- [Career preferences](templates/career-goals.md), in ordinary prose or the optional template: desired function, designation, seniority/scope, compensation, domains, responsibilities, geography and priorities. This document contains preferences, not agent instructions.
- One accurate designated editable master resume, your private resume guidelines in the [standard frame](templates/resume-guidelines.md) (base themes, company grouping, length, layout, language), and optionally a library of approved base resumes you build offline. Goals are not evidence of experience.
- Explicit company choices: approve or decline Proposed companies (Allow/Exclude), and register the funding-news feeds Curate should read.
- Answers to decision-critical questions. Agents must ask when a missing answer changes the work.

No model API key is required. Connectors may use service APIs internally. A fork does not copy private data, authentication or another person's setup. Plain chat without suitable tools cannot execute these stages.

## Set up and run

Follow [SETUP.md](SETUP.md) once, including its saved harness prompt. Each new session, and each newly onboarded agent, starts with its connection check: the agent asks for any missing Airtable, Google or web connection, then reports which stages are ready. Then use `Run Nextmove` for the full authorized sequence or `Curate`, `Scan`, `Review` or `Prepare` for a single stage. Every Run stops after Prepare and hands you the verified resume links and change notes.

For manual switching, release the previous owner and open the next configured harness. It recovers from Airtable/Drive, not a chat summary. One agent writes at a time. Save and verify every handoff; continue independent work while reporting required gaps as Partial/Blocked.

## Expectations and limits

Expect thorough configured source coverage, recall-oriented candidate capture, explained review decisions, factual resumes, compact tracker values and recoverable verified progress. Do not expect guaranteed interviews/compensation, universal careers-site access, unattended authentication, automatic cross-provider orchestration, identical model judgment or unlimited free storage. Form filling, application answers/submissions, application-limit/cooldown management, mailbox monitoring and all later recruiting work are outside scope.

Career preferences, domain rules and personal exceptions belong in each user's private goals, so a friend can use the same public frame.

## Existing installations

The simplified schema is for new setup and active writes. Existing answer/question tables, submission columns, later statuses, old controls and historical files are preserved as inactive history. They are not automatically deleted or required by the four stages. Historical outcomes and unresolved legacy attempts are protected from automatic reopening. Valid Review/Prepare evidence remains usable when its actual inputs are unchanged; the Review scoring instructions are unchanged by this scope reduction. See [maintenance](docs/MAINTENANCE.md) before any separate physical cleanup.

## Contributing and license

Keep private data, account identifiers, resumes, job/mail snapshots and credentials out of public Git and issues. Read [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md). With Python 3.10+, run:

    python scripts/check_repo.py
    python scripts/build_schema.py
    python -m unittest discover -s tests -v

These validate public contracts/helpers, not live scan completion or account readiness. Licensed under [MIT](LICENSE); no access to private data is granted.

## Feedback that improves the workflow

Manual notes is permanent human context and is never automatically cleared. Feedback is the separate inbox for correcting an agent's output. On the next invocation, the coordinator captures Feedback with evidence and history, verifies it, then clears only that unchanged Feedback. Ambiguous feedback remains pending; previous evals/receipts remain preserved.

Use **Capture feedback** to consume the inbox, and **Review eval** (or **Eval Review**) to test frozen cases with a fresh reviewer. Reports distinguish blind performance from a comparison of existing statuses. Normal stage runs capture feedback and propose tested improvements; they do not run unattended between invocations. DATA.md "Feedback inbox and Review eval" defines the shared process, including duplicate handling, holdout protection and rule-change review. No new table or per-stage instruction file is required.

Source files remain in Drive. Settings registers their identity, authority and current revision/hash; DATA.md "Registered sources and small artifact reads" defines freshness checks and exact-ID evidence selection. Use scripts/artifact_reader.py for stored job/company/coverage artifacts, and the dedicated Review eval workflow for label-free eval inputs. No extra preference/fact table is required.

For manually submitted application answers, the existing Application questions table can be used as an optional human-maintained interview reference. Record the linked application, exact question, exact Final answer and Answered on date. It is not a pipeline dependency.
