#!/usr/bin/env python3
"""Conservative public-repository secret checks; not a substitute for human review."""
from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "private key block": re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC |DSA |.* )?PRIVATE KEY-----"),
    "common API/token prefix": re.compile(r"(?:nvapi-|github_pat_|gh[pousr]_|glpat-|sk-(?:proj-)?)[A-Za-z0-9_-]{10,}"),
    "authorization bearer token": re.compile(r"(?i)authorization\s*[:=]\s*[\"']?bearer\s+\S{12,}"),
    "secret-like assignment": re.compile(r"(?i)\b(?:api_key|secret_key|private_key|access_token|auth_token)\s*[:=]\s*[\"'](?!example|placeholder|your_)[A-Za-z0-9/+=_.:-]{16,}[\"']"),
}

SKIP = {".git", ".venv", "__pycache__", ".pytest_cache"}
ALLOWED_EXTENSIONS = {".py", ".md", ".csv", ".txt", ".yml", ".yaml", ".toml", ".json", ".sh", ".gitignore"}


def files_from_args(args: list[str]):
    for arg in args:
        p = Path(arg)
        if not p.exists():
            raise FileNotFoundError(p)
        if p.is_file():
            yield p
        else:
            for f in p.rglob("*"):
                if f.is_file() and not any(s in SKIP for s in f.parts):
                    yield f


def main():
    if len(sys.argv) <= 1:
        print("Usage: python3 scripts/check_public_safety.py PATH [PATH ...]")
        sys.exit(2)
    findings = []
    for f in sorted(set(files_from_args(sys.argv[1:]))):
        if f.suffix not in ALLOWED_EXTENSIONS and f.name != ".gitignore":
            findings.append(f"{f}: unexpected file type; inspect manually")
            continue
        try:
            contents = f.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            findings.append(f"{f}: non-text/unreadable file; inspect manually")
            continue
        for number, line in enumerate(contents.splitlines(), start=1):
            for name, rx in PATTERNS.items():
                if rx.search(line):
                    findings.append(f"{f}:{number}: possible {name}")
    if findings:
        print("PUBLICATION BLOCKED — review findings (secret values are not printed):")
        for finding in findings:
            print(" -", finding)
        sys.exit(1)
    print("No common secret patterns detected. Manual review is still required.")


if __name__ == "__main__":
    main()
