# Set up the six-table instance

Read AGENTS.md, ARCHITECTURE.md and CONNECTORS.md. A setup request authorizes missing private destinations/configuration, not paid upgrades, real submissions or an unrequested tracker migration.

1. Confirm the user's Google/Airtable accounts, goals, PM admission threshold/equivalent-scope benchmark, geography/domain preferences and designated editable master. Use CAREER-GOALS.md and offer templates/career-goals.md for preference capture; do not ask the user to author agent instructions. Keep master/answer references and workflow configuration outside that document. Unknown inputs remain unresolved. Human login/consent/workspace selection may be necessary; do not invent account access.
2. Reuse identified resources. Otherwise create/select a private workspace and Nextmove base; create a private Drive root with Resumes and Content children. Preserve existing parents/sharing and document locations.
3. Provision only Companies, Applications, Sources, Runs, Settings and History from contracts/core-schema.json. Resolve actual IDs, create links in a second pass, add computed metadata through supported tools and read back fields/types/options/links. Never send values into computed fields. state-schema.json is a deprecated marker, not extra tables.
4. Extract the Scan-criteria and Review-queue preference projections from the current goals revision using CAREER-GOALS.md. Record readiness, evidence and missing/conflicting values; clarify only decision-critical gaps. Populate Settings using contracts/setup-seed.json: repository, goals/master/destinations, role policy, current criteria, optional reader/base/mail/answer resources, execution policy and safe controls. Preserve existing user values. Pause applications=true; no submission scope/cap implied.
5. Register one Sources row per official board/region for explicit Allow companies. Missing configuration is a coverage gap, not permission to omit a company.
6. Save HARNESS-BOOTSTRAP.md in each intended harness with private references outside Git. Verify actual source/tool capabilities there. Default is one agent running the full plan; manual stages share the same state.
7. Test authorized fixture create/read/update/archive with meaningful History, Drive readback and fresh-session recovery. Fixtures are not production jobs, scan coverage or Ready resumes. Check interrupted writes, stale inputs and submission uncertainty safely without submitting a form.
8. Return/store a private readiness report with actual references/mappings, tested capabilities, per-stage blockers, scope and next action. No false “fully operational” claim from empty tables.

The base/journal cannot audit creation before they exist. Record the bootstrap boundary honestly once History is available. Routine reads use Run scope rather than per-read logs. DATA-GOVERNANCE.md explains limitations.

## Migration

An authorized migration needs a complete durable verified backup, dependency/identity map, exact per-record delta evidence and final readback. Retain human application outcomes/notes and old references. Retire generic task/config/artifact tables only after their useful state is merged. A one-off old raw archive is not new inventory.

Legacy unreviewed Queued roles need eligibility/career revalidation. They do not automatically pass the new gate, and new criteria do not erase submitted/terminal history. Physical cleanup and backup destinations require authorization; never bypass automatic approval rejection. A local file alone is not a durable recovery plan.

## Operation

Scan uses keywords/basic semantics and stores plausible PM candidates, including uncertain level, without career filtering. Review owns full eligibility/career/resume checks and Queued approval. ROLE-ELIGIBILITY.md and SCAN-OPTIMIZATION.md define boundaries and feedback. Do not claim title-only company-grade equivalence or introduce hidden caps.

Keep one writer, current input versions, verified changes and recoverable handoffs. Apply remains scoped, paused by default and gated by answers/resume/availability/restrictions. Mail stays read-only. See docs/COMPANY-RESTRICTIONS.md and docs/SETUP-CHECKLIST.md.
