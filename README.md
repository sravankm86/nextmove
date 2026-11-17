# Nextmove

Nextmove is a set of instructions for tool-capable AI harnesses such as Codex and Claude Code. It keeps your target-company list current (funding discovery, employer application limits and rejection cooldowns), finds plausible roles in the function you target, reviews their fit, prepares truthful resumes, supports authorized applications and tracks recruiting progress through the interview stage.

One agent can run the whole sequence. You can also start each stage manually in a different harness. Both use the same saved state, evidence and safeguards. This repository is not a hosted app, scheduler or automatic launcher for other harnesses.

## The workflow

| Stage | Work | Result |
|---|---|---|
| [Curate](stages/curate.md) | Recompute company application holds, research employer limits and cooldowns, and propose newly funded companies that meet your Career Goals funding minimum. | Current holds; Proposed companies await your Allow/Exclude. |
| [Scan](stages/scan.md) | Enumerate every configured official board and region for allowed companies. Use broad role keywords and basic semantics. | Plausible candidates for your target roles become Inventoried. |
| [Review](stages/review.md) | Extract the JD, score career fit against Career Goals, then score resume fit against the master. | Total score routes Queued, Need review or Not pursuing, with explained ratings. |
| [Prepare](stages/prepare.md) | Reuse an approved base resume that fully covers the role, or tailor a role version from the closest base under your resume guidelines. Verify every claim against the master and inspect the rendered PDF. | Ready with an exact resume file/version. |
| [Apply](stages/apply.md) | A browser agent opens the real form, fills it from your answer bank and uploads the exact verified resume, within your on/off switch and daily limit. | Applied with confirmation; anything unclear stops that role. Default is preflight. |
| [Track](stages/track.md) | Read exact-role recruiting messages and reconcile receipts/engagement. | Confirmation evidence under Applied; active engagement reaches Interviewing. |

