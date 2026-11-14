# Optional authorized execution

Analysis and proposal creation are the defaults. The bundled optional connector can
create a GitHub issue using the documented REST API. It does not execute payments,
contracts, deletions or binding communications; those requests remain proposals.
No connector or schedule is simulated. An installed host connector is not automatically
wired into this Python journal; do not claim audited execution through an unimplemented
bridge. Where the host cannot run this workflow, return the proposal for human handling.

## Workflow
1. Prepare `action-propose --company-id ID --target owner/repo --title TITLE
   --body-file FILE --out action.json`. This does not contact GitHub.
2. Present exact target, full title/body and fingerprint. GitHub issue creation is
   conservatively treated as a high-risk post, even for private repositories.
3. The founder runs `action-approve action.json --journal journal.sqlite --actor NAME
   --scope external_write`, reviews the content and types the exact displayed phrase.
4. Obtain separate explicit approval with a second invocation using `--scope high_risk`.
   Approvals expire after 15 minutes by default (maximum 60), bind the entire action,
   and are consumed on the first external attempt. Never type these confirmations on
   the founder's behalf. Noninteractive approval is intentionally refused.
5. Set `SOLOOS_GITHUB_TOKEN` outside repository files using a token with only the needed
   repository issue-write access. Never display, log or persist the credential.
6. Run `action-execute action.json --journal journal.sqlite --approval-id ID
   --high-risk-approval-id ID --execute`. Without `--execute`, it remains a dry-run.
7. Inspect `audit --journal journal.sqlite` and the returned provider identifier.

## Failure and trust boundaries
The same action key cannot authorize changed content. A successful duplicate returns
the original result without another HTTP write. In-flight or uncertain operations
block retry. GitHub does not provide guaranteed exactly-once creation here; the issue
body marker helps human reconciliation. If a timeout/crash occurs, inspect GitHub and
the journal before any newly approved replacement action. There is no automatic retry
or automatic rollback of external writes.

The local OS user owns the SQLite journal. This is not an identity service or defense
against a malicious process with filesystem access. Protect the journal and token with
OS access controls. A typed actor name is an audit label, not verified legal identity.
Audit events store action digests, approval scope, timestamps and outcomes; raw HTTP
exceptions and credentials are not recorded. This local audit is not tamper-proof.

Developer tests use isolated fake transports to verify the real adapter's HTTP contract.
That is a test fixture, not a fake production integration. No live business write is
performed merely to demonstrate installation.
