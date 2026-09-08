# AI Use and Disclosure

TestAutothon encourages AI when it improves the solution responsibly. AI supports team judgment; it does not replace validation, test execution, or accountable defect reporting.

## Allowed uses in this solution

| Activity | How AI can help | Required human validation |
| --- | --- | --- |
| Test strategy generation and improvement | Identify risk-based journeys, coverage gaps, and prioritization improvements | Compare with the supplied requirements and execute prioritized checks |
| Test scenario and edge-case identification | Propose negative paths, boundaries, state transitions, and cross-platform cases | Review against product behavior and execute selected scenarios |
| Automation framework design | Propose page-object structure, fixtures, configuration, and maintainable test architecture | Review imports, data flow, and maintainability; run targeted tests |
| Automation code generation and refactoring | Draft or improve readable test code, assertions, and utilities | Review every change and run targeted tests before adoption |
| Test data creation | Generate synthetic boundary, invalid, and combinatorial data | Verify business rules and ensure no personal, production, or credential data is used |
| Test failure diagnosis | Analyze trace, video, log, and report patterns to propose likely causes | Inspect the application and prove the diagnosis by rerunning the test |
| Self-healing automation capabilities | Suggest equivalent fallback locators when the primary locator changes | Confirm the fallback identifies the same user-facing control and preserve logged evidence |
| Accessibility, security, performance, and visual analysis | Propose authorized test ideas and help analyze evidence | Use authorized environments only; reproduce findings and assess actual impact |
| Test result summarization | Summarize JUnit/HTML reports, results, and execution evidence | Compare summaries with raw artifacts and correct unsupported conclusions |
| Dashboards and execution insights | Identify trends, failure clusters, and useful report views | Verify all metrics and conclusions against the underlying execution data |
| Defect analysis and business-impact estimation | Analyze defect scope and propose evidence-based impact statements | Validate the defect and distinguish verified facts from estimates |
| Bug description and repro-step improvement | Improve titles, deterministic repro steps, expected results, and observed results | Reproduce the defect and confirm the report contains no speculation |
| Product recommendations | Suggest product improvements based on validated test evidence | Ground recommendations in verified findings and clearly label them as recommendations |

## Mandatory operating rules

1. Never provide passwords, OTPs, access tokens, personal data, proprietary source, private screenshots, or unredacted logs to public AI tools.
2. Treat AI output as an untrusted draft. Read it, understand it, and validate it against the supplied application before committing it or submitting it.
3. Keep tests deterministic. AI must not be used to conceal failures, bypass controls, weaken assertions, or invent evidence.
4. Keep only verified locator fallbacks. The framework logs fallback selection so the team can review locator drift.
5. Retain execution evidence for claims made in reports: test command, build/environment, screenshots, traces, video, logs, and JUnit/HTML output as appropriate. Store generated execution material under `output/` and transfer only redacted, relevant items to Bug Quest evidence.
6. Be ready to explain the tool/model, task, prompt sequence, output adopted, review method, defects or hallucinations found, and measured benefit to the judges.

## Disclosure log

Complete one row for each meaningful AI-assisted activity. Store only sanitized prompt excerpts and references.

| Date/time | Team member | Tool/model | Task | Sanitized prompt/reference | Output adopted | Review and execution evidence | Errors/limits found | Time saved or improvement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## Suggested contest flow

1. Use AI to draft a risk inventory and candidate test scenarios after the challenge artifacts arrive.
2. Assign validated web and Android scenarios to the corresponding automation agent/workstream.
3. Use AI to propose implementation or diagnosis only with sanitized inputs.
4. Review the output, run the narrowest test, inspect evidence, and log the result.
5. Before submission, reconcile the disclosure log with the final code, reports, and execution artifacts.