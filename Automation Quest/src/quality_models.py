from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class FailureCategory(StrEnum):
    PRODUCT_DEFECT = "product_defect"
    AUTOMATION_DEFECT = "automation_defect"
    ENVIRONMENT_FAILURE = "environment_failure"
    TEST_DATA_FAILURE = "test_data_failure"
    LOCATOR_FAILURE = "locator_failure"
    SYNCHRONIZATION_FAILURE = "synchronization_failure"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FailureClassification:
    nodeid: str
    category: FailureCategory
    reason: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            **asdict(self),
            "category": self.category.value,
        }


@dataclass(frozen=True)
class HealingEvent:
    primary_selector: str
    selected_selector: str
    candidate_index: int
    confidence: float
    safe_validation_passed: bool
    expected_role: str | None
    expected_name: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Recommendation:
    priority: str
    area: str
    action: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)