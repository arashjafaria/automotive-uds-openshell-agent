# Automotive UDS Log Analysis Agent — OpenShell / OpenCode / Nemotron

**Educational, synthetic-data-only portfolio project.**

This repository documents an exercise in building a specialized automotive diagnostics **AI agent**. It is **not a fine-tuned model**: NVIDIA's pretrained Nemotron model was accessed through OpenRouter. The experiment configured the agent and its tool permissions, while NVIDIA OpenShell isolated the agent application in a sandbox.

## Architecture

```text
User asks to analyze a synthetic UDS log
                  |
                  v
OpenCode custom agent (agents/automotive-uds.md)
    |                  |
    | tool access      | model request
    v                  v
Synthetic CSV/Python   OpenRouter -> NVIDIA Nemotron (hosted)
    |
    v
Local result / evidence -> agent explanation

OpenShell sandbox: protects the execution environment and restricts
file/network access according to the active runtime policy.
```

**Sandbox:** `arash-agent-v2` was the name of the user's learning environment (not included as a deployable container in this repository).

**Original agent configuration:** `agents/automotive-uds.md` is copied from the original exercise output. It names model `openrouter/nvidia/nemotron-3.5-lightning:free`. This service may have availability or quota restrictions; running it requires your own authorized account and credentials. Do **not** put credentials in this repository.

## Files

- `agents/automotive-uds.md`: original OpenCode agent instructions and requested permission settings.
- `original/uds_analyzer.py`: original local UDS response-analysis script, reviewed before public release.
- `original/test_uds_analyzer.py`: four unit tests for the original analyzer.
- `uds_demo.py`: newly written standalone illustrative Python classifier of already reassembled UDS **response payloads**. **Not a reproduction of the original local analyzer.**
- `examples/synthetic_uds_responses.csv`: five fabricated examples, three positive and two negative responses.
- `tests/test_uds_demo.py`: unit tests of the demonstration classifier.
- `SECURITY.md`: publishing and data-boundary notes.

## Run the synthetic offline example

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
python3 uds_demo.py examples/synthetic_uds_responses.csv
PYTHONPATH=original:. .venv/bin/python -m pytest -q
```

The offline Python examples require **no LLM/API key** and make no network requests when analyzing data. With `PYTHONPATH=original:.`, pytest can import both the original analyzer and the standalone demo, and should collect **10 tests** (4 original + 6 demonstration). To run only the demonstration tests, use `.venv/bin/python -m pytest -q tests/test_uds_demo.py`.

## Example results

- `62 F1 90 ...` -> positive response to UDS service `0x22` (ReadDataByIdentifier)
- `7F 22 31` -> negative response to `0x22`, NRC `0x31` Request Out Of Range
- `7F 27 33` -> negative response to `0x27`, NRC `0x33` Security Access Denied

These are **simplified UDS payloads**. This demo does **not** implement CAN/CAN-FD capture, ISO-TP segmentation/reassembly, flashing, ECU access, DTC traceability, or real-vehicle validation.

## What was actually done

1. Used Ubuntu on WSL2 and Docker to work with OpenShell.
2. Configured a sandbox named `arash-agent-v2` and ran OpenCode inside it.
3. Defined a specialized OpenCode agent for synthetic CAN/UDS log analysis.
4. Selected Nemotron through OpenRouter; defined tool-use restrictions and guardrails in the agent instructions.
5. Practiced tool-based log interpretation and security concepts with synthetic examples.

No Nemotron model training, fine-tuning, or trained checkpoint is claimed. Configuration-level permissions do not replace OpenShell runtime policy enforcement.

## Interview summary

> I configured an automotive UDS log-analysis agent using OpenCode, NVIDIA OpenShell sandboxing, and a hosted NVIDIA Nemotron model. I constrained tool access, used synthetic data, and created an offline Python demonstration for classifying positive and negative UDS responses. I did not fine-tune the LLM; my focus was secure agent configuration, tool orchestration and diagnostic interpretation.

## Security and scope

Do not commit passwords, tokens, private keys, internal customer logs, trace dumps, screenshots from company tooling, or confidential vehicle identifiers. Only synthetic examples belong in a public repo. OpenShell protects the **agent process**; external model APIs still receive the request content that is sent to them.

This is a learning project and **not certified for safety-critical automotive use**.

## Publication status and source provenance

This repository combines my original automotive UDS diagnostic analysis project with a separate educational demonstration.

### Original project files
- `original/uds_analyzer.py` — Original Python implementation for analyzing UDS diagnostic responses.
- `original/test_uds_analyzer.py` — Original unit tests (4 tests passed).
- `agents/automotive-uds.md` — OpenCode agent configuration recovered from the original learning exercise and formatted for publication.

### Additional educational demonstration
- `uds_demo.py` — Standalone Python example for interpreting synthetic UDS responses.
- `tests/test_uds_demo.py` — Six automated tests for the demonstration.
- `examples/synthetic_uds_responses.csv` — Fabricated diagnostic data for testing.

### Security and verification
- The original Python files were manually reviewed before publication.
- Automated checks found no common secret patterns.
- All 4 original tests and 6 demonstration tests passed.
- No confidential vehicle logs, credentials, or company data are intentionally included.

### AI model and architecture
This project demonstrates the configuration and use of an automotive diagnostic AI agent using NVIDIA OpenShell, OpenCode, and a pretrained NVIDIA Nemotron model accessed through OpenRouter.

**No LLM was trained or fine-tuned.** The work focused on agent configuration, sandbox security, tool permissions, Python-based diagnostic analysis, and automated testing.

This is an educational engineering project, not a production-ready or safety-certified automotive diagnostic system.
