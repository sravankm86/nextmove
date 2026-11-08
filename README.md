# Nextmove

Portable, agent-agnostic job-search operations. Run with ChatGPT, Claude, Codex, or another assistant that can access GitHub and Google Workspace.

## Architecture
- **GitHub**: public, versioned instructions, contracts, and examples. No personal data or secrets.
- **Google Sheets in Google Drive**: persistent application tracker and authoritative target-company list.
- **Google Docs**: editable master resume, the sole source of resume facts.
- **Google Drive**: tailored one-page PDF resumes in one output folder, with descriptive filenames. No separate Job Descriptions or Research folders.
- **Recruiting email**: optional read-only input for reconciliation. Never send email or submit applications.

Start with [SETUP.md](SETUP.md), then run [WORKFLOW.md](WORKFLOW.md). Universal instructions are in [AGENTS.md](AGENTS.md). Private Google resource links belong in private configuration, not this public repository.

## Portability and safety
A runtime needs authenticated access to Google Sheets/Drive/Docs and optionally recruiting email and web search. Use native connectors or APIs; no provider-specific model behavior is required. Reuse existing resources; create only missing ones with authorization. Default to review mode. For concurrent runs, use one writer for tracker changes; parallelize research, not conflicting writes.
