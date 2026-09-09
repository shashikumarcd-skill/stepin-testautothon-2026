# TestAutothon 2026 Quality Engineering Workspace

This workspace contains two connected, independently auditable TestAutothon 2026 solutions:

| Solution | Purpose | Primary deliverables |
| --- | --- | --- |
| [Automation Quest](Automation%20Quest/README.md) | Repeatable Web and Android test automation with diagnostics and execution evidence | Automated tests, HTML/JUnit reports, screenshots, traces, videos, and an intake presentation |
| [Bug Quest](Bug%20Quest/README.md) | Risk-based test strategy and evidence-first product-defect reporting | Test strategy, validated defect reports, redacted evidence, and a reviewed submission package |

The projects work in parallel, but they have distinct ownership:

```text
Automation Quest: execute -> capture evidence -> classify failure -> hand off qualified lead
																																				|
																																				v
Bug Quest:        prioritize -> reproduce -> validate evidence -> report -> package
```

An automated failure is a lead, not automatically a product defect. Bug Quest must reproduce it, verify the expected behavior, confirm the failure is product-related, redact evidence, and document its business impact before reporting it as a defect.

## Workspace Map

```text
Automation Quest/     Web and Android automation framework
	apps/               Supplied Android APKs
	src/                Configuration, intake, presentation, and page objects
	tests/              Web and Android pytest suites
	tools/              Challenge intake and execution utility
	output/             Generated reports and failure evidence

Bug Quest/            Test-strategy and defect-reporting workflow
	data/               Test-data inventory
	docs/               Strategy and AI-use disclosure
	evidence/           Controlled working evidence for investigation
	reports/            Defect templates and validated defect reports
	tools/              Defect-report validation utility
	output/             Reviewed final submission package only
```

## Prerequisites

- Python 3.11 or later
- A challenge-supplied Web URL, test credentials, and test data
- For Web automation: Chromium installed through Playwright
- For Android automation: an Android device or emulator, Appium 2 with the `uiautomator2` driver, and the supplied APK

Create one virtual environment at the workspace root. It can be used by both solutions:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Set-Location "Automation Quest"
pip install -r requirements.txt
playwright install chromium firefox
Copy-Item .env.example .env
```

Configure the local `Automation Quest/.env` file after challenge assets arrive:

```dotenv
WEB_BASE_URL=<challenge-web-url>
WEB_USERNAME=<test-user>
WEB_PASSWORD=<test-password>
ANDROID_APP_PATH=<path-to-supplied-apk>
APPIUM_SERVER_URL=http://127.0.0.1:4723
ANDROID_DEVICE_NAME=<device-or-emulator-name>
ANDROID_PLATFORM_VERSION=<android-version>
```

Do not commit challenge credentials, personal data, or unredacted evidence.

## Use Automation Quest

Automation Quest owns stable, risk-prioritized test execution. Tests express the business journey; page objects in `src/pages/` own UI interactions; runtime setup and evidence capture are handled through configuration and pytest fixtures.

Run these commands from `Automation Quest/`:

```powershell
# Participant-required browser coverage
pytest tests/web -m smoke --browser chromium --browser-channel chrome
pytest tests/web -m smoke --browser firefox
pytest tests/web -m smoke --browser chromium --browser-channel msedge

# Android APK execution; start an Appium server and device/emulator first
pytest tests/android -m smoke

# Full participant-required matrix in one command
python tools/run_required_matrix.py

# Dry run readiness for language support (English + Hinglish)
python tools/dry_run_language_matrix.py

