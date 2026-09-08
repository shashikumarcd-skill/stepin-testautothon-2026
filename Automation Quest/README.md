# Automation Quest

Contest-ready Python quality-automation framework for web and Android applications. It turns risk-prioritized test intent into repeatable execution, evidence, diagnosis, and an evidence-backed Bug Quest handoff.

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
- A locator fallback utility for simple self-healing, with every fallback logged

## Output And Bug Quest Handoff

Generated execution material belongs in `output/` and may be packaged or shared only after it is reviewed for credentials and personal data:

| Path | Contents | Use |
| --- | --- | --- |
| `output/reports/` | Self-contained HTML and JUnit XML results | Judge-facing execution summary and machine-readable results |
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
playwright install chromium
Copy-Item .env.example .env
```

Set `WEB_BASE_URL` in `.env` when the challenge URL is supplied. For Android, set `ANDROID_APP_PATH` to the supplied `.apk`, start a device/emulator, then run `appium`.

`WEB_USERNAME` and `WEB_PASSWORD` configure the web login tests. The committed example values are the public Practice Test Automation training credentials; use challenge-provided test credentials in your local `.env` and do not commit them.

## Execute

```powershell
pytest tests/web -m smoke
pytest tests/web --headed
pytest tests/android
```

Reports are written to `output/reports/`; screenshots, videos, and traces are written below `output/`. Open `output/reports/report.html`, verify the JUnit totals and evidence links, and retain the exact command and environment details with the run.

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

Rename the repository to `TeamName-TestAutothon26-AutomationFramework` before sharing it. Include the generated execution report under `output/reports/` and state the command, environment, outcome, limitations, and any locator-healing events demonstrated.