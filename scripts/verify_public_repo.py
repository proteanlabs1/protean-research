#!/usr/bin/env python3
"""Self-contained, fail-closed leak verifier for the Protean Research archive.

This script is intentionally dependency-free (Python standard library only) so
anyone who clones this public repository can independently verify that it
carries no secrets, credentials, private keys, local paths, private-artifact
references, embeddings, scoring internals, wet-lab order automation, or prompt
leaks. It mirrors the authoritative Galen-side verifier.

It treats full candidate/family amino-acid sequences as PUBLIC (intentional
publication data) and never flags them.

Usage:
    python scripts/verify_public_repo.py            # scan this repo
    python scripts/verify_public_repo.py PATH ...   # scan given paths
    python scripts/verify_public_repo.py --json      # JSON report

Exit code 0 if clean, 2 if any finding (fail-closed).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# This detector's own source necessarily contains the patterns it detects, so it
# exempts itself from the scan. It is static, reviewed code — not data.
_SELF = Path(__file__).resolve()

_TEXT_EXTENSIONS = {
    ".md", ".mdx", ".markdown", ".txt", ".json", ".jsonl", ".yml", ".yaml",
    ".toml", ".csv", ".py", ".ts", ".tsx", ".js", ".html", ".css",
}
_SKIP_PARTS = {".git", "node_modules", ".next", "dist", ".venv", "__pycache__"}

_PATTERNS = [
    ("github_token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[0-9a-zA-Z_]{30,})\b")),
    ("telegram_token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")),
    ("bankr_key_marker", re.compile(r"(?i)bankr[_-]?api[_-]?key")),
    ("aws_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("llm_api_key", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_\-]{20,}\b")),
    ("provider_token", re.compile(r"\babs0_[A-Za-z0-9._~+\-/=]{16,}\b")),
    ("private_key_header", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+\-/=]{12,}\b", re.IGNORECASE)),
    ("local_path", re.compile(r"(/Users/|/private/|/var/folders/|/tmp/|/opt/|/Volumes/|/home/|\bfile:///|\s~/[A-Za-z0-9._\-]+)")),
    ("private_artifact_ref", re.compile(r"(data/private|ip/packages|selected_batch_latest|candidate_salts|private_salt|auth-profiles|wallet\.env|paired\.json|exec-approvals|\.openclaw/secrets|galen/secrets|provider_packet|provider-order|assay[_-]prep|assay[_-]order)")),
    ("wetlab_action", re.compile(r"(?i)(auto_submit|auto_accept_quote|skip_draft|submit_to_provider|provider_submission)[\"']?\s*[:=]\s*[\"']?(?:true|1|yes)")),
    ("scoring_internals", re.compile(r"(?i)\b(BASE_WEIGHTS|scoring_weight|weight_delta_internal)\b")),
    ("embedding_vector", re.compile(r"(?i)embedding.{0,40}\[(?:\s*-?\d+\.\d+\s*,){15,}")),
    ("prompt_leak", re.compile(r"(?i)(SOUL\.md|peptide_generation_prompt|prompts/[A-Za-z0-9_./-]+\.txt|ALLOWED_EXTERNAL_PURPOSES|system prompt\s*:)")),
]
_CRED_ASSIGN = re.compile(
    r"(?i)\b([A-Z0-9_]*(?:API[_-]?KEY|SECRET|ACCESS[_-]?TOKEN|AUTH[_-]?TOKEN|"
    r"CLIENT[_-]?SECRET|WEBHOOK[_-]?SECRET|PRIVATE[_-]?KEY|PASSWORD|PASSWD|"
    r"MNEMONIC|SEED[_-]?PHRASE)[A-Z0-9_]*)\s*[:=]\s*['\"]?([^\s'\"]{8,})"
)
_PLACEHOLDER = re.compile(
    r"(?i)^(?:<.*>|\*+|x{3,}|redacted|none|null|env:|process\.env|"
    r"your[_-].*|example.*|changeme|placeholder|\$\{.*\}|\.\.\.).*$"
)


def iter_files(paths):
    for p in paths:
        if not p.exists():
            continue
        if p.is_file():
            yield p
            continue
        for f in sorted(p.rglob("*")):
            if not f.is_file():
                continue
            if any(part in _SKIP_PARTS for part in f.parts):
                continue
            if f.resolve() == _SELF:
                continue
            if f.suffix.lower() in _TEXT_EXTENSIONS:
                yield f


def scan_line(rel, line_no, line, findings):
    for code, pat in _PATTERNS:
        if pat.search(line):
            findings.append({"file": rel, "line": line_no, "code": code})
    m = _CRED_ASSIGN.search(line)
    if m and not _PLACEHOLDER.match(m.group(2).strip()):
        findings.append({"file": rel, "line": line_no, "code": "credential_assignment"})


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed leak verifier for the public archive.")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    paths = args.paths or [ROOT]
    findings: list[dict] = []
    scanned = 0
    for f in iter_files(paths):
        scanned += 1
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            findings.append({"file": str(f), "line": 0, "code": "unreadable_file"})
            continue
        try:
            rel = f.relative_to(ROOT).as_posix()
        except ValueError:
            rel = str(f)
        for line_no, line in enumerate(text.splitlines(), start=1):
            scan_line(rel, line_no, line, findings)

    report = {"ok": not findings, "scanned_files": scanned,
              "finding_count": len(findings), "findings": findings[:500]}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"public-research verify: scanned {scanned} files, {len(findings)} finding(s)")
        for fnd in findings[:50]:
            print(f"  {fnd['file']}:{fnd['line']} [{fnd['code']}]")
        print("OK" if report["ok"] else "FAILED (fail-closed)")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