The ten statuses are **Inventoried, Need review, Queued, Ready, Needs answer, Applied, Interviewing, Not pursuing, Rejected and Duplicate**. The successful path ends at Interviewing, including recruiter screening, assessments and interviews. Offers, negotiation, acceptance and later recruiting outcomes are outside automatic tracking scope. See [the lifecycle rules](WORKFLOW.md#ten-lifecycle-states). Needs answer means Apply is waiting for you to answer an application question in your answer bank.

Inventory and the preparation queue are states in the same Applications table. Reasons, confirmation, missing evidence and uncertain attempts are recorded as evidence; only a missing application answer gets its own status (Needs answer). A manually selected status does not create review approval, verify a PDF or authorize submission.

Curate hands human-approved companies and factual company evidence to Scan/Review. Temporary application holds do not reduce inventory or fit; permanent blocks stop new inventory and automatic advancement. A standalone Scan or Review reads that saved handoff without launching company research. Draft boards become eligible only after human Allow and still need verification. Review assesses company facts against current goals rather than copying Curate’s saved advisory assessment; changed funding/business evidence revalidates affected approvals. A partial Curate does not stop independent scanning/review, but stays visible in full-Run completion.

## Architecture

~~~mermaid
flowchart LR
    User[Human preferences and authorization] --> Agent[One active AI harness]
    Git[GitHub instructions] --> Agent
    Agent <--> Airtable[Seven Airtable tables: saved state]
    Agent <--> Drive[Google Drive: content and evidence]
    Agent --> Boards[Official catalogs and application sites]
    Funding[Funding news and employer policy pages] --> Agent
    Mail[Read-only recruiting mailbox] --> Agent
    Airtable --> Next[Same agent or manually chosen next harness]
    Drive --> Next
~~~

Git owns all procedures. Drive owns Career Goals, the factual master, resumes, job captures and reports. Airtable owns targeting, candidate/application state, source progress, fixed inputs, checkpoints and history. The active harness executes through its own authenticated connections; connections do not transfer between providers.

The private main Drive folder has two working children: **Role specific** for customized resumes and application materials, and **Audit trail** for captures, assessments, run reports and process metadata. Setup creates or reuses them and registers their IDs in Airtable. Source documents keep their verified locations; existing links remain valid.

| Airtable table | Responsibility | Minimal target columns |
|---|---|---:|
| Companies | Proposed/Allow/Exclude targeting, funding stage, company evidence, employer policies and holds | 21 |
| Applications | Job facts, review/resume/application state, Manual notes and Agent notes | 29 |
| Sources | Official board/region, reviewed reader and pagination/coverage checkpoint | 13 |
| Runs | Frozen inputs, ownership, progress and handoff | 21 |
| Settings | Private references, versions, controls and verification | 6 |
| History | Meaningful field changes, decisions, events, failures and uncertainty | 13 |
| Review eval | Golden answer key from your graded notes, and each eval's prediction and match | 13 |

The 116-column target includes required reciprocal relationships. [DATA.md](DATA.md) explains storage and recovery; [core-schema.json](contracts/core-schema.json) is the machine-readable blueprint.

Review scores and decisions are maintained only in [stages/review.md](stages/review.md). The code reads its tables and automatically records a fingerprint of the exact instructions used. Users do not synchronize a second scoring file or bump a Review version.


## Where to find each rule

There are 12 operational instruction files. Each concern has one owner; maintenance and public-project policies are separate.

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
| Company list, funding discovery, employer quotas/cooldowns and holds? | [Curate](stages/curate.md) |
| Submission safeguards and the final pre-submit hold check? | [Apply](stages/apply.md) |
| Receipts, recruiter engagement and mailbox checkpoints? | [Track](stages/track.md) |
| Retiring live columns and release checks? | [Maintenance](docs/MAINTENANCE.md) |

Agents read the entry point, workflow and requested stage, then relevant reference sections. They do not load the entire repository or bulk catalogs into model context. Standard public files such as SECURITY.md, CONTRIBUTING.md and LICENSE are not additional stage procedures.

## What you provide

- Your own Airtable and Google accounts, sufficient service capacity and the intended private destinations.
- Separate authenticated connections in every harness, plus any browser or mailbox tools that its stages require. You handle sign-in, consent and MFA; unsupported capabilities remain blockers.
- Your target role family in private Settings `role_family`: a name and title patterns ([example](templates/role-family.example.json)). Nextmove ships no default role, funding minimum or application limit; each user sets their own.
- [Career preferences](templates/career-goals.md), in ordinary prose or the optional template: desired function, designation, seniority/scope, compensation, domains, responsibilities, geography and priorities. This document contains preferences, not agent instructions.
- One accurate designated editable master resume, your private resume guidelines in the [standard frame](templates/resume-guidelines.md) (base themes, company grouping, length, layout, language), and optionally a library of approved base resumes you build offline. Goals are not evidence of experience.
- Explicit company choices: approve or decline Curate's Proposed companies (Allow/Exclude), confirm any permanent block, and share known application limits or recruiter-stated cooldowns. Register the funding-news feeds Curate should read. A default personal limit of 3 applications per company in any rolling 30 days applies unless your Career Goals set another.
- Answers to decision-critical questions. Agents must ask when a missing answer changes the work.
- A [daily submission limit and the Pause applications switch](stages/apply.md#guard-rails-you-control) and an answer bank Google Doc in your Drive ([blank template](templates/answer-bank.md)) before real applications, plus a browser-capable agent signed into the sites you allow. Track needs read-only mailbox access.

No model API key is required. Connectors may use service APIs internally. A fork does not copy private data, authentication or another person's setup. Plain chat without suitable tools cannot execute these stages.

## Set up and run

Follow [SETUP.md](SETUP.md) once, including its saved harness prompt. Then use `Run Nextmove` for the full authorized sequence or `Curate`, `Scan`, `Review`, `Prepare`, `Apply`, `Track` for a single stage. Fresh setup leaves submissions paused; a Run or bare Apply command does not authorize submissions.

For manual switching, release the previous owner and open the next configured harness. It recovers from Airtable/Drive, not a chat summary. One agent writes at a time. Save and verify every handoff; continue independent work while reporting required gaps as Partial/Blocked.

## Expectations and limits

Expect thorough configured source coverage, recall-oriented candidate capture, explained review decisions, factual resumes, compact tracker values and recoverable verified progress. Do not expect guaranteed interviews/compensation, universal careers-site access, unattended authentication, automatic cross-provider orchestration, identical model judgment or unlimited free storage. Availability monitoring and post-interview outcome tracking are outside scope.

Career preferences, domain rules and personal exceptions belong in each user's private goals, so a friend can use the same public frame.

## Contributing and license

Keep private data, account identifiers, resumes, job/mail snapshots and credentials out of public Git and issues. Read [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md). With Python 3.10+, run:

    python scripts/check_repo.py
    python scripts/build_schema.py
    python -m unittest discover -s tests -v

These validate public contracts/helpers, not live scan completion or account readiness. Licensed under [MIT](LICENSE); no access to private data is granted.

## Feedback that improves the workflow

Manual notes is an inbox. Write what the agent should have done and why; partial feedback is useful too. On the next invocation the coordinator saves it as an eval case with evidence and audit history, verifies the capture, then clears the unchanged note. Your feedback survives in Review eval/Drive even after the inbox is empty. Unclear feedback stays pending instead of becoming a guessed answer key.

Use **Capture feedback** to consume the inbox, and **Review eval** (or **Eval Review**) to test frozen cases with a fresh reviewer. Reports distinguish blind performance from a comparison of existing statuses. Normal stage runs capture feedback and propose tested improvements; they do not run unattended between invocations. DATA.md "Feedback inbox and Review eval" defines the shared process, including duplicate handling, holdout protection and rule-change review. No new table or per-stage instruction file is required.
