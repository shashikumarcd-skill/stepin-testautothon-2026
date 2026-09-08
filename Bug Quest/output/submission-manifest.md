# Submission Manifest

Complete this file when packaging the final Bug Quest submission.

| Deliverable | Final output path | Source | Validation date | Environment/build coverage | Final classification or approval | Known limitations |
| --- | --- | --- | --- | --- | --- |
| Test strategy export | `output/strategy/` | `docs/test-strategy.md` | | | Approved strategy | |
| Bug report export(s) | `output/bug-reports/` | `reports/bugs/` | | | Product defect, evidence validated | |
| Evidence package, if requested | `output/evidence/` | `evidence/` | | | Approved and redacted | |

## Final Review

- [ ] All defect reports pass `python tools/validate_bug_reports.py`.
- [ ] Evidence references resolve and are redacted.
- [ ] Output contains no credentials, personal data, or unsupported claims.
- [ ] Every automation-originated finding records its source test, run, environment, and final classification.
- [ ] Every packaged defect has a validated reproduction, documented business impact, `Product defect` classification, and regression recommendation.
- [ ] Strategy or defect-summary export includes highest-impact defects, recommended regression tests, failure distribution, and business-impact summary.
- [ ] Known limitations and untested risks are disclosed.