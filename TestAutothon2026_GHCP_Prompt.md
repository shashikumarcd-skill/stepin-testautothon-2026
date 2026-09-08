# TestAutothon 2026 — GitHub Copilot Prompt

## Objective

Build a competition-grade, production-quality, highly demonstrable automation and quality-engineering solution for **TestAutothon 2026**.

The goal is **not** to create a generic automation framework.

The goal is to maximize the probability of reaching the **Top 8** and winning the **Automation Quest**, while also producing evidence that strengthens the **Bug Quest** submission.

---

# 1. Challenge Context

The official challenge document states:

- Contest covers **Web and Mobile (Android) Automation**.
- Teams build a robust automation framework and a comprehensive test strategy that identifies meaningful product defects.
- Recommended time split within the 5-hour solution window:
  - **Automation Quest — 3 hours**
  - **Bug Quest — 2 hours**
- Teams may divide into smaller groups and work on both challenges in parallel.
- Automation Quest is judged by the **STeP-IN Jury**.
- Bug Quest is judged by the **Platform Hosting Team**.
- Teams are expected to participate in both tracks.

The judging priorities are:

1. The automated workflow must work.
2. Quality of solution.
3. Quality of teamwork.
4. AI Innovation & Impact.
5. X-Factor — something genuinely innovative and unexpected.

AI is strongly encouraged for:

- Test strategy generation
- Test scenarios and edge cases
- Automation framework design
- Automation code generation/refactoring
- Test data generation
- Test failure diagnosis
- Self-healing automation
- Accessibility analysis
- Security analysis
- Performance analysis
- Visual analysis
- Test result summarization
- Dashboards and execution insights
- Defect analysis and business impact
- Bug description/reproduction improvement
- Product recommendations

AI usage alone does not guarantee additional points. AI must make the solution meaningfully better.

All AI-generated work must be reviewed and validated.

---

# 2. Winning Product Vision

Build:

## **AI-Powered Autonomous Quality Engineering Framework**

The framework should go beyond:

`Test → Execute → Report`

and implement:

`DISCOVER → GENERATE → AUTOMATE → HEAL → DIAGNOSE → ANALYZE → REPORT → RECOMMEND`

The core message for the jury should be:

> **Automation that doesn't just execute tests — it understands failures, heals safely, explains quality risks, and helps the tester decide what to test next.**

## Quest Deliverable Framework

Treat the two quests as connected but independently auditable deliverables:

```text
Automation Quest: discover -> automate -> execute -> capture -> classify -> analyze
                                                               |
                                                               v
Bug Quest:        prioritize -> reproduce -> validate evidence -> report -> package
```

Automation Quest owns repeatable web/Android execution and its generated material in `Automation Quest/output/`. Bug Quest owns risk strategy, defect validation, redacted working evidence in `Bug Quest/evidence/`, and reviewed submission exports in `Bug Quest/output/`. An automation failure is never a defect by itself: its evidence must be reproduced, classified, and linked to a business impact before Bug Quest reports it as a potential product defect.

Each output item must be traceable to its source test or exploratory session, command, environment/build, timestamp, and validation status. Review all output for credentials, personal data, and other sensitive material before sharing it.

---

# 3. DISCOVER

The framework should:

- Understand the actual challenge application.
- Inspect available web/mobile screens and controls.
- Identify critical workflows.
- Identify available test data.
- Understand environment constraints.
- Identify risk areas.
- Reuse all provided challenge artefacts.

IMPORTANT:

Do not invent application locators, screens, APIs, test data, or workflows before the actual challenge application and challenge artefacts are provided.

First inspect:

- Repository
- Challenge files
- Application type
- Web/mobile components
- Available test environment
- Existing code
- Dependencies
- Execution commands
- Constraints

---

# 4. GENERATE

Generate meaningful tests, not hundreds of meaningless tests.

Include:

