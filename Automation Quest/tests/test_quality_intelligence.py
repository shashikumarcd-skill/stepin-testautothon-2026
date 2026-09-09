from src.failure_classifier import classify_failure
from src.quality_models import FailureCategory
from src.quality_navigator import recommend_next_tests, risk_score
from src.test_data_factory import invalid_login_cases


def test_classifier_labels_environment_and_product_failures():
    environment = classify_failure("tests/android/test_smoke.py::test_open", "Appium server connection refused")
    policy_block = classify_failure("tests/web/test_home.py::test_home", "DevTools remote debugging is disallowed by the system admin")
    product = classify_failure("tests/web/test_login.py::test_login", "AssertionError: expected success heading")

    assert environment.category is FailureCategory.ENVIRONMENT_FAILURE
    assert policy_block.category is FailureCategory.ENVIRONMENT_FAILURE
    assert product.category is FailureCategory.PRODUCT_DEFECT


def test_navigator_prioritizes_failures_and_unverified_quality_areas():
    classification = classify_failure("tests/web/test_login.py::test_login", "AssertionError: expected success heading")

    recommendations = recommend_next_tests([classification], skipped=1, quality_areas=("accessibility",))

    assert risk_score([classification], skipped=1) == 10
    assert [item.area for item in recommendations] == ["product behavior", "platform coverage", "performance", "security"]


def test_invalid_login_data_covers_boundary_and_inert_security_shaped_inputs():
    names = {case.name for case in invalid_login_cases()}

    assert {"empty credentials", "overlong username", "unicode username", "sql-shaped username", "xss-shaped username"} <= names