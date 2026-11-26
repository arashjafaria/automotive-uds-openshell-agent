# Publishing and maintaining this public GitHub repository

**Repository:** https://github.com/arashjafaria/automotive-uds-openshell-agent
**Status:** Published on the `main` branch
**Data policy:** Synthetic educational UDS examples only
**Model claim:** A pretrained NVIDIA Nemotron model was used through OpenRouter; **no LLM training or fine-tuning** was performed.

## What has been published

The initial public commit contained the OpenCode agent configuration, a separate synthetic offline UDS demonstration, six demonstration tests, documentation, and publication scripts.

A later commit added two previously local, manually reviewed Python files:

- `original/uds_analyzer.py` — original UDS response-analysis code.
- `original/test_uds_analyzer.py` — four original unit tests.

These original files are **distinct from** `uds_demo.py` and `tests/test_uds_demo.py`. The latter are additional educational examples, not the original source code. The reviewed public files contain synthetic data rather than raw company traces.

## Verify the published project locally

```bash
cd ~/automotive-uds-openshell-agent
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
PYTHONPATH=original:. .venv/bin/python -m pytest -q
python3 scripts/check_public_safety.py original/ agents/automotive-uds.md
git status --short
```

The expected test suite is **10 passing tests**: four original and six demonstration tests. The secret-pattern scan is not a substitute for a human review.

## Safety checklist for future changes

1. Use only synthetic or explicitly approved, non-confidential data. Never commit actual BMW/ARRK/customer logs, VINs, credentials, private keys, internal configuration, or screenshots from company systems.
2. Review exact changed contents before staging or pushing. In particular, check files in `original/` manually.
3. Run the tests and secret-pattern scanner, then inspect `git diff --cached` (not only `--stat`).
4. Commit and push normal updates with `git push origin main` after review.

The `/original/` entry in `.gitignore` was originally a precaution against accidental publication. Files already tracked in Git remain tracked despite that rule. A new file inside `original/` must be explicitly reviewed and force-added if needed.

**Do not rerun `scripts/publish_public.sh` for updates.** That script is for the initial creation of the GitHub repository, which has already happened.

Git history may retain old contents even after later deletion. If a secret is accidentally published, revoke or rotate the credential immediately and follow a secure Git history-removal process.

## Runtime and model boundaries

`agents/automotive-uds.md` records OpenCode agent instructions and requested tool permissions. It does **not** export a complete, deployable OpenShell sandbox policy or contain model weights. OpenShell runtime restrictions are configured independently. OpenRouter is an external model route, so model requests may leave the sandbox; do not send confidential work data.