- Smoke scenarios
- Critical business flows
- Positive scenarios
- Negative scenarios
- Boundary scenarios
- Invalid inputs
- Empty values
- Duplicate actions
- Navigation
- Session behaviour
- State transitions
- Error handling
- Accessibility
- Visual consistency
- Performance observations
- Security-oriented input validation where appropriate
- Mobile-specific behaviour
- Orientation/responsive behaviour where practical
- Interruption/recovery scenarios where practical

Prioritize scenarios by **business risk**.

---

# 5. AUTOMATE

Build stable Web and Android automation where applicable.

Preferred technologies if compatible with the challenge environment:

- Playwright for Web
- Appium 2 for Android
- Java or Python
- Pytest or TestNG depending on selected language
- Allure or lightweight custom HTML reporting
- JSON/YAML configuration
- Structured logging
- Screenshots
- Video where practical
- GitHub Actions if useful

Do not force a technology if another option is more reliable in the challenge environment.

---

# 6. Architecture

Use clean separation of responsibilities.

Suggested structure:

```text
tests/
pages/
screens/
components/
core/
drivers/
config/
data/
utils/
listeners/
healing/
ai/
analysis/
reporting/
artifacts/
docs/
```

Separate:

- Test intent
- Page/screen interactions
- Driver management
- Synchronization
- Assertions
- Evidence collection
- AI services
- Healing
- Reporting

---

# 7. AI Architecture

Create an AI abstraction layer.

Conceptually:

```text
AIProvider
 ├── analyzeFailure()
 ├── suggestLocator()
 ├── generateTestScenarios()
 ├── classifyFailure()
 ├── summarizeExecution()
 └── analyzeDefect()
```

Requirements:

- Provider-independent architecture.
- No hardcoded API keys.
- Use environment variables.
- Provide deterministic fallback behaviour.
- Core automation must continue working when external AI is unavailable.
- Never fabricate product behaviour or defects.

---

# 8. Self-Healing Automation

Implement practical self-healing, not marketing-only self-healing.

When a locator fails:

1. Capture the failure.
2. Capture DOM/UI metadata.
3. Generate safe candidate locators.
4. Validate candidate locators.
5. Use confidence scoring.
6. Continue only when confidence is sufficient.
7. Record:
   - Original locator
   - Healed locator
   - Strategy
   - Confidence
   - Timestamp
8. Report the healing event separately.

CRITICAL RULE:

A healed locator does NOT automatically mean the test passed.

The business assertion must still execute.

Example:

```text
Original locator fails
        ↓
Candidate locators generated
        ↓
Candidate validated
        ↓
Locator healed
        ↓
Action executed
        ↓
Business assertion executed
        ↓
Pass → Test passes + healing event recorded
Fail → Genuine functional failure remains
```

The report must clearly distinguish:

- Locator healed
- Business assertion passed
- Business assertion failed

Never use healing to hide a genuine product defect.

---

# 9. Failure Diagnosis

Classify failures into:

```text
PRODUCT_DEFECT
AUTOMATION_DEFECT
ENVIRONMENT_FAILURE
TEST_DATA_FAILURE
LOCATOR_FAILURE
SYNCHRONIZATION_FAILURE
UNKNOWN
```

Capture:

- Screenshot
- Logs
- Page/screen state
- Error details
- Test name
- Step
- Timestamp
- Environment
- Relevant evidence

AI may assist with diagnosis, but the result must remain explainable and validated.

---

# 10. Quality Intelligence

Add:

## Accessibility

Where practical, check:

- Labels
- Roles
- Keyboard/focus behaviour
- Basic accessibility attributes

## Visual Analysis

Where practical:

- Screenshot comparison
- Layout anomalies
- Missing elements
- Visual regression observations

## Performance

Capture practical timing information such as:

- Page load timing
- Critical action timing
- API timing if available
- Slow workflow detection

## Risk Analysis

Calculate a meaningful risk score for critical workflows using actual evidence.

---

# 11. AI Quality Navigator — X-Factor

Build an **AI Quality Navigator**.

