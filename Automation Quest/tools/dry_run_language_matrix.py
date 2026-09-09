from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"
SUPPORTED_LANGUAGES = ("english", "hinglish")


def _run(command: list[str], language: str, label: str) -> int:
    print(f"\n=== Dry Run | language={language} | target={label} ===")
    print(" ".join(command))

    env = os.environ.copy()
    env["CHALLENGE_LANGUAGE"] = language

    result = subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=False)
    return result.returncode


def _pytest_collect_cmd(target: str, report_prefix: str, marker: str, extra: list[str]) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        target,
        "--collect-only",
        "-q",
        "-m",
        marker,
        f"--html={REPORTS_DIR / f'report-{report_prefix}.html'}",
        f"--junitxml={REPORTS_DIR / f'junit-{report_prefix}.xml'}",
        *extra,
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Dry run TestAutothon challenge readiness for English and Hinglish "
            "without executing browser/device sessions."
        )
    )
    parser.add_argument(
        "--marker",
        default="smoke",
        help="Marker expression used during dry run collection. Default: smoke",
    )
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments passed to every pytest collect command.",
    )
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    extra = list(args.pytest_args)
    if extra and extra[0] == "--":
        extra = extra[1:]

    failed: list[tuple[str, str, int]] = []

    for language in SUPPORTED_LANGUAGES:
        web_prefix = f"dryrun-web-{language}"
        android_prefix = f"dryrun-android-{language}"

        web_cmd = _pytest_collect_cmd("tests/web", web_prefix, args.marker, extra)
        android_cmd = _pytest_collect_cmd("tests/android", android_prefix, args.marker, extra)

        web_code = _run(web_cmd, language, "web")
        if web_code:
            failed.append((language, "web", web_code))

        android_code = _run(android_cmd, language, "android")
        if android_code:
            failed.append((language, "android", android_code))

    print("\n=== Dry Run Summary ===")
    if not failed:
        print("Dry run passed for both languages (English, Hinglish) on web and android suites.")
        print("Challenge language matrix is ready for execution mode.")
        return 0

    for language, target, code in failed:
        print(f"language={language} target={target} failed with exit code {code}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
