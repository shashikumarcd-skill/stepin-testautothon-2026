# Test Strategy

## 1. Scope

- Application/version:
- In scope: web application, Android application, and supplied integrations
- Out of scope:
- Environments and build identifiers:

## 2. Parallel Delivery Framework

```text
Automation Quest: execute -> failure evidence -> failure classification -> potential-defect lead
																		|
																		v
Bug Quest:        prioritize -> reproduce -> validate evidence -> report -> package
```

This strategy governs Bug Quest work running in parallel with Automation Quest. Automation results are inputs, not automatic defects. Classify every notable failure as `PRODUCT_DEFECT`, `AUTOMATION_DEFECT`, `ENVIRONMENT_FAILURE`, `TEST_DATA_FAILURE`, `LOCATOR_FAILURE`, `SYNCHRONIZATION_FAILURE`, or `UNKNOWN`; only a reproducible, evidence-supported product failure is reported as a defect. A report must identify its module, environment, preconditions, reproduction, expected and actual results, severity, priority, business impact, reproducibility, evidence, logs, screenshot, video where available, Automation Quest reference, classification, and proposed regression coverage.

Working evidence is stored in `../evidence/`. Final approved strategy exports, bug-report exports, requested redacted evidence copies, and the submission manifest are stored in `../output/strategy/`, `../output/bug-reports/`, `../output/evidence/`, and `../output/`. For an automation-originated finding, record its test identifier, run command, environment/build, timestamp, classification, and original path under `../../Automation Quest/output/`, then copy redacted evidence needed for validation into `../evidence/`.

## 3. Quality risks and priorities

| Risk | User/business impact | Likelihood | Priority | Test approach |
| --- | --- | --- | --- | --- |
| Authentication/session failure | Users cannot access accounts | Medium | P0 | Positive, negative, timeout, and session-expiry tests |
| Core transaction/data loss | Revenue and trust impact | Medium | P0 | End-to-end, validation, duplicate-submit, and recovery tests |
| Cross-platform inconsistency | Feature is unusable for target users | High | P1 | Web browser and Android parity checks |
| Accessibility defect | Excludes users and creates compliance risk | Medium | P1 | Keyboard, labels, contrast, focus, and screen-reader checks |
| Privacy/security weakness | Regulatory and trust impact | Low | P0 | Authorization, input handling, session, and exposed-data checks |

## 4. Coverage

| Area | Happy path | Negative/edge cases | Web | Android | Evidence |
| --- | --- | --- | --- | --- | --- |
| Onboarding/authentication | | | | | |
| Primary user journey | | | | | |
| Data creation/editing | | | | | |
| Search/filter/navigation | | | | | |
| Notifications/errors/recovery | | | | | |
| Accessibility | | | | | |
| Security/privacy | | | | | |
| Performance/responsiveness | | | | | |

## 5. Test data

Use unique, disposable test accounts and input values. Do not place real personal data or credentials in test records, screenshots, or AI prompts.

## 6. Entry and exit criteria

- Entry: build and test environment are available; critical accounts and data are prepared.
- Exit: P0 tests executed; reproducible defects logged with evidence; risks and untested areas disclosed; final reports pass validation; reviewed exports and a submission manifest are present in `../output/`.

## 7. Defect triage

Rank severity by user/business impact and priority by urgency. Each defect needs deterministic steps, actual and expected results, environment/build, and redacted evidence. Record the failure classification and Automation Quest test reference when applicable; document why the evidence supports a product defect rather than an automation, locator, data, synchronization, or environment problem. Do not create a report when reproduction or product-defect qualification fails; capture the outcome in the investigation notes instead.

## 8. Reporting And Traceability

Each reported defect must trace to the tested workflow, test data or account state, environment/build, evidence identifiers, and a validated reproduction. Link the detailed Markdown report, worksheet row, Automation Quest lead where applicable, and evidence items. Publish a defect summary, highest-impact defects, recommended regression tests, failure distribution, and business-impact summary in the approved strategy or defect-summary export. Package only reviewed final exports in `../output/`; retain raw or potentially sensitive working material in `../evidence/` with access controls appropriate to the challenge.