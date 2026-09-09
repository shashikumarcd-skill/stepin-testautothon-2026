# Automation Quest

Contest-ready Python quality-automation framework for web and Android applications. It turns risk-prioritized test intent into repeatable execution, evidence, diagnosis, and an evidence-backed Bug Quest handoff.

This framework is aligned to the TestAutothon Participants Challenge requirement that the workflow automation runs on Chrome, Firefox, and Edge, and that the same business scenarios are executable against the Android APK path.

## Framework Workflow

```text
Discover application and supplied artefacts
	-> Prioritize business-risk workflows
	-> Automate stable web and Android journeys
	-> Capture evidence and classify failures
	-> Validate safe locator fallback where needed
	-> Summarize execution and recommend next coverage
	-> Hand supported potential product defects to Bug Quest
```

| Layer | Responsibility | Current location |
| --- | --- | --- |
| Test intent | Risk tags, business assertions, test data, and smoke selection | `tests/` |
| Interaction | Explicit waits and readable application actions | `src/pages/` |
| Runtime | Environment configuration, browser/device lifecycle, and artifact setup | `src/config.py`, `tests/conftest.py` |
| Intelligence and evidence | Locator fallback events, reports, screenshots, traces, and video | `src/`, `output/` |

Keep test intent separate from page or screen mechanics. A healed locator only restores an interaction; the workflow passes only after its business assertion succeeds. Classify each failure as product, automation, environment, test-data, locator, synchronization, or unknown before it can be considered for Bug Quest.

## What is included

- Web UI tests using pytest and Playwright
- Android native/mobile-web test seam using pytest and Appium
- Page objects, configuration, test data, and reusable assertions
- HTML/JUnit reports plus screenshots, traces, and video for failed web tests
- Boundary and negative login coverage using reviewed, synthetic test data
- Accessibility, performance, and client-side security quality gates
- Explainable failure classification, confidence-scored locator-healing evidence, and risk-based next-test recommendations
- A unified HTML/JSON quality dashboard for browser, platform, and quality-gate decisions

## Output And Bug Quest Handoff

Generated execution material belongs in `output/` and may be packaged or shared only after it is reviewed for credentials and personal data:

| Path | Contents | Use |
| --- | --- | --- |
| `output/reports/` | Self-contained HTML and JUnit XML results | Judge-facing execution summary and machine-readable results |
| `output/reports/quality-dashboard.html` | Unified cross-browser quality, risk, healing, and next-action view | Business-intelligence briefing for judges and triage |
| `output/reports/failure-classifications-*.json` | Deterministic categories and evidence reasons for test failures | Separate product-risk from environment and automation issues |
| `output/reports/healing-events.json` | Fallback selector, confidence, and semantic-validation telemetry | Review locator drift without masking failed business assertions |
| `output/reports/quality-check-results.json` | Accessibility, performance, and security gate observations | Quality evidence; warnings require review before submission |
| `output/screenshots/` | Failure screenshots | Evidence for diagnosis and validated defect reports |
| `output/traces/` | Playwright traces | Reproduction and automation-failure diagnosis |
| `output/videos/` | Retained failure video | Workflow evidence where available |

Do not create a defect simply because a test failed. For a potential product defect, copy relevant redacted material into `../Bug Quest/evidence/`, draft and validate the report in `../Bug Quest/reports/bugs/`, then place only the approved export in `../Bug Quest/output/bug-reports/`. Record the automation test name, command, environment, failure classification, exact evidence paths, and business impact supported by the reproduction.

## Automation agents and AI use

Use the workspace agents in `.github/agents/` to assign work cleanly:

- `Web Automation Specialist`: Playwright page objects, web tests, accessibility, and browser evidence.
- `Android Automation Specialist`: Appium, device setup, native/mobile-web tests, and device evidence.

The responsible-AI workflow and mandatory disclosure table are in [docs/ai-use-and-disclosure.md](docs/ai-use-and-disclosure.md). Complete it for every meaningful AI-assisted activity and retain the corresponding validation evidence.

## Setup

All necessary challenge artefacts and resources are deployed at the beginning of the challenge. Participants should arrive with their skills, a working laptop, and competitive spirit; configure this framework only after the organizers provide the application details and test assets.

```powershell
# From the workspace root; this environment is shared by both quests.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Set-Location "Automation Quest"
pip install -r requirements.txt
playwright install chromium firefox
Copy-Item .env.example .env
```

Set `WEB_BASE_URL` in `.env` when the challenge URL is supplied. The default example points to the required staging host `https://stg.gajab.com/`.

For Android, set `ANDROID_APP_PATH` to the supplied `.apk`, start a device/emulator, then run `appium`.

