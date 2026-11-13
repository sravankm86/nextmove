# Run a complete scan with Codex

Open the Nextmove repository in Codex. Connect access to your private Google Sheets tracker, candidate preferences and master CV. Provide private links in the session or local configuration. Verify Codex can read the Target Companies and Applications tabs, write to the tracker, and reach official career sites. Use [setup](SETUP.md) to map headers and add missing audit tabs if authorized. The repository contains instructions and templates. Codex needs working web or browser tools or a runtime that can fetch official feeds.

## 1. Scan and save jobs

Ask Codex:

> Run Nextmove's scan stage in prepare mode. Read AGENTS.md and stages/scan.md. Load my live Target Companies, Applications, broad criteria and prior inventory. Reuse the private source registry, tested readers and durable checkpoints. Validate every configured official board, including regional boards; enumerate all pages unless an authoritative unchanged resource or validated change feed provides equivalent coverage. Use bounded code concurrency for bulk work and reserve model workers for specific exceptions. Process new/changed postings and reevaluate affected inventory when criteria change. Honor the configured description policy and recovery budget; default to all descriptions and no recovery cutoff if unset. Use one writer, write only changed fields, verify readback in code, save the audit, and report Complete/Partial/Failed companies, deltas and remaining gaps. Stop after scan.

The scan uses code for bulk work; do not pass full inventories, descriptions or readbacks into model context. Reuse cached descriptions only with current evidence that covers description edits. Unchanged titles/counts alone do not establish freshness. Without durable state or tested readers, report baseline/setup work rather than promising delta execution.

The fidelity-preserving defaults capture all descriptions and impose no recovery cutoff. The private configuration may explicitly select candidate-only individual description retrieval or a recovery budget; see [scan policy tradeoffs](stages/scan.md). Record the chosen policy in every audit. Candidate-only retrieval retains all posting metadata and uncertain roles but weakens archival/re-filtering coverage after closure. A recovery cutoff can leave recoverable boards incomplete. Neither option may weaken coverage labels or hide gaps.

A run is complete only when all planned official boards have verified coverage and all first-pass matches have been saved or matched to existing rows. Review gaps by company and source. Ask Codex to resume the unfinished sources for the same run and verify the merged audit.

## 2. Shortlist in a fresh task

Ask Codex:

> Run Nextmove's shortlist stage in prepare mode. Read AGENTS.md and stages/shortlist.md. Take the unrated Discovered jobs from my Applications tracker for the scan run I specify. Open each official description and rate relevance High, Medium or Low using my private profile and master CV. Write the rating, evidence and gaps to the existing row. Leave the rating blank if the full description cannot be verified and report why. Verify the writes and summarize counts and unresolved roles. Stop after shortlisting.
