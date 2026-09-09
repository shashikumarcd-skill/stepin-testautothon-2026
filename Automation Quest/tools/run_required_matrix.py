from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as element_tree
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"
sys.path.insert(0, str(PROJECT_ROOT))

from src.bi_reporting import create_quality_dashboard


def _run(command: list[str], label: str) -> int:
    print(f"\n=== {label} ===")
    print(" ".join(command))
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env={**os.environ, "QUALITY_RUN_LABEL": label},
        check=False,
    )
    return result.returncode


def _pytest_base_args(extra_args: Iterable[str]) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        *extra_args,
    ]


def _junit_summary(path: Path) -> dict[str, int]:
    root = element_tree.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    counts = {
        key: sum(int(suite.attrib.get(key, "0")) for suite in suites)
        for key in ("tests", "failures", "errors", "skipped")
    }
    counts["passed"] = counts["tests"] - counts["failures"] - counts["errors"] - counts["skipped"]
    return counts


def _write_execution_summary(results: list[tuple[str, int]]) -> None:
    runs = []
    for label, exit_code in results:
        report = REPORTS_DIR / f"junit-{label.removeprefix('web-')}.xml"
        summary = _junit_summary(report) if report.is_file() else {}
        runs.append({"target": label, "exit_code": exit_code, **summary})

    totals = {
        key: sum(run.get(key, 0) for run in runs)
        for key in ("tests", "passed", "failures", "errors", "skipped")
    }
    (REPORTS_DIR / "execution-summary.json").write_text(
        json.dumps({"runs": runs, "totals": totals}, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the TestAutothon participant-required automation matrix: "
            "Chrome, Firefox, Edge, and Android."
        )
    )
    parser.add_argument(
        "--web-target",
        default="tests/web",
        help="Web pytest target (file/folder/expression). Default: tests/web",
    )
    parser.add_argument(
        "--android-target",
        default="tests/android",
        help="Android pytest target (file/folder/expression). Default: tests/android",
    )
    parser.add_argument(
        "--marker",
        default="smoke",
        help="Marker expression applied to all runs. Default: smoke",
    )
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments passed to every pytest invocation.",
    )
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    extra = list(args.pytest_args)
    if extra and extra[0] == "--":
        extra = extra[1:]

    shared = ["-m", args.marker, *extra]

    runs = [
        (
            "web-chrome",
            _pytest_base_args(
                [
                    args.web_target,
                    "--browser",
                    "chromium",
                    "--browser-channel",
                    "chrome",
                    f"--html={REPORTS_DIR / 'report-chrome.html'}",
                    f"--junitxml={REPORTS_DIR / 'junit-chrome.xml'}",
                    *shared,
                ]
            ),
        ),
        (
            "web-firefox",
            _pytest_base_args(
                [
                    args.web_target,
                    "--browser",
                    "firefox",
                    f"--html={REPORTS_DIR / 'report-firefox.html'}",
                    f"--junitxml={REPORTS_DIR / 'junit-firefox.xml'}",
                    *shared,
                ]
            ),
        ),
        (
            "web-edge",
            _pytest_base_args(
                [
                    args.web_target,
                    "--browser",
                    "chromium",
                    "--browser-channel",
                    "msedge",
                    f"--html={REPORTS_DIR / 'report-edge.html'}",
                    f"--junitxml={REPORTS_DIR / 'junit-edge.xml'}",
                    *shared,
                ]
            ),
        ),
        (
            "android",
            _pytest_base_args(
                [
                    args.android_target,
                    f"--html={REPORTS_DIR / 'report-android.html'}",
                    f"--junitxml={REPORTS_DIR / 'junit-android.xml'}",
                    *shared,
                ]
            ),
        ),
    ]

    results = []
    for label, command in runs:
        code = _run(command, label)
        results.append((label, code))

    _write_execution_summary(results)
    create_quality_dashboard(REPORTS_DIR)

    failed = [(label, code) for label, code in results if code]

    print("\n=== Matrix Summary ===")
    if not failed:
        print("All required runs passed: Chrome, Firefox, Edge, and Android.")
        return 0

    for label, code in failed:
        print(f"{label}: failed with exit code {code}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
