# Competition-Start Intake

Use one supplied `.csv`, `.pdf`, `.txt`, or `.md` file as the requirements or scenario input. Keep the original document in the organizer-provided working area rather than copying it to `output/`.

```powershell
python tools/execute_challenge.py <input-file>
python tools/execute_challenge.py <input-file> -- -m smoke tests/web
```

With no pytest arguments, the command safely collects the available tests rather than attempting an unverified web or Android environment.

The command creates these derived outputs in `output/reports/`:

- `input-summary.json`: source filename, SHA-256 hash, extracted requirement/scenario entries, priorities, and source references.
- `quality-presentation.pptx`: a concise briefing with provenance, prioritized intent, test execution totals from JUnit, and evidence/triage actions.
- `report.html` and `junit.xml`: pytest execution reports when a test scope is executed.

The extractor is intentionally conservative. It does not create page objects, locators, credentials, APIs, test data, or product-defect claims. AI agents can draft coverage suggestions from the intake, but a tester must verify workflows and expected results against the supplied application before tests are implemented or failures are promoted to Bug Quest.