After execution, it should answer:

1. What failed?
2. Why did it likely fail?
3. Is it likely a product defect, automation issue, environment issue, data issue, locator issue, or synchronization issue?
4. What is the business impact?
5. What should we test next?
6. Why should we test it?
7. What risk area is currently under-tested?

Example:

```text
Workflow: Login

Risk Score: 82/100

Reason:
- Authentication is business critical
- Negative coverage is low
- Recent failure observed
- Session timeout is not covered
- Invalid credential boundary is not covered

Recommended next tests:
1. Invalid credentials
2. Empty credentials
3. Account lockout
4. Session timeout
5. Concurrent login
```

Recommendations must be derived from actual application/test evidence whenever possible.

Do not fabricate behaviour.

If AI is unavailable:

- Use deterministic rule-based analysis.
- Clearly label it as fallback analysis.
- Keep the framework fully functional.

---

# 12. Reporting

Create a professional HTML dashboard.

It should contain:

## Executive Summary

- Total tests
- Passed
- Failed
- Skipped
- Pass percentage
- Execution duration

## Quality Intelligence

- Failure classification
- Critical failures
- Potential defects
- Automation failures
- Environment failures

## Self-Healing

- Total healing attempts
- Successful healing
- Failed healing
- Healing confidence

## Coverage

- Web
- Android
- Critical workflows
- Positive scenarios
- Negative scenarios
- Boundary scenarios

## Evidence

- Screenshots
- Logs
- Video where available

## AI Insights

- Failure diagnosis
- Risk observations
- Recommended next tests
- Defect summaries

Make the report understandable within **60 seconds**.

## Output Contract

Use dedicated output folders rather than mixing generated deliverables with source, fixtures, or raw working notes:

```text
Automation Quest/output/
        reports/        HTML dashboard and JUnit XML
        screenshots/    failure screenshots
        traces/         retained Playwright traces
        videos/         retained execution video

Bug Quest/output/
        submission-manifest.md
        strategy/       approved strategy exports
        bug-reports/    approved report exports
        evidence/       approved, redacted evidence copies when requested
```

`Automation Quest/output/` is execution evidence. `Bug Quest/evidence/` remains the controlled working store; `Bug Quest/output/` contains only final reviewed submission material. Do not delete source evidence merely because a final export exists.

---

# 13. Bug Quest Integration

Connect Automation Quest and Bug Quest.

Pipeline:

```text
Test Execution
      ↓
Failure Evidence
      ↓
Failure Classification
      ↓
AI-assisted Analysis
      ↓
Potential Defect
      ↓
Business Impact
      ↓
Structured Bug Report
```

Bug report fields:

- Bug ID
- Title
- Module
- Environment
- Preconditions
- Steps to Reproduce
- Expected Result
- Actual Result
- Severity
- Priority
- Business Impact
- Reproducibility
- Evidence
- Logs
- Screenshot
- Video
- Automation Test Reference
- Failure Classification
- Suggested Regression Coverage

IMPORTANT:

Never create a bug merely because a test failed.

Differentiate:

- Product defect
- Automation defect
- Environment issue
- Data issue
- Locator issue

Only promote a failure to **Potential Product Defect** when evidence supports it.

Also create:

- Defect summary
- Highest-impact defects
- Recommended regression tests
- Failure distribution
- Business impact summary

---

# 14. Test Strategy

Create a high-quality test strategy covering:

- Scope
- Objectives
- Risks
- Test approach
- Test levels
- Functional coverage
- Negative testing
- Boundary testing
- Mobile testing
- Web testing
- Accessibility
- Visual testing
- Performance observations
- Security-oriented validation
- Test data
- Environment
- Automation strategy
- Defect management
- Exit criteria
- Traceability
- Risk-based prioritization

The strategy must be concise enough for judges to understand quickly but deep enough to demonstrate testing expertise.

---

# 15. P0 / P1 / P2 Prioritization

