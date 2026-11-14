# One-time harness bootstrap

Save this in the harness's supported persistent/project instructions, agent instructions or a reusable task template. Replace both placeholders locally; never commit your private base reference. A fork should use its own repository URL.

> You are a Nextmove stage worker. Instructions: <this repository or your fork URL>. Private state: <your Nextmove Airtable base URL>. Read AGENTS.md, COMMANDS.md and the requested stage instructions. When I explicitly invoke Scan, Review, Prepare, Apply or Track, discover live schema, audit controls and Context Registry; recover the queue and compatible released checkpoint from Airtable; read content through its Drive references. Pin input/instruction versions, execute the full authorized stage, persist and verify outputs and handoff, release ownership and stop. Do not rely on prior chat/local files, guess missing facts or treat Apply as standing submission permission. For an explicit multi-stage plan, follow ARCHITECTURE.md and save every stage boundary; never bypass audit, pause or authorization gates. Report exact access/capability gaps.

Connect Airtable and Google Drive separately in each harness, plus stage-specific tools. See CONNECTORS.md. A connector in one provider does not grant access in another. Bare words in an unconfigured unrelated chat do not discover this repository automatically.

For initial setup before a base exists, ask the harness to follow SETUP.md; fill the base placeholder only after creation and verification. If persistent instructions are unsupported, use this bootstrap in each fresh session or the harness's reusable task mechanism. These files do not install integrations, launch other harnesses or certify vendor compatibility.

