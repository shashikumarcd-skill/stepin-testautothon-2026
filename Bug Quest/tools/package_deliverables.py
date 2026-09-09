from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"


def _safe_team_name(raw: str) -> str:
    return "".join(ch for ch in raw.strip() if ch.isalnum() or ch in {"_", "-"})


def _copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    print(f"Copied: {source} -> {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Copy final Bug Quest exports into TestAutothon naming convention files."
        )
    )
    parser.add_argument("--team-name", required=True, help="Team name prefix.")
    parser.add_argument(
        "--strategy-source",
        default="docs/test-strategy.md",
        help="Approved test strategy export source path.",
    )
    parser.add_argument(
        "--bug-report-source",
        required=True,
        help="Approved bug report export source path.",
    )
    args = parser.parse_args()

    team_name = _safe_team_name(args.team_name)
    if not team_name:
        raise ValueError("Team name must contain alphanumeric characters.")

    strategy_source = (PROJECT_ROOT / args.strategy_source).resolve()
    bug_report_source = (PROJECT_ROOT / args.bug_report_source).resolve()

    if not strategy_source.exists():
        raise FileNotFoundError(f"Strategy source not found: {strategy_source}")
    if not bug_report_source.exists():
        raise FileNotFoundError(f"Bug report source not found: {bug_report_source}")

    strategy_name = f"{team_name}_TestAutothon26_TestStrategy{strategy_source.suffix}"
    bug_report_name = f"{team_name}_TestAutothon26_BugReport{bug_report_source.suffix}"

    strategy_target = OUTPUT_DIR / "strategy" / strategy_name
    bug_report_target = OUTPUT_DIR / "bug-reports" / bug_report_name

    _copy(strategy_source, strategy_target)
    _copy(bug_report_source, bug_report_target)

    print("\nSubmission naming complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