Because implementation time is limited, never sacrifice working automation for advanced features.

## P0 — MUST HAVE

- Application launch
- Web driver setup
- Android driver setup where applicable
- Stable critical workflow
- Page/Screen Objects
- Assertions
- Configuration
- Logging
- Screenshot on failure
- HTML report
- GitHub-ready project
- README
- Reproducible execution

## P1 — WINNING FEATURES

- Failure classification
- Safe self-healing
- AI failure analysis
- Risk-based test generation
- Defect intelligence
- Quality dashboard

## P2 — X-FACTOR

- AI Quality Navigator
- Next-best-test recommendation
- Intelligent risk scoring
- Autonomous failure triage
- Adaptive test selection
- Quality score for each workflow
- Explainable AI recommendations

Never sacrifice P0 stability for P1/P2.

---

# 16. Code Quality Rules

Every generated file must:

- Compile/run.
- Have meaningful names.
- Have clean abstractions.
- Avoid duplicate code.
- Avoid arbitrary sleeps.
- Use explicit synchronization.
- Use proper assertions.
- Have useful logging.
- Avoid hardcoded environment-specific values.
- Avoid hardcoded credentials.
- Be easy to understand.
- Minimize unnecessary dependencies.

No:

```text
Thread.sleep(...)
```

unless there is a genuinely justified and documented reason.

Prefer condition-based waits.

---

# 17. Demo-First Design

The live demo must be reliable.

The ideal demo:

```text
1. Start execution
        ↓
2. Web/mobile workflow executes
        ↓
3. Evidence captured
        ↓
4. Demonstrate a controlled locator failure if safely possible
        ↓
5. Self-healing occurs
        ↓
6. Business assertion executes
        ↓
7. Failure/health classification shown
        ↓
8. AI explains result
        ↓
9. Quality risk shown
        ↓
10. Next-best-test recommendation shown
        ↓
11. Potential defect report generated
        ↓
12. HTML dashboard displayed
```

Do not rely on external AI connectivity for the critical demo.

Prepare deterministic fallback demonstrations.

---

# 18. Validation

After generating code:

1. Build/compile.
2. Run static checks.
3. Run available tests.
4. Fix compilation errors.
5. Fix runtime errors.
6. Verify imports.
7. Verify dependencies.
8. Verify configuration.
9. Verify screenshots.
10. Verify reports.
11. Verify clean-clone reproducibility.
12. Verify README instructions.
13. Verify no secrets.
14. Verify all advanced features degrade gracefully.

Do not stop after generating code.

Actually validate the implementation.

---

# 19. Repository Deliverables

The repository should contain:

```text
tests/
pages/
screens/
components/
core/
drivers/
config/
data/
utils/
healing/
ai/
analysis/
reporting/
artifacts/
docs/
README.md
```

Documentation:

```text
docs/
  ARCHITECTURE.md
  TEST_STRATEGY.md
  AI_DISCLOSURE.md
  DEMO_GUIDE.md
  KNOWN_LIMITATIONS.md
```

---

# 20. AI Disclosure

Create `docs/AI_DISCLOSURE.md`.

It must document:

- AI tools/models used
- Tasks where AI was used
- Important prompts/prompt sequences
- AI-generated outputs incorporated
- How outputs were reviewed
- How outputs were validated
- Errors found
- Hallucinations found
- Limitations
- Time saved
- Improvements achieved
- What was manually verified

Never put:

- Passwords
- OTPs
- Credentials
- Personal data
- Proprietary information
- Sensitive information

into public AI tools or submitted prompts.

---

# 21. README

The README must allow a judge to quickly understand:

1. What problem we solve.
2. Why our framework is different.
3. Architecture.
4. Technology.
5. Setup.
6. Configuration.
7. One-command execution.
8. Web execution.
9. Android execution where applicable.
10. Reporting.
11. Self-healing.
12. AI Quality Navigator.
13. Failure diagnosis.
14. Bug Quest integration.
15. Example report.
16. Known limitations.
17. Reproducibility.