# All available automation tests
pytest tests/
```

At challenge start, intake a supplied `.csv`, `.pdf`, `.txt`, or `.md` requirements/scenario file. The first command extracts reviewable test intent without calling the application; the second runs the selected pytest scope and then generates a presentation.

```powershell
python tools/execute_challenge.py .\challenge-scenarios.csv
python tools/execute_challenge.py .\challenge-requirements.pdf -- -m smoke tests/web
```

Review the generated intent before automating it. The intake summary is planning material, not proof that an application behavior exists.

### Automation Outputs

| Location | Contents | Use |
| --- | --- | --- |
| `Automation Quest/output/reports/` | HTML report, JUnit XML, intake summary, and presentation | Execution summary and machine-readable results |
| `Automation Quest/output/screenshots/` | Failure screenshots | Diagnosis and defect evidence |
| `Automation Quest/output/traces/` | Playwright traces | Reproduction and automation diagnosis |
| `Automation Quest/output/videos/` | Failure videos where retained | Supporting workflow evidence |

Record the exact test name, command, environment/build, timestamp, failure classification, and evidence paths for every issue handed to Bug Quest. A locator fallback can restore an interaction, but the business assertion must still pass for the test to pass.

## Use Bug Quest

Bug Quest owns quality-risk decisions and the final classification of potential defects. Start it while automation runs, using the supplied brief and automation outcomes to prioritize revenue, authentication, data-loss, privacy, blocker, platform, and accessibility risks.

Run these commands from `Bug Quest/`:

```powershell
# Validate that reports in reports/bugs/ contain required sections
python tools/validate_bug_reports.py
```

The normal workflow is:

1. Tailor `docs/test-strategy.md` to the supplied product, build, risks, and available test data.
2. Reproduce the highest-risk journeys and qualified Automation Quest leads with deterministic steps and stated preconditions.
3. Verify expected behavior, classify the failure, redact evidence, and establish business impact.
4. For a reproducible product defect, copy `reports/bug-report-template.md` into `reports/bugs/` and complete it; add a matching row to `reports/bug-report-template.csv` when an Excel/TFS-style import is needed.
5. Run the validator and export only reviewed deliverables to `output/`.

Keep investigation evidence in `Bug Quest/evidence/`, named with a defect identifier such as `BUG-001-login-error.png`. Copy the relevant redacted Automation Quest evidence into this folder rather than relying on a link that may not survive submission.

### Bug Quest Outputs

| Location | Contents | Use |
| --- | --- | --- |
| `Bug Quest/evidence/` | Working, redacted screenshots, logs, recordings, and traces | Investigation and traceability |
| `Bug Quest/reports/bugs/` | Detailed Markdown reports for validated product defects | Source defect records |
| `Bug Quest/output/strategy/` | Approved test-strategy exports | Submission deliverable |
| `Bug Quest/output/bug-reports/` | Approved defect-report exports | Submission deliverable |
| `Bug Quest/output/evidence/` | Requested, approved redacted evidence copies | Submission support |
| `Bug Quest/output/submission-manifest.md` | Final package inventory and limitations | Submission control |

## Evidence, Classification, and AI Use

Use these failure classifications consistently: `PRODUCT_DEFECT`, `AUTOMATION_DEFECT`, `ENVIRONMENT_FAILURE`, `TEST_DATA_FAILURE`, `LOCATOR_FAILURE`, `SYNCHRONIZATION_FAILURE`, and `UNKNOWN`. Only `PRODUCT_DEFECT` findings with reproducible, evidence-supported business impact should become Bug Quest defect reports.

AI may support scenario design, diagnosis, locator candidates, summaries, and report drafting. It must not invent product behavior or defects. Keep a reviewable record of meaningful AI-assisted work in [Automation Quest/docs/ai-use-and-disclosure.md](Automation%20Quest/docs/ai-use-and-disclosure.md) and [Bug Quest/docs/ai-disclosure.md](Bug%20Quest/docs/ai-disclosure.md), including the validation performed.

Before sharing any output, inspect it for secrets, credentials, personal data, and unredacted sensitive material. Open final exports, confirm evidence references resolve, and record known limitations in the submission manifest.

## Submission

- Automation Quest: rename the repository to `TeamName-TestAutothon26-AutomationFramework` and include reviewed execution output for Chrome, Firefox, Edge, and Android from `Automation Quest/output/reports/`.
- Bug Quest: place approved exports in `Bug Quest/output/`, complete the submission manifest, and name the requested deliverables `TeamName_TestAutothon26_TestStrategy` and `TeamName_TestAutothon26_BugReport`.

For project-specific architecture, configuration, and challenge-start details, use the linked README for each solution above.
