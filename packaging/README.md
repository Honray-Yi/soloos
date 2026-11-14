# Packaging sources

`plugin.json` is the portable skill-only plugin manifest; the package contains no
server, lifecycle hooks, fake MCP mapping or credential. `marketplace.json` is the
source for the repo-local `.agents/plugins/marketplace.json` catalog.

The canonical runtime lives in `.agents/skills/soloos`. `tools/build_plugin.py`
copies it into the package's required `skills/soloos` layout, writes checksums and
optionally creates a deterministic ZIP. The committed `plugins/soloos` folder is a
generated distribution copy. Rebuild it through an inspected staging directory when
the runtime changes; never edit its copies independently.

Text assets are normalized to LF before hashing and packaging. `.gitattributes`
preserves LF in repository checkouts so checksum verification works on Windows/Linux.

`agent-plugin.schema.json` was retrieved without modification on 2026-11-14 from
https://agent-plugins.org/schemas/1.0.0/plugin.schema.json for offline validation.
It is a third-party specification resource, not original SoloOS source; retain its
source attribution. Structural validation is supplemented with path and executable
package tests. It does not certify acceptance by every host or public directory.
