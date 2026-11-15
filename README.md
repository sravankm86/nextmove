# Nextmove

Nextmove is a set of instructions for tool-capable AI harnesses such as Codex and Claude Code. It finds plausible senior product-management roles, reviews their fit, prepares truthful resumes, supports authorized applications and tracks recruiting progress through the interview stage.

One agent can run the whole sequence. You can also start each stage manually in a different harness. Both use the same saved state, evidence and safeguards. This repository is not a hosted app, scheduler or automatic launcher for other harnesses.

## The workflow

| Stage | Work | Result |
|---|---|---|
| [Scan](stages/scan.md) | Enumerate every configured official board and region for allowed companies. Use broad role keywords and basic semantics. | Plausible PM candidates become Inventoried. |
| [Review](stages/review.md) | Read the full JD and assess role/seniority, hard career requirements and independent career/resume fit. | Approved candidates become Queued; others remain pending or become Not pursuing, with reasons. |
| [Prepare](stages/prepare.md) | Reuse or tailor from the factual master, record grounded changes and verify the rendered PDF. | Ready with an exact resume file/version. |
| [Apply](stages/apply.md) | Check authorization, answers, real form access, exact resume and company restrictions. | Applied after an established submission; uncertainty blocks retries. Default is preflight. |
| [Track](stages/track.md) | Read exact-role recruiting messages and reconcile receipts/engagement. | Confirmation evidence under Applied; active engagement reaches Interviewing. |

The seven statuses are **Inventoried, Queued, Ready, Applied, Interviewing, Not pursuing and Rejected**. The successful path ends at Interviewing, including recruiter screening, assessments and interviews. Offers, negotiation, acceptance and later recruiting outcomes are outside automatic tracking scope. See [the lifecycle rules](WORKFLOW.md#seven-lifecycle-states).

Inventory and the preparation queue are states in the same Applications table. Reasons, confirmation, missing evidence and uncertain attempts do not need separate lifecycle states. A manually selected status does not create review approval, verify a PDF or authorize submission.

## Architecture

~~~mermaid
flowchart LR
    User[Human preferences and authorization] --> Agent[One active AI harness]
    Git[GitHub instructions] --> Agent
    Agent <--> Airtable[Six Airtable tables: saved state]
    Agent <--> Drive[Google Drive: content and evidence]
    Agent --> Boards[Official catalogs and application sites]
    Mail[Read-only recruiting mailbox] --> Agent
    Airtable --> Next[Same agent or manually chosen next harness]
    Drive --> Next
~~~

Git owns all procedures. Drive owns Career Goals, the factual master, resumes, job captures and reports. Airtable owns targeting, candidate/application state, source progress, fixed inputs, checkpoints and history. The active harness executes through its own authenticated connections; connections do not transfer between providers.

| Airtable table | Responsibility | Minimal target columns |
|---|---|---:|
| Companies | Allow/Exclude choices and confirmed application restrictions | 15 |
| Applications | Job facts, review/resume/application state, Manual notes and Agent notes | 28 |
| Sources | Official board/region, reviewed reader and pagination/coverage checkpoint | 13 |
| Runs | Frozen inputs, ownership, progress and handoff | 20 |
| Settings | Private references, versions, controls and verification | 6 |
| History | Meaningful field changes, decisions, events, failures and uncertainty | 13 |

The 95-column target includes required reciprocal relationships. An older live base may need verified migration before fields can retire. No common metadata bundle is added to every table. [DATA.md](DATA.md) explains storage/recovery; [core-schema.json](contracts/core-schema.json) is the machine-readable blueprint.

## Where to find each rule

There are 11 operational instruction files. Each concern has one owner; maintenance and public-project policies are separate.

| Question | Read |
|---|---|
| What should a harness load first? | [AGENTS.md](AGENTS.md) |
| Commands, lifecycle, ownership, clarifications and stage handoff? | [WORKFLOW.md](WORKFLOW.md) |
| Accounts, Drive folders, Airtable setup, connectors and saved harness prompt? | [SETUP.md](SETUP.md) |
| Fields, identity, compact values, notes, evidence, history and recovery? | [DATA.md](DATA.md) |
| How are end-user career preferences interpreted? | [CAREER-GOALS.md](CAREER-GOALS.md) |
| Scan criteria, pagination and recall-tested improvement? | [Scan](stages/scan.md) |
| Final role/seniority, compensation and fit decisions? | [Review](stages/review.md) |
| Resume production and verification? | [Prepare](stages/prepare.md), with [file/version rules](RESUME-FILES.md) |
| Company quotas, cooldowns and submission safeguards? | [Apply](stages/apply.md) |
| Receipts, recruiter engagement and mailbox checkpoints? | [Track](stages/track.md) |
| Deliberate field retirement, deployment and release checks? | [Maintenance](docs/MAINTENANCE.md) |

Agents read the entry point, workflow and requested stage, then relevant reference sections. They do not load the entire repository or bulk catalogs into model context. Standard public files such as SECURITY.md, CONTRIBUTING.md and LICENSE are not additional stage procedures.

## What you provide

- Your own Airtable and Google accounts, sufficient service capacity and the intended private destinations.
- Separate authenticated connections in every harness, plus any browser or mailbox tools that its stages require. You handle sign-in, consent and MFA; unsupported capabilities remain blockers.
- [Career preferences](templates/career-goals.md), in ordinary prose or the optional template: desired function, designation, seniority/scope, compensation, domains, responsibilities, geography and priorities. This document contains preferences, not agent instructions.
- One accurate designated editable master resume; an approved base PDF is optional. Goals are not evidence of experience.
- Explicit company choices, known application restrictions and answers to decision-critical questions. Agents must ask when a missing answer changes the work.
- Explicit submission scope and approved answers before real applications. Track needs read-only mailbox access.

No model API key is required. Connectors may use service APIs internally. A fork does not copy private data, authentication or another person's setup. Plain chat without suitable tools cannot execute these stages.

## Set up and run

Follow [SETUP.md](SETUP.md) once, including its saved harness prompt. Then use `Run Nextmove` for the full authorized sequence or `Scan`, `Review`, `Prepare`, `Apply`, `Track` for a single stage. Fresh setup leaves submissions paused; a Run or bare Apply command does not authorize submissions.

For manual switching, release the previous owner and open the next configured harness. It recovers from Airtable/Drive, not a chat summary. One agent writes at a time. Save and verify every handoff; continue independent work while reporting required gaps as Partial/Blocked. Do not run production work through an unresolved migration pause.

## Expectations and limits

Expect thorough configured source coverage, recall-oriented candidate capture, explained review decisions, factual resumes, compact tracker values and recoverable verified progress. Do not expect guaranteed interviews/compensation, universal careers-site access, unattended authentication, automatic cross-provider orchestration, identical model judgment or unlimited free storage. Availability monitoring and post-interview outcome tracking are outside scope.

Airtable display fields are not SQL uniqueness constraints, ownership labels are not locks, and editable logs do not provide immutable all-access auditing. History records meaningful changes/events and run-level read scope rather than a row for every read. Direct human/API edits may bypass the agent journal. Missing evidence, tool limits and uncertain writes must remain visible; no hidden page caps, invented completion or automatic paid upgrades.

## Contributing and license

Keep private data, account identifiers, resumes, job/mail snapshots and credentials out of public Git and issues. Read [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md). With Python 3.10+, run:

    python scripts/check_repo.py
    python scripts/build_schema.py
    python -m unittest discover -s tests -v

These validate public contracts/helpers, not live scan completion or account readiness. Licensed under [MIT](LICENSE); no access to private data is granted.
