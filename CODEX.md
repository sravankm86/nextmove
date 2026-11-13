# Run a complete scan with Codex

Open the Nextmove repository in Codex. Connect access to your private Google Sheets tracker, candidate preferences and master CV. Provide private links in the session or local configuration. Verify Codex can read the Target Companies and Applications tabs, write to the tracker, and reach official career sites. Use [setup](SETUP.md) to map headers and add missing audit tabs if authorized. The repository contains instructions and templates. Codex needs working web or browser tools or a runtime that can fetch official feeds.

## 1. Scan and save jobs

Ask Codex:

> Run Nextmove's scan stage in prepare mode. Read AGENTS.md and stages/scan.md. Read my live Target Companies and Applications tabs and my broad role, seniority and geography criteria. Snapshot every allowed company and its official boards, including regional boards. Enumerate every page of every configured catalog. Use official feeds or repeatable readers where available, and inspect official careers pages for gaps. If parallel workers are available, assign disjoint groups of boards and wait for their results. Use one writer. Apply only the first-pass filter, upsert qualifying jobs into Applications as Discovered, and save the audit. Verify writes and show Complete, Partial and Failed companies, counts and remaining gaps. Stop after the scan.

A run is complete only when all planned official boards have verified coverage and all first-pass matches have been saved or matched to existing rows. Review gaps by company and source. Ask Codex to resume the unfinished sources for the same run and verify the merged audit.

## 2. Shortlist in a fresh task

Ask Codex:

> Run Nextmove's shortlist stage in prepare mode. Read AGENTS.md and stages/shortlist.md. Take the unrated Discovered jobs from my Applications tracker for the scan run I specify. Open each official description and rate relevance High, Medium or Low using my private profile and master CV. Write the rating, evidence and gaps to the existing row. Leave the rating blank if the full description cannot be verified and report why. Verify the writes and summarize counts and unresolved roles. Stop after shortlisting.
