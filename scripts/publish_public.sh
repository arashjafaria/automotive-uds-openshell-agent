#!/usr/bin/env bash
# Publish ONLY the audited synthetic starter files, after an explicit local review.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO='arashjafaria/automotive-uds-openshell-agent'
FILES=(README.md SECURITY.md PUBLISHING.md .gitignore requirements-dev.txt agents/automotive-uds.md examples/synthetic_uds_responses.csv tests/test_uds_demo.py uds_demo.py scripts/check_public_safety.py scripts/inspect_local_originals.sh scripts/publish_public.sh)
command -v gh >/dev/null || { echo 'GitHub CLI (gh) missing'; exit 1; }
command -v git >/dev/null || { echo 'Git missing'; exit 1; }
gh auth status >/dev/null || { echo 'Authenticate GitHub CLI first: gh auth login'; exit 1; }
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
python3 scripts/check_public_safety.py "${FILES[@]}"
if [[ ! -d .git ]]; then git init -b main; fi
git add -- "${FILES[@]}"
git diff --cached --check
printf '\nFILES STAGED FOR PUBLICATION:\n'
git diff --cached --stat
printf '\nThis will create the PUBLIC repository: https://github.com/%s\n' "$REPO"
printf 'Only synthetic starter files above will be published, NOT the original local analyzer.\n'
read -r -p 'After reviewing, type PUBLISH to make these files public (anything else cancels): ' answer
[[ "$answer" == 'PUBLISH' ]] || { echo 'Cancelled before publication.'; exit 0; }
git commit -m 'Publish synthetic automotive UDS OpenShell agent project'
gh repo create "$REPO" --public --source=. --remote=origin --push
printf 'Published: https://github.com/%s\n' "$REPO"
