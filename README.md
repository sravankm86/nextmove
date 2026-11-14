# Nextmove

Nextmove runs a careful job search through tool-capable AI harnesses such as Codex and Claude Code, with shared private state in Airtable and content in Google Drive.

The primary workflow is **one agent completing a thorough end-to-end run**. You can instead invoke separate stages across different connected harnesses. Both use the same criteria, evidence and handoffs. This is an instruction-led repository, not a hosted app, installed scheduler or certified integration with every harness.

## Simple architecture

| Location | Responsibility |
|---|---|
| Git | Versioned instructions, contracts and shared validation helpers |
| Airtable | Six tables: Companies, Applications, Sources, Runs, Settings, History |
| Drive | Goals, factual master, admitted-job descriptions, PDFs and bounded reports |
| Active harness | Executes through its actual authenticated tools |

See [ARCHITECTURE.md](ARCHITECTURE.md). No general work-item, attempt or artifact tables are needed.

## Admission before storage

1. Enumerate official catalogs transiently and identify possible PM roles.
2. Verify actual PM function and the configured experience or equivalent senior-scope bar from the exact description. Titles are not universal grade mappings.
3. Store verified roles as Inventoried. Clear mismatches never become new inventory; unresolved checks get minimal Run checkpoints.
4. Check domain, industry, vertical and current career goals before Queued.
5. Review fit, prepare an honest resume, apply only if authorized and track updates.

Recall is primary within the eligible PM population. Precision comes from verification before admission, not aggressive keyword rejection. See [ROLE-ELIGIBILITY.md](ROLE-ELIGIBILITY.md). Legacy application history is preserved separately from new admission.

## Prerequisites and setup

Use your own Google/Airtable accounts, private goals/criteria and designated editable master. Each harness needs authenticated Airtable/Drive access and the web, PDF/document, browser or read-only mailbox capabilities required by its stages. Plain chat without tools is insufficient.

No model API key is required. Data connectors may use OAuth, MCP or native APIs internally. Subscriptions, account consent and real storage/tool limits remain separate.

Ask a capable setup agent:

> Set up my private instance using SETUP.md. Reuse identified resources, create missing authorized private destinations and the six-table base, register my goals/master/criteria, verify readiness and keep submissions paused. Do not run production stages or migrate existing data without authorization.

Follow [SETUP.md](SETUP.md), [CONNECTORS.md](CONNECTORS.md), [the checklist](docs/SETUP-CHECKLIST.md) and [one-time bootstrap](HARNESS-BOOTSTRAP.md). Workspace creation and authentication may need a human step. Forking the repo does not copy another user's data or connections.

## Commands

| Command | Behavior |
|---|---|
| Run | Single agent: Scan → Review → Prepare → Apply → Track, with stage checkpoints and submission gates |
| Scan | Cover sources, verify admission, screen career goals and queue aligned roles |
| Review | Detailed current career/resume fit after admission gates |
| Prepare | Produce and verify a grounded base/tailored resume |
| Apply | Default preflight; submissions require explicit scope and live gates |
| Track | Exact-role mail/receipt reconciliation, read-only on mail |

Single-stage commands stop at their handoff. Run continues unaffected useful work safely, reports blocked items/stages and never labels incomplete work Complete. See [COMMANDS.md](COMMANDS.md).

## Expectations and limits

Expect durable state, honest coverage/fit reports, resume integrity and resumable handoffs. Different models can produce different judgments/wording; acceptance rules stay the same.

Do not expect guaranteed interviews, universal site access, autonomous authentication, invented facts/answers, unattended reliability or automatic permission to submit. Airtable alone does not provide SQL constraints or tamper-proof all-path auditing. [DATA-GOVERNANCE.md](DATA-GOVERNANCE.md) documents meaningful change history and its limits.

[SCALING.md](SCALING.md) distinguishes transient observations, inventory and legacy migration backups. Filtered views and Archived flags do not reclaim records.

## Sharing and contributing

Only public instructions and fictional examples belong here. Keep real resumes, job data, account links/IDs, mail, filled configuration and secrets outside public Git/issues. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

With Python 3.10+:

    python scripts/check_repo.py
    python -m unittest discover -s tests -v

These validate public contracts and admission regressions, not accounts or production runs. Licensed under [MIT](LICENSE); no access to private data is granted.
