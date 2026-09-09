# Bug Quest

Structured documentation and evidence workflow for the TestAutothon Bug Quest. It turns the challenge brief, exploratory observations, and Automation Quest results into credible test strategy, reproducible defect reports, and a clean submission package.

This framework is aligned to the participant challenge guidance: use AI to improve the test strategy, use AI to improve bug-report quality, and publish outputs using the required naming convention.

## Parallel Framework Workflow

```text
Automation Quest: execute -> capture failure evidence -> classify -> hand off qualified leads
                                                                   |
                                                                   v
Bug Quest:        prioritize -> reproduce -> validate evidence -> report -> package
```

Run Bug Quest alongside Automation Quest from the start of the challenge. Use the strategy to decide what to test first: P0 for revenue, authentication, data-loss, privacy, or blockers; P1 for major workflow, platform, or accessibility risk; P2 for lower-impact improvements. A failed automated test is a lead, not a defect, until Bug Quest reproduces it and validates evidence that supports a product failure.

### Decision gates

1. **Prioritize:** select a workflow based on documented business risk, coverage gaps, or an Automation Quest lead.
2. **Reproduce:** use deterministic steps, stated preconditions, and the recorded build/environment; record a non-reproduction as an investigation outcome, not a bug.
3. **Validate evidence:** classify the failure, verify expected behavior against supplied requirements, redact evidence, and establish business impact.
4. **Report:** create a detailed report only when classification is `Product defect` and the evidence supports that conclusion.
5. **Package:** export reviewed material only to `output/`; retain controlled working evidence in `evidence/`.

## Deliverables

- `docs/test-strategy.md`: tailor this strategy to the supplied application
- `reports/bug-report-template.md`: a repeatable evidence-first defect report
- `reports/bug-report-template.csv`: an Excel-compatible defect worksheet for TFS or other test-management imports
- `reports/bugs/`: one Markdown file per validated defect
- `data/test-data-catalog.csv`: a starting test-data inventory
- `tools/validate_bug_reports.py`: verifies mandatory report sections
- `output/strategy/`: approved strategy exports
- `output/bug-reports/`: approved report exports
- `output/evidence/`: approved, redacted evidence copies only when requested
- `output/submission-manifest.md`: final package inventory; do not treat `output/` as raw working evidence

## Evidence And Automation Quest Integration

`evidence/` is the working evidence store. Keep redacted screenshots, recordings, logs, and exported traces there using a defect identifier, for example `evidence/BUG-001-login-error.png`. `output/` is the submission package: place final PDF/Word/Excel exports, approved report copies, and a manifest there only after review.

When Automation Quest identifies a potential product defect, retain the exact test identifier, command, environment/build, classification, failure message, timestamp, and source path under `../Automation Quest/output/`. Copy only relevant redacted evidence into `evidence/`; do not rely on a link that may not survive submission. Bug Quest must independently reproduce the behavior, validate the expected outcome, classify the cause, and state the business impact. Treat `AUTOMATION_DEFECT`, `ENVIRONMENT_FAILURE`, `TEST_DATA_FAILURE`, `LOCATOR_FAILURE`, and `SYNCHRONIZATION_FAILURE` as investigation outcomes, not product defects.

## Setup

Python 3.11 or later is required only for report validation.

All necessary challenge artefacts and resources are deployed at the beginning of the challenge. Participants should arrive with their skills, a working laptop, and competitive spirit; tailor the strategy and reports after the organizers provide the application details and test assets.

```powershell
# From the workspace root; this environment is shared by both quests.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Set-Location "Bug Quest"
```

No third-party package installation is necessary.

## Workflow

1. Update `docs/test-strategy.md` with the supplied product brief and build details while Automation Quest prepares execution.
2. Prioritize and reproduce the highest-risk journeys and Automation Quest leads.
3. Validate expected behavior, final classification, evidence redaction, traceability, and business impact before writing a report.
4. Copy `reports/bug-report-template.md` only for a reproducible, evidence-supported product defect.
5. Open `reports/bug-report-template.csv` in Excel, add one row per validated defect, and map its columns to the destination system's bug fields during import. Retain the Markdown report as the detailed evidence record; link it from `Evidence Links` where permitted.
6. Store redacted screenshots, video, and logs in `evidence/`; cite each item from the Markdown report and worksheet.
7. Validate reports before submission:

```powershell
python tools/validate_bug_reports.py
```

8. Export the strategy and reports to Word, PDF, or Excel as requested by organizers. Place approved strategy exports in `output/strategy/`, approved reports in `output/bug-reports/`, requested redacted evidence copies in `output/evidence/`, and complete `output/submission-manifest.md`.

## AI-first Strategy And Report Workflow

1. Use AI to draft and improve `docs/test-strategy.md` from product context, risk model, and known dependencies.
2. Validate AI output against actual product behavior and challenge constraints.
3. Use AI to improve reproducibility language, business-impact framing, and remediation suggestions in bug reports.
4. Keep the final decision human-reviewed and evidence-backed for every claim.
5. Record meaningful prompts, models, validations, and limitations in `docs/ai-disclosure.md`.

## Naming Convention Packaging

Create the final named deliverables required by the challenge:

- `TeamName_TestAutothon26_TestStrategy`
- `TeamName_TestAutothon26_BugReport`

Use this utility after your final exports are approved:

```powershell
python tools/package_deliverables.py --team-name Aura --strategy-source docs/test-strategy.md --bug-report-source reports/bugs/BUG-001.md
```

The utility copies files to:

- `output/strategy/TeamName_TestAutothon26_TestStrategy.<ext>`
- `output/bug-reports/TeamName_TestAutothon26_BugReport.<ext>`

## Output Package

Use `output/` only for reviewed final deliverables. `output/submission-manifest.md` identifies each delivered file, its source, build/environment coverage, validation date, final classification, and known limitations. Before upload, open every export, validate Markdown reports, confirm all evidence references resolve, and remove secrets, credentials, and personal data.

## AI disclosure

Record AI use in `docs/ai-disclosure.md`: model/tool, task, relevant prompt, output used, review method, errors found, and benefit. The log explicitly covers strategy and scenario design, test data, test-failure diagnosis, accessibility/security/performance/visual analysis, result summaries, dashboards, defect analysis, bug-report improvements, and product recommendations. Do not send credentials, personal data, proprietary information, or unredacted evidence to public AI tools.

## Submission

Rename deliverables to `TeamName_TestAutothon26_TestStrategy` and `TeamName_TestAutothon26_BugReport`, place the approved files in `output/`, and upload them to the team folder provided by organizers.