# Jenkins CI — Automotive UDS Log Analysis Agent

This project has a **Jenkins Pipeline as Code** file in `Jenkinsfile`. It reuses the locally installed Jenkins controller and Python Docker agent originally built for a separate, educational **AEB validation** project.

**Important distinction:** The earlier AEB Jenkins pipeline was successfully executed (17 AEB tests, 100% measured AEB coverage, a 95% AEB coverage quality gate, and JUnit/coverage artifacts). This new **UDS** pipeline is a separate job and is **not yet verified by an actual Jenkins build**. Its results must be recorded after the first run. Do not attribute the AEB coverage percentage to the UDS analyzer.

## Prerequisites

- Ubuntu on WSL2 with Docker running.
- Existing Jenkins controller `jenkins-learning` available at `http://localhost:8080`.
- Existing Docker Jenkins agent `python-aeb-worker` online in Jenkins as `python-aeb-agent`.
- Its existing label: `aeb-python`. The current `Jenkinsfile` uses that label to avoid changing or recreating the agent.
- Python 3 and `python3 -m venv` available on the agent.
- Network access from Jenkins and its agent to **public GitHub** and to Python package indexes for the Setup stage.

## Create a new, independent Jenkins Pipeline job

1. Open `http://localhost:8080` on your own computer.
2. Select **New Item** → **Pipeline**, and name it `UDS-Validation-Pipeline`.
3. Set **Definition** to **Pipeline script from SCM**.
4. Select **SCM: Git**.
5. Set **Repository URL** to:

   `https://github.com/arashjafaria/automotive-uds-openshell-agent.git`

6. Select **Credentials: - none -** (this repository is public; do not reuse the read-only SSH deploy key for the private AEB repository).
7. Set **Branch Specifier** to `*/main`; **Script Path** to `Jenkinsfile`. Keep **Lightweight checkout** enabled when available.
8. Save and click **Build Now** **once** for the initial verification. The `Jenkinsfile` includes the SCM polling trigger `H/5 * * * *` for later commits, while the local controller is running.
9. Open **Console Output**, **Test Result**, and **Build Artifacts** for that build.

This does **not** change, overwrite, or delete `AEB-Validation-Pipeline` or `AEB-Validation-Tests`.

## Pipeline stages and responsibilities

| Stage | What it does |
|---|---|
| Checkout | Clears only this job's workspace and checks out the public repository. |
| Setup | Creates a fresh workspace-local `.venv` and installs pinned-range development dependencies from `requirements-dev.txt`. |
| Security Scan | Checks named synthetic source files for common credential patterns; this does not prove the absence of all secrets. |
| UDS Unit Tests | Runs **4 original** and **6 demonstration** unit tests, publishes JUnit XML and collects statement/branch coverage for both Python modules. |
| Synthetic Reports | Produces a report from `examples/synthetic_uds_responses.csv` and another report from the original built-in synthetic samples. |

The expected count is **10 collected tests** if both test files still contain their current four and six tests. The exact UDS coverage percentage is **not yet verified**; **no UDS coverage threshold has been imposed**. After measuring coverage in Jenkins, consider a justified threshold rather than copying the unrelated 95% value from AEB.

Archived artifacts:

- `test-results.xml` is published through Jenkins's **JUnit Test Result** UI.
- `coverage.xml` is archived under **Build Artifacts**.
- `reports/synthetic_uds_summary.txt` and `reports/original_uds_summary.txt` are archived under **Build Artifacts**.

The code does **not** download model weights, query Nemotron/OpenRouter, read a real vehicle log, operate an ECU, or claim to certify automotive software. These checks cover only offline synthetic UDS parsing code. OpenShell agent sandbox policy must be validated separately.

## Run the same unit tests locally

```bash
cd ~/automotive-uds-openshell-agent
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
PYTHONPATH=original:. .venv/bin/python -m pytest -v \
  tests/test_uds_demo.py original/test_uds_analyzer.py \
  --junitxml=test-results.xml \
  --cov=uds_demo --cov=uds_analyzer --cov-branch \
  --cov-report=term-missing --cov-report=xml:coverage.xml
```

The generated reports and virtual environment should not be committed to Git. GitHub-hosted CI is not required: this Jenkins instance runs locally, with no paid cloud runner.

## Troubleshooting

- **Agent unavailable:** in **Manage Jenkins → Nodes**, verify `python-aeb-agent` is online and has the `aeb-python` label. Do not delete the working agent.
- **Git checkout permission error:** verify you used the public **HTTPS** repository URL with no credentials, not the AEB-only SSH deploy key.
- **Missing Python packages:** inspect the Setup stage and `requirements-dev.txt`. Do not modify the agent's global Python environment.
- **ModuleNotFoundError for `uds_analyzer`:** verify the test command includes `PYTHONPATH=original:.` and the tracked original files were checked out.
- **No JUnit test report:** investigate the earliest failure. The Test stage rejects a missing JUnit report.
- **Polling does not run:** Jenkins must be running; check the job's Git Polling Log. `H/5 * * * *` schedules a check approximately every five minutes and triggers a build when changes are detected.
- **Cost:** the tools and local workflow use no paid API or cloud compute. Normal internet access and your machine's own resources are still required.

## Interview explanation

> I had already built a separate local Jenkins Controller/Agent CI setup for a Python AEB simulator. For this public UDS project, I version-controlled an additional Jenkinsfile that reuses the Python agent, performs a public GitHub checkout, installs a clean test environment, runs original and synthetic UDS unit tests, publishes JUnit and code-coverage data, and archives synthetic reports. The UDS job must be executed and its actual result verified before describing it as operational. The AI-agent side (OpenShell/OpenCode/Nemotron) and the deterministic offline Python CI checks are distinct parts of the portfolio.
