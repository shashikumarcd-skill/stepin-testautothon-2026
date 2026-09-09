from __future__ import annotations

from src.quality_models import FailureCategory, FailureClassification


_RULES: tuple[tuple[FailureCategory, tuple[str, ...], str], ...] = (
    (
        FailureCategory.ENVIRONMENT_FAILURE,
        (
            "connection refused",
            "name or service not known",
            "no authorized android device",
            "appium server",
            "devtools remote debugging is disallowed",
            "headless mode is disallowed",
        ),
        "The failure indicates unavailable test infrastructure.",
    ),
    (
        FailureCategory.SYNCHRONIZATION_FAILURE,
        ("timeout", "timed out", "waiting for", "not visible"),
        "The failure indicates a timing or readiness problem.",
    ),
    (
        FailureCategory.LOCATOR_FAILURE,
        ("locator", "selector", "element not found", "strict mode violation"),
        "The failure indicates a UI element could not be resolved.",
    ),
    (
        FailureCategory.TEST_DATA_FAILURE,
        ("test data", "credential", "username", "password"),
        "The failure indicates configured or generated test data may be invalid.",
    ),
    (
        FailureCategory.AUTOMATION_DEFECT,
        ("attributeerror", "typeerror", "keyerror", "importerror"),
        "The failure indicates a test implementation error.",
    ),
    (
        FailureCategory.PRODUCT_DEFECT,
        ("assertionerror", "expect(", "expected", "received"),
        "The application behavior did not satisfy the test assertion.",
    ),
)


def classify_failure(nodeid: str, message: str) -> FailureClassification:
    normalized = message.lower()
    for category, signals, reason in _RULES:
        if any(signal in normalized for signal in signals):
            return FailureClassification(nodeid=nodeid, category=category, reason=reason, message=message)
    return FailureClassification(
        nodeid=nodeid,
        category=FailureCategory.UNKNOWN,
        reason="No deterministic classification rule matched the failure evidence.",
        message=message,
    )