# Installation, distribution and compatibility

## Standalone Codex skill
Clone the private repository, open Codex in it, install the Python requirements and
invoke `$soloos`. The runtime is `.agents/skills/soloos`. For another project copy
that whole folder into its `.agents/skills`; do not include the development virtual
environment. Python 3.11+ with jsonschema and tzdata enables deterministic commands.
On Windows use the virtual environment's Scripts/python.exe; on Unix use bin/python.

## Portable plugin
The generated package lives at `plugins/soloos`, with root `plugin.json` and
`skills/soloos/SKILL.md`. The manifest is validated against the official Agent Plugins
1.0 schema. Build a fresh copy and ZIP:

```text
python tools/build_plugin.py --output work/release-plugin --archive dist/soloos-plugin.zip
```

Choose new output paths. The builder includes runtime assets and checksums and excludes
Python caches. Update canonical sources, then rebuild the generated distribution;
the tests reject drift between the committed plugin and standalone skill.

## Private local marketplace
`.agents/plugins/marketplace.json` points to `./plugins/soloos` relative to the
repository root. With a supported Codex CLI:

```text
codex plugin marketplace add .
codex plugin list --marketplace soloos-private --available --json
```

This local registration and discovery were verified: `soloos@soloos-private`,
version 1.0.0, appears available. The plugin has not been enabled automatically.
Choose it in a supported host's Plugins interface, or inspect your CLI's
`codex plugin add --help` for its installation syntax. Use either the standalone
skill or installed plugin in a project to avoid duplicate entries. Restart/refresh
the host if it retains an older cached package.

## ChatGPT and constrained hosts
| Surface | Verified status |
| --- | --- |
| Local Python runtime | Automated tests and end-to-end examples |
| Extracted plugin runtime | Automated subprocess tests |
| Codex marketplace discovery | Verified using installed CLI |
| ChatGPT desktop plugin installation | Not performed; needs a supported host installation |
| ChatGPT web/mobile invocation | Not performed; do not assume local runtime access |
| Optional GitHub connector | Offline HTTP contract and failure tests; no live write |

When Python/files/dependencies are unavailable, use the skill's advisory workflow with
supplied data or exported results. Label unexecuted arithmetic and schema validation.
Neither copying a folder nor loading a skill grants code execution, durable storage,
connector access or scheduling. Do not claim universal host acceptance.

## Optional external execution
Read the bundled operations reference. Provide a least-privilege issue-write token
outside the repository only if needed, and obtain two exact human confirmations.
Do not run a live write just to test setup. No Render service is required or created.
The private GitHub repository is source hosting, not public plugin-directory publication.

## Reviewed documentation (2026-11-14)
- https://learn.chatgpt.com/docs/build-skills
- https://developers.openai.com/codex/skills
- https://github.com/openai/skills/blob/main/README.md
- https://agentskills.io/specification
- https://developers.openai.com/plugins/build/plugins
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://docs.github.com/en/rest/issues/issues#create-an-issue

The older OpenAI skills repository redirects distribution guidance toward plugins.
The current portable layout and repo marketplace inform this package; they do not
constitute certification or authorization for public publication.
