# Nextmove

Nextmove is an instruction-led workflow for tool-capable AI harnesses such as Codex and Claude Code. It discovers relevant companies, finds roles, reviews their fit and prepares a truthful resume plus the required application answers. It ends at **Ready**; you fill and submit the application and handle recruiting afterward.

One agent can run the sequence, or you can start individual stages in different harnesses. Both use the same saved state and acceptance checks. This repository is not a hosted app, scheduler or launcher for other harnesses.

## The workflow

| Stage | Work and result |
|---|---|
| [Curate](stages/curate.md) | Research company/funding facts and propose companies new to your list. You choose Allow or Exclude; agents never auto-Allow. |
| [Scan](stages/scan.md) | Enumerate every configured official board and region for allowed companies. Broad role keywords and basic semantic checks produce Inventoried roles, protecting recall. |
| [Review](stages/review.md) | Compare the exact job description with Career Goals and the master resume. Current scores route to Queued, Need review or Not pursuing. |
| [Prepare](stages/prepare.md) | Reuse a suitable approved base or tailor from it, verify the PDF, inspect application questions and capture missing answers for your approval. |

**Ready requires all three:** a verified resume at an exact link/version, complete current application-question inspection, and a nonempty Approved or Resolved answer for every required question. A resume alone, a draft answer or a manual status change is not acceptance evidence. Incomplete preparation stays Queued with the blocker explained.

The six active states are Inventoried, Need review, Queued, Ready, Not pursuing and Duplicate. [WORKFLOW.md](WORKFLOW.md#six-lifecycle-states) owns their meaning. Each stage can run independently from its saved handoff; it does not silently launch earlier stages. A blocked item does not prevent independent work, but remains visible in completion reports.

## Architecture and storage

~~~mermaid
flowchart LR
    User[Preferences, company choices and answer approvals] --> Agent[One active AI harness]
    Git[GitHub: procedures] --> Agent
    Agent <--> Airtable[Airtable: state and references]
    Agent <--> Drive[Google Drive: content and evidence]
    Agent --> Web[Official catalogs, company evidence and application questions]
    Airtable --> Next[Same agent or next manually chosen harness]
    Drive --> Next
~~~

- **GitHub** holds portable procedures, contracts, helpers and tests. Personal preferences and credentials do not belong here.
- **Google Drive** holds Career Goals, the factual master resume, resume guidelines, approved bases, role resumes, captures and reports. Setup creates or reuses **Role specific** and **Audit trail** under your private main folder.
- **Airtable** holds nine tables: Companies, Applications, Sources, Runs, Settings, History, Review eval, Answer bank and Application questions. [DATA.md](DATA.md) defines their purposes and recovery; [core-schema.json](contracts/core-schema.json) defines the active fields and relationships.

Answer bank holds reusable Form answers. Application questions holds role-specific Narrative drafts and final answers, including exact submitted answers you may later record for interview reference. Agents draft and match; you approve or resolve. Preparation never claims a submission occurred.

Each harness uses its own authenticated connections. Airtable/Drive checkpoints, source identities and verified artifacts let the next harness recover without this chat or the previous computer's files. Only one agent writes at a time. Historical outcomes and uncertain prior submissions remain protected.

## What you provide

- Your own Airtable and Google accounts, private destinations and sufficient service capacity.
- A tool-capable harness with repository access, Airtable/Drive integrations, official-page readers, application-question inspection and PDF generation/visual inspection. You handle authentication, consent and MFA; access may differ across harnesses.
- [Career preferences](templates/career-goals.md): desired function, seniority, compensation, work, geography and company preferences. Free-form prose is supported. The harness derives private criteria under [CAREER-GOALS.md](CAREER-GOALS.md); no personal role or funding minimum is built in.
- An accurate editable master, private approved [resume guidelines](templates/resume-guidelines.md), and optionally approved base resumes created offline. The master is the sole resume-fact source.
- Company Allow/Exclude choices, answers to consequential clarification questions, and approvals for application answers.

No model API key is required; connectors may use service APIs internally. A fork copies no private data, credentials or account setup. Plain chat without suitable tools cannot execute the workflow.

## Set up and run

Follow [SETUP.md](SETUP.md) once, including its saved harness prompt. A new session starts at [AGENTS.md](AGENTS.md), verifies its own connections and reports any blocked stages. Then use **Run Nextmove** for Curate → Scan → Review → Prepare, or **Curate**, **Scan**, **Review** or **Prepare** for one stage.

To switch harnesses, release the previous writer and open the next configured harness. It reads saved state and current source versions, preserves human edits and asks for missing information. You do not need to orchestrate with APIs.

Manual notes is permanent context. Feedback is the separate correction inbox: **Capture feedback** saves and verifies eval evidence before clearing only the unchanged captured Feedback. **Review eval** tests frozen cases with a fresh blind reviewer; it does not change production applications. [DATA.md](DATA.md#feedback-inbox-and-review-eval) owns that process.

Use **Sanitize Nextmove** only for an explicitly requested repository-wide consistency and simplification pass. [Maintenance](docs/MAINTENANCE.md#sanitize-explicit-only) covers every file and field. It never runs with the pipeline, setup, retries or schedules.

## Where instructions live

| Concern | Owner |
|---|---|
| Entry and global boundaries | [AGENTS.md](AGENTS.md) |
| Commands, lifecycle, ownership and handoff | [WORKFLOW.md](WORKFLOW.md) |
| Accounts, connectors, folders and first-time setup | [SETUP.md](SETUP.md) |
| Fields, notes, source freshness, evidence, feedback and recovery | [DATA.md](DATA.md) |
| Preference interpretation | [CAREER-GOALS.md](CAREER-GOALS.md) |
| Stage behavior | [Curate](stages/curate.md), [Scan](stages/scan.md), [Review](stages/review.md), [Prepare](stages/prepare.md) |
| Resume naming, placement and versions | [RESUME-FILES.md](RESUME-FILES.md) |
| Explicit sanitization and live field retirement | [Maintenance](docs/MAINTENANCE.md) |

Agents load the requested stage and relevant reference sections, not the whole repository or raw catalogs. Review scores and routing have one owner: the Review file; code reads and fingerprints it rather than keeping a second scoring configuration.

## Expectations and limits

Expect thorough configured coverage, explained decisions, grounded resumes, approval-aware answers and recoverable progress. Do not expect guaranteed interviews or pay, universal careers-site access, unattended authentication, automatic cross-provider orchestration, identical model judgments or unlimited free storage. A hidden form step, missing earlier resume or unanswered question can require your help.

External form filling, submission, mailbox monitoring, application-limit/cooldown management and later recruiting work are outside scope. Existing historical fields/files are preserved; the active schema does not authorize automatic deletion. [Maintenance](docs/MAINTENANCE.md#retiring-live-columns-or-choices) governs any live retirement.

## Contributing and license

Keep private data, real account identifiers, resumes, snapshots and credentials out of Git and issues. Read [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md). With Python 3.10+, run:

    python scripts/check_repo.py
    python scripts/build_schema.py
    python -m unittest discover -s tests -v

Checks validate public contracts and logical helpers, not a live scan, rendered resume or account readiness. The project uses the [MIT license](LICENSE); it grants no access to private data.
