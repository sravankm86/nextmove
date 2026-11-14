# Run Nextmove

Read AGENTS.md and the requested stage. Load reference docs only when needed, and keep bulk catalogs/readback outside model context.

| Command | Scope |
|---|---|
| Run / Run Nextmove | Default single agent: Scan → Review → Prepare → Apply → Track |
| Scan | Source coverage, verified PM admission, career screen before Queued |
| Review / Assess / Shortlist | Gated queue and explicitly retryable legacy/review backlog |
| Prepare | Current eligible Shortlisted roles |
| Apply | Ready roles; default preflight unless separately authorized |
| Track | Exact-role mail/receipt reconciliation from checkpoint |

Quoted examples/setup discussions do not dispatch production work. A single stage stops after handoff. Run advances authorized useful stages without asking to continue, but cannot infer submission permission or launch another harness.

## Startup and ownership

Discover/map the six tables, Settings and live controls. Record run-level read scope, not routine per-read events. Resolve goals/master/content as required and verify this harness's access/capabilities. Connections and local files are not inherited.

Resume one compatible released unfinished Run or create one. Pin instruction/input versions, owner and frozen scope. A full run uses one row with stage checkpoints; manual invocations use the same checkpoint format. Sources hold board cursors and Applications hold job state. Bounded Run segments handle oversized pending lists without truncation.

One active writer. Never seize an owner solely on timeout. Missing global access, Stop all or uncertain writes block affected work; item problems need not stop independent work. Submission pause affects Apply, not useful Scan/Review/Prepare/Track work.

## Execute and persist

Use code for enumeration, normalization, identity, candidate filters, hashes and verification. Reuse verified unchanged inputs, but recheck authoritative versions and live gates at relevant boundaries. No unverified TTL, hidden page/item/time cap or false completion after one batch.

Scan creates records only after verified PM/experience-or-scope admission. Uncertainty stays in minimal Run checkpoints; unrelated clear failures only produce aggregate counts. Career screening precedes Queued. ROLE-ELIGIBILITY.md defines the gate.

Preserve human outcomes/notes. Legacy broad Queued rows require revalidation under the new policy, not automatic certification. Do not reopen submitted/terminal roles when fit inputs change.

Reread affected state, reconcile human edits, write permitted deltas and verify actual persisted values/artifacts. Save meaningful changes/events and failed/uncertain writes in History under the run. For bounded migration batches, exact per-record private delta artifacts can be indexed by a verified History manifest; never hide unverified changes.

Current description/resume references, versions and verification live on Applications. Content lives in registered Drive locations. A vanished local reader is a recovery gap, not evidence of incremental support.

Review respects admission/career gates. A base PDF requires factual/current/visual verification; a URL does not mean Ready. Before Submit persist unique attempt identity and exact resume version. Require explicit scope, answers, availability, restrictions and live controls; capture receipt or uncertainty. Never blind-retry, and never infer non-submission from missing mail.

## Stage boundaries and exit

Save accepted stage outputs before advancing. Continue independent useful work safely, but blocked required stages/items mean Partial/Blocked. Verify every planned item and count before Complete. No work means verified empty eligible scope, not invented coverage.

Persist versions, outputs, pending identities/reasons, errors, next action and ownership release. Report source coverage, transient rejects, verification candidates, admitted inventory, career queue and later outcomes separately. A new harness must recover this without prior chat/local state.
