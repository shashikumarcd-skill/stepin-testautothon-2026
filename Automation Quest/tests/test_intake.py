from pathlib import Path

import pytest

from src.intake import read_intake


def test_read_intake_extracts_csv_requirements_and_priorities(tmp_path: Path):
    source = tmp_path / "scenarios.csv"
    source.write_text(
        "ID,Scenario,Priority,Expected Result\nSC-01,User can sign in,P0,Dashboard opens\n",
        encoding="utf-8",
    )

    intake = read_intake(source)

    assert intake.source_name == "scenarios.csv"
    assert intake.requirements[0].identifier == "SC-01"
    assert intake.requirements[0].priority == "P0"


def test_read_intake_rejects_unsupported_file_types(tmp_path: Path):
    source = tmp_path / "scenarios.docx"
    source.write_text("Not supported", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported input format"):
        read_intake(source)