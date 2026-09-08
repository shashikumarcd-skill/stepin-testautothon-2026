from pathlib import Path
import sys


REQUIRED_HEADINGS = (
    "## Summary",
    "## Defect qualification",
    "## Preconditions",
    "## Steps to reproduce",
    "## Expected result",
    "## Actual result",
    "## Business impact",
    "## Evidence",
)


def validate_report(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in content]
    if "| Failure classification | Product defect |" not in content:
        missing.append("a Product defect failure classification")
    if "| Automation test reference |" not in content:
        missing.append("an Automation test reference field")
    return missing


def main() -> int:
    report_directory = Path(__file__).resolve().parents[1] / "reports" / "bugs"
    reports = sorted(report_directory.glob("*.md"))
    if not reports:
        print("No reports found. Add validated defects under reports/bugs/.")
        return 0

    failures = 0
    for report in reports:
        missing = validate_report(report)
        if missing:
            failures += 1
            print(f"FAIL {report.name}: missing {', '.join(missing)}")
        else:
            print(f"PASS {report.name}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())