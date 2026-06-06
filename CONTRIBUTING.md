# Contributing

This repository is a **generated, single-maintainer archive**. Its contents are
produced automatically by Galen (the operational auditor for Protean) from
approved public surfaces and committed through a fail-closed safety verifier. It
is not a collaborative codebase, and pull requests that add or edit artifacts
will not be merged — artifacts are regenerated from the runtime, so manual edits
would be overwritten and would bypass the safety gate.

## How to engage

- **Found something that looks like a leak?** Please report it privately — see
  [`SECURITY.md`](SECURITY.md). Do not open a public issue containing the
  suspected sensitive value.
- **Found a factual or provenance discrepancy?** Verify against the source of
  truth first: the Protean Ledger on Base mainnet and the reproducible Digest.
  This archive is a supplemental mirror; the chain is canonical. If the
  discrepancy is real, open an issue describing it (without pasting any private
  data) and reference the on-chain record.
- **Want to verify the archive yourself?** Clone it and run the self-contained
  verifier:

  ```bash
  python scripts/verify_public_repo.py
  ```

  It is stdlib-only and exits non-zero if it finds any leak class.

## What will not be accepted

- Edits to generated artifacts (they are regenerated and re-verified).
- Any content that bypasses or weakens the safety verifier.
- Requests to publish private runtime artifacts, raw assay data, secrets, or
  wet-lab order automation.

## Provenance

Every artifact carries a generation timestamp and a boundary statement, and is
indexed in `indexes/manifest.jsonl` with a content hash. The manifest hash in
`indexes/latest.json` changes only when artifact content changes.
