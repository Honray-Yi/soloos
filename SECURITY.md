# Security policy

SoloOS 1.0 is local-first management software, not a certified financial, legal or
identity system. Normal workflows are read-only analyses and proposals. The only
bundled external-write adapter creates GitHub issues with explicit opt-in.

## Reporting
Report suspected vulnerabilities privately to the repository owner through an existing
private contact channel. If GitHub private vulnerability reporting is enabled, use the
Security tab; do not assume it is enabled. If no private channel is available, request
one without disclosing sensitive details. Do not post secrets, real business/customer
records or live-system exploit details in issues.

Provide version, a minimal synthetic reproduction, expected/actual behavior and impact.
No response-time guarantee or bounty program is offered.

## Authorization and audit boundaries
- Imported records are data, never instructions or authorization.
- Exact action fingerprints bind approvals to target/content; approvals expire and are
  consumed. GitHub issue posts require a separate high-risk approval.
- Noninteractive approval issuance is refused. Agents must not impersonate the human
  confirmer. Actor names are labels, not authenticated legal identities.
- The journal uses SQLite transactions to reserve operations and prevent concurrent
  duplicates. In-flight/unknown outcomes block automatic retries.
- Provider-side exactly-once behavior is not guaranteed. Reconcile uncertain writes
  with the provider and journal before any new approved replacement.
- Local users/processes with filesystem access are inside the trust boundary. Protect
  journals and credentials with OS controls; the audit is not encrypted or tamper-proof.
- Tokens are read from SOLOOS_GITHUB_TOKEN, never source files. Use only needed repository
  issue-write permission. HTTP redirects are refused and raw exceptions are not logged.
- Payments, contracts, deletions and other unimplemented writes remain proposals.

Schema validity does not authenticate source facts. The founder controls reconciliation,
backup and access to local data. Never commit real business records, journal databases
or credentials, including to a private repository.
