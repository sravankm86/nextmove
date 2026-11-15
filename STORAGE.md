# Storage

Six active Airtable tables: Companies, Applications, Sources, Runs, Settings, History. See contracts/core-schema.json. Map live IDs/types and legacy aliases; do not force destructive recreation.

Airtable owns operational choices, admission/queue/application state, pending checks, cursors, input versions, errors and handoffs. Drive owns registered documents, candidate-role captures, PDFs and bounded reports. Git owns instructions; local/chat state is not authoritative memory.

Process catalogs transiently. Clear unrelated/junior roles get aggregate counts; plausible PM candidates become Inventoried even with uncertain level. Unresolved identity/availability remains minimal Run state. Review verifies final eligibility and career/resume fit before Queued. Store scan evidence/version and review reason categories separately; SCAN-OPTIMIZATION.md defines feedback.

A one-off old raw catalog/retired-table backup is private recovery evidence, not normal inventory. Future rejects are not mirrored into an unfiltered shadow inventory. This reduces later re-filtering after closure; re-enumerate on criteria changes and resolve ambiguity while live.

Keep current artifact references on Applications, reusable reader references on Sources/Settings and previous values in History. No generic artifact registry. state-schema.json is a deprecated marker.

History records meaningful deltas/events and Run read scope, not every read. Validate business keys, links and permitted state changes with readback. Report actual service limits and checkpoints; no hidden caps, base splitting or automatic plan purchase.
