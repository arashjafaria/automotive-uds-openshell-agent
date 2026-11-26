# Publication and security boundaries

This repository is **public**, and includes both the previously reviewed original Python analyzer and the separately created offline demonstration. It is an educational example using synthetic UDS response data, not a production or safety-certified automotive diagnostic product.

## Data and credentials

- Only synthetic or explicitly approved non-confidential test data should be published. Never add BMW/ARRK/customer logs, internal documents, VINs, trace dumps, or screenshots from company tooling.
- Never commit OpenRouter, NVIDIA, GitHub, Jenkins, or other API keys, passwords, bearer tokens, SSH private keys, certificates, or environment dumps.
- The files `original/uds_analyzer.py` and `original/test_uds_analyzer.py` were manually reviewed and scanned for common secret patterns before their separate public commit. The scan does **not** guarantee the absence of all confidential information.
- Additional fabricated examples appear in `examples/synthetic_uds_responses.csv`, `uds_demo.py`, and `tests/test_uds_demo.py`.

## Agent execution boundaries

- `agents/automotive-uds.md` contains OpenCode instructions and requested tool-use permissions. These do not replace separately enforced OpenShell filesystem and network policies.
- OpenRouter routes API requests to an external model provider. A sandbox does not automatically keep data in the company or on the local machine; only send synthetic or explicitly authorized data.
- Treat LLM explanations as suggestions. Ground diagnostic conclusions in protocol specifications, validated code, and test evidence.
- The repository does not ship a deployable OpenShell sandbox, LLM weights, or a fine-tuned model.

Before every public update, review the complete diff, rerun relevant tests, and rerun `scripts/check_public_safety.py` on files being added. Removing a sensitive file in a later commit does not necessarily remove it from Git history.
