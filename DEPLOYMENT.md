# Local deployment and compatibility

No Render deployment, database or paid API is required for Phase 1. No resources were
created on Render. Private GitHub source hosting is authorized separately from
product deployment; it does not make this a published plugin. Connector work is Phase 4;
plugin distribution and host acceptance are Phase 5.

## Local Codex
Keep `.agents/skills/soloos/` in the repository and open Codex in that repository.
Invoke `$soloos`. For another repository, copy the entire `soloos` folder into its
`.agents/skills/` directory, preserving assets, scripts and references. Install the
Python dependencies in a suitable local environment. Do not copy the development
repository or its `.venv` into the skill. If discovery does not update, restart Codex.

## ChatGPT
The instruction workflow includes capability detection and advisory fallback. Do not
assume a ChatGPT session has Python, jsonschema, a writable filesystem or connectors.
Where local skill loading and runtime tools are supported, the same folder is designed
to work; live installation has not been validated. In a constrained session, supply
the relevant workflow and exported data/results for advisory review, without claiming
that installing or uploading a folder enables code execution. Plugin installation
validation remains Phase 5. No Phase 1 plugin manifest is presented as installable.

## Official documentation reviewed on 2026-11-14
- https://learn.chatgpt.com/docs/build-skills
- https://developers.openai.com/codex/skills (redirected to the guide above)
- https://github.com/openai/skills/blob/main/README.md
- https://agentskills.io/specification

Current OpenAI guidance supports repo-scoped `.agents/skills`, required name/description
frontmatter and optional `agents/openai.yaml`. It recommends plugins for broader
distribution. The older skills repository marks itself deprecated and points to
OpenAI's plugins repository. These findings inform packaging, not a claim of certification.
