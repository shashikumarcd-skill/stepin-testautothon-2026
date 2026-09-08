from __future__ import annotations

import csv
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path


SUPPORTED_INPUT_SUFFIXES = {".csv", ".md", ".pdf", ".txt"}


@dataclass(frozen=True)
class Requirement:
    identifier: str
    title: str
    details: str
    priority: str
    source_reference: str


@dataclass(frozen=True)
class IntakeSummary:
    source_name: str
    source_sha256: str
    requirements: tuple[Requirement, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "source_name": self.source_name,
            "source_sha256": self.source_sha256,
            "requirements": [asdict(requirement) for requirement in self.requirements],
        }


def read_intake(source_path: Path) -> IntakeSummary:
    if not source_path.is_file():
        raise FileNotFoundError(f"Input file was not found: {source_path}")
    if source_path.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_INPUT_SUFFIXES))
        raise ValueError(f"Unsupported input format. Use one of: {supported}")

    source_bytes = source_path.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    if source_path.suffix.lower() == ".csv":
        requirements = _read_csv(source_path)
    else:
        requirements = _read_text(source_path)

    if not requirements:
        raise ValueError("The input did not contain any usable requirement or scenario entries.")
    return IntakeSummary(source_path.name, source_hash, tuple(requirements))


def _read_csv(source_path: Path) -> list[Requirement]:
    with source_path.open(encoding="utf-8-sig", newline="") as source_file:
        rows = list(csv.DictReader(source_file))
    if not rows or not rows[0]:
        return []

    requirements: list[Requirement] = []
    for row_number, row in enumerate(rows, start=2):
        normalized = {key.strip().lower(): (value or "").strip() for key, value in row.items() if key}
        title = _first_value(normalized, "title", "scenario", "requirement", "name", "summary")
        if not title:
            continue
        requirements.append(
            Requirement(
                identifier=_first_value(normalized, "id", "identifier", "requirement id", "scenario id")
                or f"CSV-{row_number - 1:03d}",
                title=title,
                details=_first_value(normalized, "description", "details", "acceptance criteria", "expected result"),
                priority=_priority_from(_first_value(normalized, "priority", "risk", "severity", "tags")),
                source_reference=f"CSV row {row_number}",
            )
        )
    return requirements


def _read_text(source_path: Path) -> list[Requirement]:
    if source_path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        text = "\n".join(page.extract_text() or "" for page in PdfReader(source_path).pages)
    else:
        text = source_path.read_text(encoding="utf-8")

    requirements: list[Requirement] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        candidate = raw_line.strip().lstrip("#-*").strip()
        if len(candidate) < 4 or candidate.lower() in {"requirements", "scenarios", "acceptance criteria"}:
            continue
        if raw_line.lstrip().startswith(("#", "-", "*")) or raw_line[:1].isdigit():
            identifier = f"REQ-{len(requirements) + 1:03d}"
            requirements.append(
                Requirement(
                    identifier=identifier,
                    title=candidate,
                    details="",
                    priority=_priority_from(candidate),
                    source_reference=f"Source line {line_number}",
                )
            )
    return requirements


def _first_value(values: dict[str, str], *keys: str) -> str:
    return next((values[key] for key in keys if values.get(key)), "")


def _priority_from(value: str) -> str:
    normalized = value.upper()
    if "P0" in normalized or "CRITICAL" in normalized or "HIGH" in normalized:
        return "P0"
    if "P2" in normalized or "LOW" in normalized:
        return "P2"
    return "P1"