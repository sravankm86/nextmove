# Before production work

This checklist separates repository validation from actual account readiness. Save the completed private results in Runs/Settings; never publish private identifiers or evidence.

## Instruction release

- Read every tracked file, check internal links and remove conflicting stage/status/authority rules.
- Validate JSON, schema generation, field aliases and CSV headers; run repository checks and regression tests.
- Check public content for private identifiers, resumes, job/mail data and credentials. Current-tree checks do not prove history-wide privacy.
- Publish the exact reviewed files and verify their contents and CI result.

## Private deployment

- Discover actual tables, columns, types, select options, links and business keys. Save the active mapping. Resolve duplicate lifecycle columns and preserve original values.
- Merge private resource references and controls into Settings. Mark old procedure/config tables as legacy; stale manual-only or all-read logging rules must not override Git.
- Preserve legacy outcomes. Put old unreviewed queues into a visible revalidation backlog; do not certify them from their old status.
- Verify goals/master/output references, fresh-session access, source coverage configuration and one active writer. Ask decision-critical questions under CLARIFICATIONS.md.
- Test authorized fixture writes with History, interrupted-write recovery, Drive content/readback, PDF rendering and manual handoff. Fixtures are not live stage completion.
- Confirm actual browser and read-only mailbox capabilities; absent access blocks affected stages.
- Leave submissions paused unless the user authorizes exact scope and all Apply requirements pass.
- Complete authorized backups, transfer/dependency checks and legacy retirement, or keep migration paused and list the precise blocker.

Report Passed, Blocked or Not tested for each applicable area. A clean GitHub release does not mean a paused/mismatched base is ready. Never announce full cleanup or production readiness with an unresolved deployment blocker.
