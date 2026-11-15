# Nextmove

Nextmove runs a careful job search through tool-capable AI harnesses such as Codex and Claude Code, with shared private state in Airtable and content in Google Drive.

The primary workflow is **one agent completing a thorough end-to-end run**. You can instead invoke separate stages across different connected harnesses. Both use the same criteria, evidence and handoffs. This is an instruction-led repository, not a hosted app, installed scheduler or certified integration with every harness.

## Simple architecture

| Location | Responsibility |
|---|---|
| Git | Versioned instructions, contracts and shared validation helpers |
| Airtable | Six tables: Companies, Applications, Sources, Runs, Settings, History |
| Drive | Goals, factual master, candidate-job descriptions, PDFs and bounded reports |
| Active harness | Executes through its actual authenticated tools |

See [ARCHITECTURE.md](ARCHITECTURE.md). The same Career Goals source supplies broad function/seniority criteria for Scan and broader career-fit criteria for Review. End users supply preferences using ordinary prose or the optional [Career Goals template](templates/career-goals.md); [CAREER-GOALS.md](CAREER-GOALS.md) keeps all interpretation and workflow instructions in Git. No general work-item, attempt or artifact tables are needed.

## Candidate inventory, then review

1. Scan every official catalog page and use broad PM keywords with basic semantic checks.
2. Save plausible senior PM candidates as Inventoried, including uncertain level/function boundaries for Review. Clear unrelated/junior roles stay out; Scan derives role criteria from Career Goals but does not assess broader career fit.
3. Review the full description for final role/scope eligibility, career goals and resume fit. Approved candidates become Queued for preparation; others receive explicit reasons or Needs review.
4. Prepare verifies an honest resume, Apply submits only if authorized, and Track reconciles updates.

Recall is primary. Inventory is a candidate pool, not proof of eligibility. Review feedback improves basic scan criteria through versioned tests, not automatic rejection of every non-queued pattern. See [ROLE-ELIGIBILITY.md](ROLE-ELIGIBILITY.md) and [SCAN-OPTIMIZATION.md](SCAN-OPTIMIZATION.md). Legacy history is preserved; Shortlisted is a legacy status, not an extra new stage.

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
| Scan | Cover sources and inventory plausible PM candidates using keywords/basic semantics |
| Review | Verify full eligibility and career/resume fit; approve Queued and record feedback |
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

These validate public contracts and scan/review regressions, not accounts or production runs. Licensed under [MIT](LICENSE); no access to private data is granted.
