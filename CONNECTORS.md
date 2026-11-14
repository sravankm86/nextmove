# Connect a harness

Connections belong to your accounts and harness installation, not to this repository. A new harness must establish its own access. Vendor names are examples, not certified integrations; interfaces, plans and tools change.

## Procedure

1. Open the chosen harness's supported connector/tool/MCP settings or browser-access mechanism. Use official integrations and the intended account. If no supported mechanism exposes a required capability, mark that stage unsupported in this harness.
2. Connect Airtable and Google Drive/Docs with the minimum capabilities below. Complete sign-in, consent and MFA yourself. Do not paste passwords, OAuth tokens or browser cookies into prompts, repo files or issues.
3. Grant/select the intended private base and folders through the provider's controls. Read-only access is insufficient for stages that must persist results. Schema setup additionally needs base/table/field management; ongoing stages should not need account administration.
4. Read live schema and a registered content reference. Test authorized read/write/readback through a marked setup fixture under DATA-GOVERNANCE.md. Do not claim scope restrictions that the connector cannot enforce; document the actual grant.
5. Save HARNESS-BOOTSTRAP.md with the correct repo/fork and private base reference. Record verified capabilities and missing stages privately. Disconnect/revoke access through provider settings when it is no longer needed.

Airtable workspace creation or connector consent may require a human UI step even when an agent can create a base. A human can do that step and return the verified selection; the agent then resumes SETUP.md. No autonomous account creation, paid upgrade or consent bypass is assumed.

## Capability matrix

| Scope | Required capability |
|---|---|
| Read instructions | Access repo/fork contents and a pinned revision |
| All live stages | Discover Airtable schema, paginate needed records, persist/read back results and audit |
| Content | Read registered Drive/Docs content; write and verify authorized outputs when applicable |
| Setup | Create/reuse folders and base, manage fields/links, seed and verify configuration |
| Scan | Enumerate every official catalog page or validated equivalent; save/recover durable content and state |
| Review | Read full JDs, goals and latest designated master; persist independent fit evidence |
| Prepare | Produce editable content/PDF, verify factual grounding, render/visually inspect final PDF and store it |
| Apply | Operate the exact supported application site, respect consent/authorization and capture receipts/uncertainty |
| Track | Read-only mailbox query/thread access with pagination and durable coverage checkpoints |

Do not provide mail send/delete/label powers just to reconcile messages. If a connector offers broader scopes than desired, disclose the grant and use provider-level restrictions where available; runtime instructions are not a permission boundary.

A model API key is not required. Data services may use OAuth/PAT/API authentication internally; keep these secrets in their supported credential stores. No API-free guarantee is made for connector internals.

## Switching harnesses

Release the old run owner before starting the next harness. The new session reads the same registry, pinned instructions, eligible queue and checkpoint, appends a Task Attempt and verifies access itself. Do not pass private progress only through a chat summary. Never copy browser sessions or secrets between providers as a shortcut.

