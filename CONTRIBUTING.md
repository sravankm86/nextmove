# Contributing

Nextmove is an instruction-led project for tool-capable harnesses. Contributions should improve portable behavior, evidence quality, setup or recovery without introducing private user data or requiring a particular model API.

## Before proposing a change

Read AGENTS.md, ARCHITECTURE.md, DATA-GOVERNANCE.md and the affected stage. Use fictional examples. Describe the concrete trigger, resulting behavior, validation and known capability limits. No account identifiers, real resumes, mail excerpts, private links, browser state or raw job snapshots belong in issues, patches, screenshots or CI artifacts.

For a bug, provide a redacted harness/capability description, instruction revision, expected behavior and minimal fictional reproduction. For a security or privacy exposure, follow SECURITY.md instead of opening a public issue with sensitive details. Feature requests should explain the goal and any effect on fidelity, costs or permissions.

## Local workflow

1. Fork/clone the public repository and create a focused branch. Keep filled configuration and credentials outside the checkout.
2. Change the relevant contracts/docs and update their cross-references. Preserve existing deployments through explicit aliases and migrations; don't assume CSV headers are physical field IDs.
3. If changing core schema generation, edit scripts/build_schema.py and regenerate contracts/core-schema.json with Python 3.10+.
4. Run `python scripts/check_repo.py`. For a core schema change, also run `python scripts/build_schema.py` and confirm the generated file is committed.
5. Explain validation honestly. Repository checks do not prove a live scan, connector grant or cross-harness integration. Test live behavior only in your own authorized private resources and publish only redacted findings.

Keep reviews small enough to assess. Do not silently change the career-fit OR rule, resume-fact source, full catalog/description defaults, user-selected company scope, submission consent, one-writer ownership or audit claims. Propose intentional tradeoffs explicitly. Update CHANGELOG.md for user-visible behavior or schema changes.

CI uses standard-library Python and read-only GitHub permissions. Do not add external uploads, credentials, model API calls or paid service execution to public checks. Gitignore rules and regex checks reduce accidental disclosure; they cannot prove that every kind of private text is absent. Inspect the diff yourself before pushing.

## Maintainer checklist

Review data boundaries and contract compatibility; require passing public checks before merging when branch rules are available. Enable appropriate branch protection/rulesets, secret scanning/push protection and private vulnerability reporting in repository settings where supported. Those account-level settings are not configured by these files. Keep pinned Actions dependencies current and review bot updates. Do not claim a security feature is enabled without checking settings.

Contributions are distributed under the repository's MIT license. Do not submit material you lack permission to share. Follow CODE_OF_CONDUCT.md.
