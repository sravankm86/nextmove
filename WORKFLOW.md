# Run Nextmove

1. **Start one run.** Load [setup](SETUP.md), private config, live tracker headers and controls. Record a run ID, instruction revision and schedule timezone. Confirm access and mode. Reconcile recruiting messages before discovery when connected.
2. **Collect inventory.** Run [scan](stages/scan.md) for all allowed companies. Parallelize by source where useful. Keep the run visibly incomplete when any required source remains unresolved. Verified roles may proceed with the coverage gap reported.
3. **Evaluate a batch.** Pass inventory, descriptions and coverage to [shortlist](stages/shortlist.md). Advance only verified shortlisted roles.
4. **Prepare by role.** Pass each shortlisted job and its evidence to [prepare](stages/prepare.md). Verify the packet before marking it Ready.
5. **Submit and track.** Run [apply and track](stages/apply.md) serially. Check controls and authorization at submission time. Reconcile receipts and later outcomes.
6. **Report.** Publish coverage and stage totals, links to evidence and outstanding exceptions. Separate incomplete scans, unresolved eligibility, no strong matches and uncertain submissions.

## Coordinator and handoffs

Dot, a scheduled Work task or another runner can start and monitor the workflow. Use one schedule and resume from durable tracker state. In Dot, request a new visible delegated thread for the shortlist batch and inspect Activity. Stages may be separate tasks or run sequentially in one session. Pass each stage only its inputs and require output with the run ID, stage, job keys, status, evidence links and errors before advancing. Keep stage instructions in GitHub and private data in Google Workspace.

The coordinator writes shared tracker changes through a single writer. Read the current row before applying a transition and verify readback. A worker may return results without writing. Retrying a read or evaluation is safe when keyed by job and stage. A submission with uncertain outcome requires reconciliation.

## Dashboard

Use the tracker to show last run and heartbeat, allowed companies by Complete / Partial / Failed, jobs discovered, unresolved descriptions, shortlisted, Ready, Applied and exceptions. Link each exception to the company or job, latest attempt and evidence.

Pause applications blocks the next submission while scans and prep continue. Stop all prevents new stages and requires active workers to stop at their next checkpoint. Cancel delegated browser work separately if needed. A stop cannot recall a submission already sent.
