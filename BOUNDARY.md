# Boundary

This file is the scope contract for the Protean Research archive. It mirrors the
boundary statement carried in every artifact.

## What this archive is

A curated, review-safe **public research notebook** for the Protean discovery
runtime, maintained by Galen. It is a reading view over approved public surfaces.

## What this archive is NOT

- **Not the source of truth.** The Protean Ledger on Base mainnet (chain 8453)
  is canonical, followed by the reproducible Digest / indexer. This archive is a
  supplemental mirror and must never be cited as canonical.
- **Not clinical or therapeutic claims.** Nothing here asserts safety, efficacy,
  therapeutic effect, or clinical readiness.
- **Not validated results.** Computational rankings are research-prioritization
  signals. A result is only described as assay-backed when an explicit reviewed
  wet-lab label is cited. The wet-lab loop is currently review-gated and dormant.
- **Not investment, governance, or token promises.** Nothing here promises
  financial returns, governance control, automatic holder benefits, or claims on
  research outcomes.
- **Not a wet-lab order surface.** No content here places, accepts, or authorizes
  any provider order. Wet-lab rationale is review-gated and non-ordering.

## What is published

- Full candidate and family amino-acid sequences, when sourced from an approved
  public publication surface (intentional under the 2026-06-03 sequence policy).
- On-chain sequence commitments and ledger record references.
- Aggregate frontier-health metrics, scientific contradictions, runtime status,
  and calibrated research narratives.

## What is never published

Credentials, API keys, wallet private keys, salts, local filesystem paths,
`.env` values, embeddings, private assay/provider packets, operator-private
notes, scoring-weight internals, model-routing internals, raw failure logs,
prompt/system text, and any wet-lab order automation flags.

## Enforcement

A fail-closed verifier runs before every commit. Findings abort the publish. The
verifier is implemented Galen-side (`galen.public_research.safety`), backed by
Bio's `redaction_guard`, and reproduced as a self-contained scanner in
[`scripts/verify_public_repo.py`](scripts/verify_public_repo.py).

## What changes this boundary

Only the Protean operator. This file is the contract; it is changed by editing
it in the source runtime, not by any automated process. No automated run loosens
this scope.
