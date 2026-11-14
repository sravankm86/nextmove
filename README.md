# Nextmove

Portable, agent-agnostic job-search operations. Run with ChatGPT, Claude, Codex, or another assistant that can access GitHub, Airtable and Google Drive.

## Architecture
- **GitHub**: public, versioned instructions, contracts, and examples. No personal data or secrets.
- **Airtable**: authoritative target companies, applications, job metadata, company restrictions, controls and audit records. See [STORAGE.md](STORAGE.md).
- **Google Docs**: editable master resume, the sole source of resume facts.
- **Google Drive**: all content, including captured full job descriptions, master/resume documents and approved base or tailored one-page PDFs in the configured output folder. No separate Job Descriptions or Research folders.
- **Recruiting email**: optional read-only input for reconciliation. Read-only.

For manually chosen harnesses, save [the one-time bootstrap](HARNESS-BOOTSTRAP.md), then use **Scan**, **Review**, **Prepare**, **Apply** or **Track**. [COMMANDS.md](COMMANDS.md) defines fresh-session context recovery, whole-stage execution, resumption and verified handoffs. Each harness needs its own authenticated source access; model APIs are not required.

Start with [SETUP.md](SETUP.md), then run [WORKFLOW.md](WORKFLOW.md). Universal instructions are in [AGENTS.md](AGENTS.md). Private Airtable IDs and Google resource links belong in private configuration, not this public repository.

For worker-specific runs, follow the [Codex run instructions](CODEX.md).

## Lifecycle-driven workers

[Scanner](stages/scan.md) → Queued → [Reviewer](stages/review.md) → Shortlisted → [Preparer](stages/prepare.md) → Ready → [Applier](stages/apply.md). [Tracker](stages/track.md) independently reconciles recruiting mail and maintains Confirmed, In process and outcomes.

Reviewer qualifies a role when career fit OR resume fit is High. Both Low yields Not a fit; borderline/missing evidence remains Needs review. Preparer grounds every claim in the master resume, records changes, and verifies an approved base or tailored PDF. Scanner captures exact posting salary, work-location details and posted date, with missing values explicit.

[WORKFLOW.md](WORKFLOW.md) defines state-owned queues, handoffs and the single writer. [LIFECYCLE.md](LIFECYCLE.md) defines status evidence and migration. These are logical responsibilities, not five mandatory model agents. This repository supplies instructions/contracts/templates, not installed workers; bring a runtime, scheduler, readers and durable private state.

## Portability and safety
A runtime needs authenticated access to Airtable and Google Drive/Docs and optionally recruiting email and web search. Use native connectors or APIs; no provider-specific model behavior is required. Reuse existing resources; create only missing ones with authorization. Default to review mode. Enable automatic submission only through explicit private configuration and runtime authorization. For concurrent runs, use one writer for tracker changes; parallelize research, not conflicting writes.
