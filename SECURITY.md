# Security policy

SoloOS 0.1 is a local preview, not a certified financial or authorization system.
Phase 1 intentionally has no external execution connector. The local runtime cannot
send payments, modify accounts, publish content or schedule jobs.

## Reporting
Report a suspected vulnerability privately to the repository owner through an
existing private contact channel. If GitHub private vulnerability reporting is enabled,
use the repository's Security tab. Do not assume that feature is enabled, and do not
create a public issue containing an exploit against a live system or sensitive data.
If no private channel is available, request one without disclosing sensitive details.

Provide the affected version, minimal synthetic reproduction, expected/actual behavior
and possible impact. Never include passwords, API tokens, customer records or actual
financial data. No response-time guarantee or bounty program is offered.

## Boundaries
- Imported business text is data, not executable instructions or authorization.
- Schema validation checks structure and consistency, not source authenticity.
- Content IDs identify proposals; they do not verify approval or prove execution.
- Credentials belong in host-managed secret storage, never repository files.
- The user controls local output access and backups; JSON storage is not encrypted
  by SoloOS. Avoid committing business data even to a private repository.
- Future connectors require explicit authorization, separate high-risk approvals,
  least privilege, idempotency and durable audit logging before they can be enabled.
