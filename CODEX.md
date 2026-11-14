# Run Nextmove workers with Codex

Open the Nextmove repository in Codex. Connect access to your private Airtable base, candidate preferences and master CV. Provide private links in the session or local configuration. Verify Codex can read the Target Companies and Applications tables, write to the tracker, and reach official career sites. Use [setup](SETUP.md) to map fields and add missing audit tables if authorized. The repository contains instructions and templates. Codex needs working web or browser tools or a runtime that can fetch official feeds.

## Portable short commands

After [one-time registration](HARNESS-BOOTSTRAP.md), use Scan, Review, Prepare, Apply or Track under [COMMANDS.md](COMMANDS.md). These commands work through the chosen harness's actual tools and shared state; they do not require model APIs. Detailed prompts below remain valid. A new harness must connect its own Airtable/Drive access and recover the saved queue/checkpoint rather than depend on this conversation.

## 1. Scan and save jobs

Ask Codex:

> Run Nextmove's scan stage in prepare mode. Read AGENTS.md and stages/scan.md. Load my live Target Companies, Applications, broad criteria and prior inventory. Reuse the private source registry, tested readers and durable checkpoints. Validate every configured official board, including regional boards; enumerate all pages unless an authoritative unchanged resource or validated change feed provides equivalent coverage. Use bounded code concurrency for bulk work and reserve model workers for specific exceptions. Process new/changed postings and reevaluate affected inventory when criteria change. Honor the configured description policy and recovery budget; default to all descriptions and no recovery cutoff if unset. Capture exact posting salary, work-location details and posted date, marking missing data explicitly. Use one writer, write only changed fields, verify readback in code, save the audit, and report Complete/Partial/Failed companies, deltas and remaining gaps. Stop after scan.

The scan uses code for bulk work; do not pass full inventories, descriptions or readbacks into model context. Reuse cached descriptions only with current evidence that covers description edits. Unchanged titles/counts alone do not establish freshness. Without durable state or tested readers, report baseline/setup work rather than promising delta execution.

The fidelity-preserving defaults capture all descriptions and impose no recovery cutoff. The private configuration may explicitly select candidate-only individual description retrieval or a recovery budget; see [scan policy tradeoffs](stages/scan.md). Record the chosen policy in every audit. Candidate-only retrieval retains all posting metadata and uncertain roles but weakens archival/re-filtering coverage after closure. A recovery cutoff can leave recoverable boards incomplete. Neither option may weaken coverage labels or hide gaps.

A run is complete only when all planned official boards have verified coverage and all first-pass matches have been saved or matched to existing rows. Review gaps by company and source. Ask Codex to resume the unfinished sources for the same run and verify the merged audit.

## 2. Review queued candidates

> Run Nextmove's Reviewer in prepare mode. Read AGENTS.md, WORKFLOW.md, LIFECYCLE.md and stages/review.md. Assess Queued and explicitly retryable review-owned records for the run I specify using full official JDs, my career goals and latest master resume. Record career fit and resume fit independently. High on either axis means Shortlisted; both Low means Not a fit; borderline or unresolved evidence stays Needs review. Preserve later states, user dispositions and history. Verify writes and report decisions and blockers. Stop after Reviewer.

Legacy shortlist commands use stages/shortlist.md as a redirect to the same Reviewer contract.

## 3. Prepare role resumes

> Run Nextmove's Preparer in prepare mode for Shortlisted jobs I specify. Read stages/prepare.md. Ground every claim in my latest editable master resume; invent nothing. Reuse an approved suitable base PDF or tailor honestly, record changes and claim grounding, verify the one-page PDF and save its version/link. Mark Ready only after integrity and readiness checks. Report gaps/blockers. Stop after Preparer; do not apply.

## 4. Apply under explicit authorization

> Run Nextmove's Applier in review mode on Ready jobs I specify. Read stages/apply.md. Check current review/resume versions, role history, live availability, answers, company limits/cooldowns and controls. Return the submission plan and blockers. Do not submit.

Actual submissions require a separate explicit auto-apply instruction and supported runtime/policy. The Applier records reported submission separately from exact-role confirmation and hands uncertainty to Tracker without blind retry.

## 5. Track mailbox updates

> Run Nextmove's Tracker in prepare mode. Read stages/track.md. Reconcile recruiting mail read-only from the last successful checkpoint with an overlapping lookback and full pagination. Match exact roles, deduplicate events, preserve later outcomes and human edits, and record evidence-backed confirmations, active recruiter engagement and outcomes. Keep uncertain/ambiguous events unresolved with a blocker. Verify writes and save the mail audit/checkpoint. Do not send mail, modify mailbox state or submit applications.
