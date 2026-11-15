# Storage

Six active Airtable tables: Companies, Applications, Sources, Runs, Settings, History. See contracts/core-schema.json. Map live IDs/types and legacy aliases; do not force destructive recreation.

Airtable owns operational choices, admission/queue/application state, pending checks, cursors, input versions, errors and handoffs. Drive owns registered documents, candidate-role captures, PDFs and bounded reports. Git owns instructions; local/chat state is not authoritative memory.

Process catalogs without storing unrelated rows. Clear unrelated/junior roles get aggregate counts; plausible PM candidates become Inventoried even with uncertain level. Unresolved identity/availability remains minimal Run state. Review verifies final eligibility and career/resume fit before Queued. Store scan evidence/version in the Scan run and History metadata/capture; keep Decision category separately on Applications; SCAN-OPTIMIZATION.md defines feedback.

A one-off old raw catalog/retired-table backup is private recovery evidence, not normal inventory. Future rejects are not mirrored into an unfiltered shadow inventory. This reduces later re-filtering after closure; re-enumerate on criteria changes and resolve ambiguity while live.

Keep current evidence/PDF references, PDF version/verification and four stage Run links on Applications. STAGE-STATE.md locates exact metadata in History and shared fixed inputs in Runs; reusable readers stay on Sources/Settings and content in Drive. No generic artifact registry. state-schema.json is a deprecated marker.

History records meaningful deltas/events and Run read scope, not every read. Validate business keys, links and permitted state changes with verification of saved values. Report actual service limits and checkpoints; no hidden caps, base splitting or automatic plan purchase.
