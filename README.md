# Nextmove

Nextmove helps you run a job search through AI harnesses such as **Codex and Claude Code**, while keeping your progress independent of any one chat or model. It defines five stages: discover jobs, assess fit, prepare an honest resume, apply under explicit authorization, and track updates.

This is an early-stage **instruction and data-contract repository**. It contains stage instructions, schemas, templates, examples and repository checks. It is not a hosted application, installed agent fleet or universal connector package.

## Purpose

Make a job search repeatable, inspectable and resumable. Your career goals, target-company choices, evidence and application history should survive switching harnesses or starting a fresh session.

You can use one capable harness for all stages, or manually choose a different harness for each. Both must follow the same lifecycle, acceptance checks, controls and durable handoff contract. Model judgments and resume wording can vary; identical output text is not promised.

## Prerequisites

| Requirement | What you need |
|---|---|
| Tool-capable AI harness | A harness that can read these instructions and use authenticated data, web and file tools. A plain chat without those tools cannot execute the workflow. |
| Google account | Private Google Drive storage and Google Docs access for goals, the editable master resume and generated content. |
| Airtable account | Permission to create or reuse a workspace/base and manage the required tables and fields. A workspace alone is not a database. |
| Connections in each harness | Authenticated Airtable and Google Drive access. Use supported connectors, MCP, approved native tools or browser access with equivalent verification. Connections are not shared automatically between harnesses. |
| Private inputs | Career criteria, geography/work preferences, timezone, target companies and a factual editable master resume. Unknown inputs remain blockers. |
| Stage-specific tools | Complete official catalog/web access for Scan; full content access for Review; document/PDF production and visual verification for Prepare; supported browser for Apply; optional read-only mailbox for Track. |

No **model API key** or custom model-API orchestration is required. Data connectors may themselves use APIs, OAuth or access tokens. Harness subscriptions, connectors and storage limits are separate; the repository does not purchase or configure paid plans.

Full catalogs can exceed a small Airtable plan. Read [SCALING.md](SCALING.md) before choosing a storage profile. A filtered view does not reduce stored records.

## Architecture

- **Git** owns versioned instructions and public contracts.
- **Airtable** owns private operational state: company choices, application lifecycle, queues, attempts, checkpoints, decisions, controls and audit records.
- **Google Drive** owns content: goals, the designated editable master, captured descriptions, PDFs and reusable artifacts.
- **The active harness** performs the work through its actual tools. The human supplies sources, consent and authorization.

Every stage recovers its inputs from shared state, verifies outputs and saves a handoff. Prior chat, local files and provider memory cannot be the only source of progress. Only one writer owns shared mutations.

[ARCHITECTURE.md](ARCHITECTURE.md) explains the complete data model, execution arrangements, recovery, trust boundaries and implementation limits.

## Set up your own private instance

Your friend should create **their own** private resources. Forking this public repo does not copy anyone's Airtable records, resume, credentials or connected accounts.

1. Read [SETUP.md](SETUP.md), or give a capable setup agent this request:

   > Set up my private Nextmove instance using SETUP.md. Reuse resources I identify; create only missing authorized Drive folders and Airtable base/tables from both schema contracts. Register my private inputs and safe controls, help me connect this harness, verify the setup checklist, and report exact blockers. Keep submissions paused. Do not run a real stage or import/migrate existing tracker data without my authorization.

2. Complete account sign-in and connector consent yourself when requested. If the agent cannot create a workspace or connection, follow the specific human step and resume setup.
3. Save the [one-time bootstrap](HARNESS-BOOTSTRAP.md) in each harness you intend to use, with your repository and private base references.
4. Verify readiness with [the setup checklist](docs/SETUP-CHECKLIST.md). Setup should return private resource links, live schema mappings, tested capabilities and unresolved stages—not just say “done.”

The blueprints are [core-schema.json](contracts/core-schema.json) and [state-schema.json](contracts/state-schema.json). They describe seventeen logical tables; connectors may require several creation passes and ID resolution. CSV templates alone do not create typed fields or relationships. No one-click provisioner is installed.

## Run the stages

| Command | Expected result |
|---|---|
| **Scan** | Enumerate allowed companies' official sources; retain broad candidates as Queued, posting metadata and coverage evidence |
| **Review** | Assess the full JD against career goals and the master; record both fit axes and Shortlisted / Not a fit / Needs review |
| **Prepare** | Verify an approved base or tailored resume, grounded in the master, with changes and artifact evidence; advance eligible roles to Ready |
| **Apply** | Default preflight/review; submit only with explicit scoped authorization and all live gates satisfied |
| **Track** | Reconcile exact-role receipts, active recruiter engagement and outcomes; mailbox remains read-only |

See [COMMANDS.md](COMMANDS.md), [WORKFLOW.md](WORKFLOW.md) and [LIFECYCLE.md](LIFECYCLE.md). A bare command runs only that stage and stops. Interrupted compatible work resumes from a released checkpoint; “complete batch” never means “complete queue.”

For one harness doing several stages, explicitly request an ordered plan, for example:

> Run Scan, then Review, then Prepare under ARCHITECTURE.md. Persist the plan, stage checkpoints and handoffs. Stop on unresolved stage gaps. Do not apply.

A human can instead invoke each command in a different connected harness. The evidence and completion requirements stay the same. Multi-stage plans never create submission authorization implicitly.

## What to expect

A durable tracker, honest scope/coverage reports, traceable decisions, resume integrity checks, explicit blockers, resumable work and small handoffs between harnesses. Complete, Partial, Blocked and No work have distinct meanings. Missing salary, location, dates or eligibility evidence remain visible.

Scan defaults preserve complete catalog coverage, all captured descriptions and no user-selected recovery cutoff. Code handles bulk parsing, comparison and verification; models handle judgment and exceptions.

## What not to expect

- Guaranteed interviews, eligibility, job availability, perfect fit judgments or identical results across models.
- Universal access to every careers site, authentication flow or application form; supported capabilities must be tested.
- A background scheduler, installed feed readers, automatic cross-harness launching or guaranteed unattended operation.
- Permission to invent resume claims, guess application answers, send recruiting mail or submit because a job is Ready.
- SQL-enforced business constraints or tamper-proof all-path CRUD auditing from Airtable alone. Native revision history is plan-limited; custom journals do not intercept every UI/API action.

[DATA-GOVERNANCE.md](DATA-GOVERNANCE.md) describes the audit requirement and enforcement gaps. [SECURITY.md](SECURITY.md) covers private data, untrusted content and reporting.

## Share and contribute

Only public instructions and fictional examples belong here. Keep real resumes, profiles, job snapshots, account IDs/links, mail, tokens and generated artifacts out of Git, issues and pull requests. Defaults keep submissions paused.

Read [CONTRIBUTING.md](CONTRIBUTING.md). Run the dependency-free public checks with Python 3.10+:

    python scripts/check_repo.py

The checks validate contracts, local documentation links, public-data boundaries and schema consistency. They do not test your accounts, provision resources or certify a harness integration. CI runs the same checks.

Licensed under [MIT](LICENSE). This license covers the repository, not your private data or third-party services.

