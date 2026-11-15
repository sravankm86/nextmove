# Nextmove

Nextmove helps you find suitable senior product-management roles, assess them, prepare truthful resumes, apply within your instructions and track recruiting updates. It runs through connected AI tools such as Codex or Claude Code. It is a set of instructions and validation tools, not a hosted application or an automatic job scheduler.

## How it works

One capable agent can run the entire workflow. You can also run one stage at a time in different tools. Both approaches use the same saved state and checks.

| Stage | Work | Result |
|---|---|---|
| [Scan](stages/scan.md) | Read every configured official board and region for allowed companies. Derive broad role criteria from Career Goals and use keywords/basic contextual checks. | Plausible candidates become Inventoried; uncertainty is preserved for Review. |
| [Review](stages/review.md) | Read the full job description. Check seniority/scope, career preferences, compensation and resume fit. | Approved roles become Queued for preparation. Others get a clear reason or Needs review. |
| [Prepare](stages/prepare.md) | Reuse or tailor a resume using only the editable master for facts. Verify the finished PDF and record changes. | Ready, with an exact resume file and version. |
| [Apply](stages/apply.md) | Check authorization, answers, availability, resume version and company limits. | Applied, Confirmed or Submission uncertain. Default is checks only. |
| [Track](stages/track.md) | Read recruiting messages and match them to exact roles. | Confirmation, recruiter engagement and later outcomes recorded. |

Inventoried and Queued are states in the same Applications table, not duplicate rows in two trackers. Queued means Review approved the role. Shortlisted is a legacy value, not a new stage. Missing salary or unclear seniority does not silently remove a plausible candidate during Scan. Review resolves the required evidence before approval.

## Where information lives

| Location | Responsibility |
|---|---|
| GitHub | All workflow instructions, decision rules, setup guidance, templates and validation helpers. |
| Google Drive | Your Career Goals, factual master resume, base/tailored resumes, job descriptions and reports. |
| Airtable | Companies, Applications, Sources, Runs, Settings and History: choices, job state, source progress, saved run progress, private references and change history. |
| Your active AI tool | Executes instructions through its own authenticated connections to these services, official careers sites and supported application sites. |
| Mailbox | Read-only recruiting updates for Track. |

Career Goals contains preferences only. It supplies function/designation/seniority criteria for Scan and broader preferences for Review. The master is a separate source of candidate facts. Settings can cache extracted preferences with the source version; an old copy cannot override an edited document.

The agent starts with [AGENTS.md](AGENTS.md), then [COMMANDS.md](COMMANDS.md) and the stage instructions. It reads current Settings and controls, checks the required connections, saves the instruction/input versions, executes the authorized work and verifies saved results. See [ARCHITECTURE.md](ARCHITECTURE.md) and [STORAGE.md](STORAGE.md).

## What you need to provide

- Your own Airtable and Google accounts, enough capacity for your data, and the correct private destinations.
- Authenticated Airtable/Drive connections in each AI tool you use. Sign-in, account consent, MFA and some workspace selection require you.
- [Career preferences](templates/career-goals.md): desired function/titles, seniority/scope, compensation, domains, responsibilities, locations and non-negotiables. Plain prose is supported; unknowns can be clarified.
- One designated editable master resume with accurate facts, plus an approved base PDF if available. Keep these current.
- Explicit company Allow/Exclude choices and known application restrictions. The agent verifies official boards; it does not assume every company is allowed.
- Answers to decision-critical questions. [CLARIFICATIONS.md](CLARIFICATIONS.md) requires agents to ask rather than invent facts, preferences or application answers.
- For actual submissions: explicit scope/authorization, approved answers and a supported browser tool. For Track: the intended mailbox and read access.

No model API key is required. Connectors may use APIs internally. Each AI tool needs its own connections; forking this repository does not copy another user's files or access. Plain chat without suitable tools cannot run the workflow.

## Set up and run

Follow [SETUP.md](SETUP.md), [CONNECTORS.md](CONNECTORS.md) and [the setup checklist](docs/SETUP-CHECKLIST.md). Register the repo and your private base once using [HARNESS-BOOTSTRAP.md](HARNESS-BOOTSTRAP.md). Fresh setup keeps submissions paused.

| Command | Scope |
|---|---|
| Run Nextmove | Scan → Review → Prepare → Apply checks/authorized submissions → Track; one saved run with stage progress. |
| Scan / Review / Prepare / Apply / Track | Run only that stage and save a handoff. Apply alone does not grant unlimited submission permission. |

For manual switching, release the prior agent's ownership and open the next configured tool. It reads Airtable/Drive to recover progress without a chat summary. Only one agent writes at a time. Missing capabilities block the affected work; the agent continues independent useful work and reports Partial or Blocked when appropriate. See [COMMANDS.md](COMMANDS.md).

Before using an existing installation, complete its schema/settings mapping and legacy review checks. The six-table design is a target, not a claim that an older base has already been migrated. Keep old records recoverable until authorized backup and replacement checks pass. Do not start production work while a migration or readiness control is paused.

## What to expect

Expect broad source coverage, a reviewable candidate pool, clear reasons for decisions, honest resumes, exact [resume filenames and versions](RESUME-FILES.md), verified writes and saved progress. [Review feedback](SCAN-OPTIMIZATION.md) improves Scan with tests that protect recall. [History](DATA-GOVERNANCE.md) records meaningful changes and events, not a row for every read.

Do not expect guaranteed interviews, offers or compensation; access to every careers site; unattended authentication; automatic launching of other AI tools; automatic submission permission; identical judgment from every model; or unlimited free storage. A successful repository check is not proof of a complete live scan or a tested application site. Service and tool limits must be reported.

Airtable does not enforce SQL-style uniqueness/transactions or provide an unchangeable all-access audit through these instructions. Direct human/API edits can bypass the agent's journal. Missing or uncertain evidence must remain visible. No hidden page caps, fabricated completion or automatic paid upgrades are allowed.

## Maintenance and sharing

Keep private data out of public Git and issues. Read [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md), [the column guide](docs/AIRTABLE-FIELDS.md) and [release checks](docs/RELEASE-CHECKLIST.md).

With Python 3.10+:

    python scripts/check_repo.py
    python scripts/build_schema.py
    python -m unittest discover -s tests -v

These check public contracts and helper behavior, not live account readiness. Licensed under [MIT](LICENSE); no private data access is granted.
