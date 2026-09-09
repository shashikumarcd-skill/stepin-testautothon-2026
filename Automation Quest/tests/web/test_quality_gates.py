import pytest

from src.config import settings
from src.quality_checks import (
    accessibility_findings,
    keyboard_focus_is_available,
    navigation_metrics,
    record_quality_result,
    security_findings,
)


@pytest.mark.web
@pytest.mark.accessibility
def test_login_page_has_basic_accessibility_signals(page):
    page.goto(settings.web_base_url, wait_until="domcontentloaded")
    findings = accessibility_findings(page)
    findings["keyboard_focus_available"] = keyboard_focus_is_available(page)
    status = "warning" if findings["unnamed_interactive_controls"] else "passed"
    record_quality_result("accessibility", status, findings)

    assert findings["semantic_headings"]
    assert findings["keyboard_focus_available"]


@pytest.mark.web
@pytest.mark.performance
def test_login_page_meets_navigation_budget(page):
    response = page.goto(settings.web_base_url, wait_until="load")
    assert response is not None
    metrics = navigation_metrics(response)
    status = "passed" if metrics["domContentLoaded"] < 5000 else "failed"
    record_quality_result("performance", status, metrics)

    assert metrics["domContentLoaded"] < 5000


@pytest.mark.web
@pytest.mark.security
def test_login_page_reports_client_side_security_headers(page):
    response = page.goto(settings.web_base_url, wait_until="domcontentloaded")
    assert response is not None
    findings = security_findings(response)
    record_quality_result("security", "observed", findings)

    assert page.url.startswith("https://")