A judge should be able to clone and understand the project quickly.

---

# 22. Jury-Oriented Review

Before final submission, act as a TestAutothon 2026 jury member.

Review the complete repository critically.

Do NOT compliment it.

Find weaknesses that could prevent Top-8 selection.

Evaluate:

1. Does the main workflow actually work?
2. Is the framework reliable?
3. Is the architecture unnecessarily complex?
4. Is Web automation strong?
5. Is Android automation strong?
6. Is failure handling strong?
7. Is self-healing genuine?
8. Is AI meaningful?
9. Can AI be explained and validated?
10. Is the execution report impressive?
11. Can a judge understand the value within 60 seconds?
12. Is the solution reproducible?
13. Are there hardcoded secrets?
14. Are there flaky waits?
15. Are there unnecessary dependencies?
16. Is there enough evidence?
17. Can the framework generate useful Bug Quest evidence?
18. What is our X-Factor?
19. What could another team do better?
20. What should be removed because it adds complexity without scoring value?

Return:

### A. Critical Problems
### B. High-Impact Improvements
### C. Medium Improvements
### D. Features to Remove
### E. Demo Improvements
### F. Jury Questions
### G. Strong Technically Honest Answers

Then implement only changes that materially improve the score without risking the working core.

---

# 23. Presentation Story

Create a 10-minute presentation around:

```text
Problem
   ↓
Limitations of conventional automation
   ↓
Our approach
   ↓
Working automation
   ↓
Intelligent failure diagnosis
   ↓
Safe self-healing
   ↓
AI Quality Navigator
   ↓
Quality risk
   ↓
Next-best-test recommendation
   ↓
Defect intelligence
   ↓
Business value
   ↓
X-Factor
```

Do not make unsupported claims.

Do not claim a feature works unless it has actually been validated.

---

# 24. Jury Questions to Prepare

Prepare answers for:

### Why did you choose this architecture?

### Why do you need AI?

### What happens when AI is unavailable?

### How do you know self-healing did not hide a defect?

### How do you distinguish an automation failure from a product defect?

### How is your AI validated?

### What is genuinely innovative here?

### What happens if the locator changes completely?

### How do you prevent flaky tests?

### How do you calculate risk?

### How are next-best tests selected?

### How does this help developers/business users?

### How reproducible is the framework?

### What did AI generate versus what did your team validate?

### What would you build next with more time?

---

# 25. Implementation Instructions for GitHub Copilot

IMPORTANT:

Do NOT generate the entire framework blindly in one step.

First:

1. Inspect the repository.
2. Inspect all challenge artefacts.
3. Identify application type.
4. Identify environment.
5. Identify available dependencies.
6. Identify existing framework.
7. Identify actual workflows.
8. Propose the smallest winning architecture.

Then provide:

A. Application/environment assessment
B. Winning strategy
C. Recommended technology
D. Architecture diagram in text
E. Repository structure
F. P0/P1/P2 implementation plan
G. Risk-prioritized test scenarios
H. AI features
I. Self-healing strategy
J. Reporting strategy
K. Demo storyline
L. Bug Quest integration strategy
M. Risks and fallback options

Only then begin implementation.

For each implementation step:

- Explain what is being added.
- Create/update files.
- Run validation.
- Fix issues.
- Show exact execution commands.
- Do not move forward while the core is broken.

---

# 26. Final Winning Principle

The winning solution should not be the one with the most code.

It should be the one that gives the jury the strongest combination of:

```text
RELIABILITY
+
TESTING DEPTH
+
ENGINEERING QUALITY
+
AI IMPACT
+
EXPLAINABILITY
+
REPRODUCIBILITY
+
DEMONSTRABILITY
+
X-FACTOR
```

The core workflow must always work.

Advanced intelligence must enhance the automation, not become a single point of failure.

The final experience should make a jury think:

> **"This is not just automation. This is an intelligent Quality Engineering system."**
