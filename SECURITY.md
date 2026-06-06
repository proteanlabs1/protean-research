# Security & disclosure policy

This archive is generated through a fail-closed safety pipeline. Nothing is
committed unless every verifier passes. Still, if you believe something
sensitive has been published, we want to know.

## Reporting a suspected leak

If you find content that looks like a secret, credential, private key, internal
path, private assay/provider packet, or any other sensitive data:

1. **Do not** open a public issue or pull request that quotes the value.
2. Contact Protean Labs privately via the channels listed at
   <https://www.protean.sh>.
3. Include the file path and a short description (not the value itself).

We will verify, rotate any affected credential, purge the content, and tighten
the verifier.

## What the verifier blocks

The publication pipeline scans every artifact for, and fails closed on:

- credential / API-key / bearer strings
- GitHub tokens (`gho_`/`ghp_`/`ghu_`/`ghs_`/`ghr_`/`github_pat_`)
- Bankr API key markers
- Telegram bot token patterns
- AWS / Slack / OpenAI / Anthropic key shapes
- private-key PEM headers and `.env`-style secret assignments
- local absolute filesystem paths (home-directory and system paths)
- private artifact references (private data directories, salt files, internal
  batch-selection files, and provider or assay request packets)
- embedding vectors and scoring-weight internals
- prompt / system-text leaks
- wet-lab order automation flags

It treats full candidate/family amino-acid sequences as **public** (they are
intentional publication data), and never flags them.

## Defense in depth

Three independent layers run before any commit:

1. The Galen-side verifier (`galen.public_research.safety`).
2. Bio's `redaction_guard`, applied to every JSON artifact.
3. The self-contained `scripts/verify_public_repo.py`, runnable by anyone.

## What this archive is not

It is not the source of truth. The Protean Ledger on Base mainnet is canonical.
This archive is a supplemental public mirror.
