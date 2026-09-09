from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from src.quality_models import FailureCategory, FailureClassification, Recommendation


_CATEGORY_WEIGHTS = {
    FailureCategory.PRODUCT_DEFECT: 8,
    FailureCategory.ENVIRONMENT_FAILURE: 6,
    FailureCategory.LOCATOR_FAILURE: 5,
    FailureCategory.SYNCHRONIZATION_FAILURE: 4,
    FailureCategory.TEST_DATA_FAILURE: 3,
    FailureCategory.AUTOMATION_DEFECT: 3,
    FailureCategory.UNKNOWN: 2,
}


def risk_score(classifications: Iterable[FailureClassification], skipped: int = 0) -> int:
    score = sum(_CATEGORY_WEIGHTS[item.category] for item in classifications)
    return min(100, score + skipped * 2)


def recommend_next_tests(
    classifications: Iterable[FailureClassification],
    *,
    skipped: int = 0,
    quality_areas: Iterable[str] = (),
) -> list[Recommendation]:
    category_counts = Counter(item.category for item in classifications)
    recommendations: list[Recommendation] = []
    if category_counts[FailureCategory.PRODUCT_DEFECT]:
        recommendations.append(
            Recommendation("P0", "product behavior", "Review the failing workflow with its captured evidence.", "One or more assertions indicate unexpected application behavior.")
        )
    if category_counts[FailureCategory.LOCATOR_FAILURE] or category_counts[FailureCategory.SYNCHRONIZATION_FAILURE]:
        recommendations.append(
            Recommendation("P1", "automation resilience", "Review locator healing and readiness evidence, then strengthen semantic selectors or waits.", "UI resolution or synchronization failures were observed.")
        )
    if skipped:
        recommendations.append(
            Recommendation("P1", "platform coverage", "Restore skipped platform runs before considering the matrix complete.", f"{skipped} test(s) were skipped and represent unverified coverage."))
    existing_areas = set(quality_areas)
    for area in ("accessibility", "performance", "security"):
        if area not in existing_areas:
            recommendations.append(
                Recommendation("P1", area, f"Run the {area} quality gate.", f"No {area} quality result is available for this execution."))
    return recommendations