# Publication and security boundaries

- ONLY synthetic test data may be published. Never add BMW/ARRK/internal or real vehicle diagnostic files.
- Never add OpenRouter, NVIDIA, GitHub or Jenkins API keys/tokens, SSH private keys, passwords, or environment dumps.
- This project contains an OpenCode instruction/permission file. These instructions describe desired behavior; independently configured OpenShell sandbox policies are needed to enforce OS/network restrictions.
- OpenRouter routes API requests to an external model provider. A sandbox does not automatically keep model inputs local.
- Treat LLM explanations as suggestions. Ground diagnostic conclusions in protocol specifications and verified test evidence.
- This public package uses a new synthetic offline Python example; the original local `uds_analyzer.py` and `test_uds_analyzer.py` have NOT been copied. Review and sanitize them separately before any publication.
