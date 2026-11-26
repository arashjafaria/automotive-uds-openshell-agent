# Publishing safely to your GitHub account

**Account:** `arashjafaria`
**New public repository:** `automotive-uds-openshell-agent`
**Data:** synthetic UDS examples only
**Training claim:** This is an OpenCode/NVIDIA OpenShell *agent configuration*, NOT an LLM trained or fine-tuned by the project owner.

## 1. Publish the reviewed synthetic starter

1. Download this ZIP, extract into Windows Downloads, and copy/move the extracted `automotive-uds-openshell-agent` folder to `~/automotive-uds-openshell-agent` in Ubuntu/WSL2.
2. Open Ubuntu. Make sure your GitHub CLI is logged in (`gh auth status`). Never paste your GitHub token into chat.
3. Run:

```bash
cd ~/automotive-uds-openshell-agent
bash scripts/publish_public.sh
```

The script runs the six tests, checks for common secret patterns, stages **only** the explicitly listed synthetic files, prints the pending file list, and asks you to type `PUBLISH` before creating the PUBLIC GitHub repo. It uses `gh repo create --public` and your existing GitHub authentication. The script does **not** publish the original analyzer files.

Afterward check the new repository: https://github.com/arashjafaria/automotive-uds-openshell-agent

## 2. Recover and review the original local analyzer

The original files from the earlier exercise were reportedly saved in the Ubuntu home directory:

- `~/uds_analyzer.py`
- `~/test_uds_analyzer.py`
- `~/automotive-uds.md`

Run:

```bash
cd ~/automotive-uds-openshell-agent
bash scripts/inspect_local_originals.sh
```

The script copies any existing files into `.private_review/`, which `.gitignore` explicitly excludes. It reports possible credential patterns **without displaying the secret values**. It does not publish or upload those files.

**Before publishing original files:** manually inspect every line for real/customer diagnostic logs, VINs, credentials, or company project details; remove or replace sensitive content; then run tests on the sanitized copies. Publishing cannot be completely undone merely by deleting a later Git commit; the secret may remain in history.

Once confirmed safe, copy **only** sanitized Python source files into `original/`, explicitly stage them with `git add original/uds_analyzer.py original/test_uds_analyzer.py`, review `git diff --cached`, then commit and push. Do not copy raw diagnostic log dumps.

If the original files cannot be located, the synthetic demo remains a standalone, accurate, publicly shareable learning project. Do not claim that its demonstration classifier is the original source code.

## Notes

- This archive includes no API keys, deploy keys, internal customer logs, or VINs.
- `agents/automotive-uds.md` reflects the original agent *instructions*; OpenShell OS/network permissions are configured separately and not bundled as a runnable sandbox image.
- The original code may have different test results; the six passing tests belong to the separate synthetic `uds_demo.py` example.
