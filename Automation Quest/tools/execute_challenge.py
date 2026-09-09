from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.intake import read_intake
from src.bi_reporting import create_quality_dashboard
from src.presentation import create_presentation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a reviewed test-intent briefing, execute pytest, and generate a presentation."
    )
    parser.add_argument("input_file", type=Path, help="Requirement/scenario file: .csv, .pdf, .txt, or .md")
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Optional pytest arguments; place them after --, for example: -- -m smoke tests/web",
    )
    args = parser.parse_args()

    intake = read_intake(args.input_file)
    reports_path = PROJECT_ROOT / "output" / "reports"
    reports_path.mkdir(parents=True, exist_ok=True)
    (reports_path / "input-summary.json").write_text(
        json.dumps(intake.as_dict(), indent=2), encoding="utf-8"
    )
    pytest_args = args.pytest_args or ["-m", "smoke"]
    pytest_command = [sys.executable, "-m", "pytest", *pytest_args]
    result = subprocess.run(pytest_command, cwd=PROJECT_ROOT, check=False)
    create_quality_dashboard(reports_path)
    create_presentation(
        intake,
        reports_path / "quality-presentation.pptx",
        reports_path / "junit.xml",
        " ".join(pytest_command),
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())