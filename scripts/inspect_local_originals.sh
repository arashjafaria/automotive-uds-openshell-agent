#!/usr/bin/env bash
# Stage pre-existing source code on the user's own Ubuntu, privately, for review.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .private_review
for f in uds_analyzer.py test_uds_analyzer.py automotive-uds.md; do
  if [[ -f "$HOME/$f" ]]; then
    cp -- "$HOME/$f" ".private_review/$f"
    printf 'Found and staged privately: %s\n' "$HOME/$f"
  else
    printf 'Not found: %s\n' "$HOME/$f"
  fi
done
if compgen -G '.private_review/*' > /dev/null; then
  python3 scripts/check_public_safety.py .private_review || true
  echo 'Review .private_review manually BEFORE copying any original files to the public repository.'
  echo 'This private review folder is ignored by Git and is never published by publish_public.sh.'
else
  echo 'None of the original files were found in your Ubuntu home directory.'
fi