Set `GAJAB_MOBILE_NUMBER` and `GAJAB_EMAIL_RECIPIENT` only in a local `.env` using event-authorized data. The default OTP is `123456`, but it is still externalized so the test suite never requires a hard-coded secret. The supplied Android setup is verified for `Pixel_9a`, `emulator-5554`, Android 17, and `com.gajab.buyerstore`.

## Execute

```powershell
# Required browser coverage
pytest tests/web -m smoke --browser chromium --browser-channel chrome
pytest tests/web -m smoke --browser firefox
pytest tests/web -m smoke --browser chromium --browser-channel msedge

# Android APK coverage for the same scenario set (by scenario IDs and acceptance checks)
pytest tests/android -m smoke

# One command for the full participant-required matrix
python tools/run_required_matrix.py

# Run Top 2 quality gates and expanded negative/boundary coverage
pytest tests/web/test_login_edge_cases.py tests/web/test_quality_gates.py --browser chromium --browser-channel chrome

# Dry run challenge readiness for required languages (no real browser/device execution)
python tools/dry_run_language_matrix.py
```

Reports are written to `output/reports/`; screenshots, videos, and traces are written below `output/`. Open `output/reports/report.html`, verify the JUnit totals and evidence links, and retain the exact command and environment details with the run.

The matrix runner generates per-target report files:

- `output/reports/report-chrome.html`, `output/reports/junit-chrome.xml`
- `output/reports/report-firefox.html`, `output/reports/junit-firefox.xml`
- `output/reports/report-edge.html`, `output/reports/junit-edge.xml`
- `output/reports/report-android.html`, `output/reports/junit-android.xml`
- `output/reports/quality-dashboard.html`, `output/reports/quality-dashboard.json`

Dry-run language matrix output files:

- `output/reports/report-dryrun-web-english.html`, `output/reports/junit-dryrun-web-english.xml`
- `output/reports/report-dryrun-android-english.html`, `output/reports/junit-dryrun-android-english.xml`
- `output/reports/report-dryrun-web-hinglish.html`, `output/reports/junit-dryrun-web-hinglish.xml`
- `output/reports/report-dryrun-android-hinglish.html`, `output/reports/junit-dryrun-android-hinglish.xml`

## Competition-Start Intake And Presentation

At the competition start, provide one requirements or scenario file in `.csv`, `.pdf`, `.txt`, or `.md` format. The intake command records the source filename and SHA-256 hash, extracts reviewable test intent, runs the chosen pytest scope, and creates `output/reports/quality-presentation.pptx` from the input and JUnit results.

```powershell
# Safely intake the supplied intent without calling the application.
python tools/execute_challenge.py .\challenge-scenarios.csv

# Execute the verified P0 web scope and regenerate the presentation afterward.
python tools/execute_challenge.py .\challenge-requirements.pdf -- -m smoke tests/web
```

The generated `output/reports/input-summary.json` is a planning artifact, not executable automation. Review every extracted requirement against the application, then use the Scenario Intake and Quality Planner agent to produce risk-ranked coverage and hand verified journeys to the Web or Android specialist. This keeps AI useful for most analysis and drafting work while retaining human validation for test intent, locators, assertions, failure classification, and Bug Quest promotion.

The output contract remains fixed: HTML, JUnit XML, the generated presentation, and derived intake records go in `output/reports/`; failure evidence stays in `output/screenshots/`, `output/traces/`, and `output/videos/`. Keep the original requirement file outside `output/`, and place only reviewed final Bug Quest material under `../Bug Quest/output/`.

## Quality Intelligence

The framework applies deterministic rules to test failure evidence. It labels likely product, automation, environment, test-data, locator, synchronization, or unknown causes and always retains the matching reason. These labels prioritize review; they do not prove root cause or create Bug Quest defects automatically.

`quality-dashboard.html` merges execution totals, failure categories, quality-gate outcomes, and locator-healing telemetry. Its risk score is a prioritization signal, not a release decision. A skipped Android run is displayed as unverified platform coverage. Review warnings and raw artifacts before presenting results.

## Challenge-start checklist

1. Review the supplied application details, credentials, test data, and other challenge artefacts.
2. Put the supplied APK in `apps/` and update `.env`.
3. Replace `HomePage` locators with application-under-test locators.
4. Add focused page objects and user-journey tests.
5. Keep test data free of credentials and personal data.
6. Record locator fallback events and validate every AI-assisted change.
7. Review `output/` for secrets or personal data before sharing evidence.
8. Hand off only reproducible, evidence-supported potential product defects to Bug Quest.

## Submission

Rename the repository to `TeamName-TestAutothon26-AutomationFramework` before sharing it.

Include reviewed execution outputs from all required runs (Chrome, Firefox, Edge, and Android) under `output/reports/`, and state the command, environment, outcome, limitations, and any locator-healing events demonstrated.