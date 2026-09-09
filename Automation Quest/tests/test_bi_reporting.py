import json

from src.bi_reporting import create_quality_dashboard


def test_dashboard_aggregates_execution_evidence_and_recommendations(tmp_path):
    (tmp_path / "execution-summary.json").write_text(
        json.dumps({"runs": [{"target": "web-chrome", "passed": 2, "failures": 1, "errors": 0, "skipped": 0}], "totals": {"tests": 3, "passed": 2, "failures": 1, "errors": 0, "skipped": 1}}),
        encoding="utf-8",
    )
    (tmp_path / "failure-classifications-web-chrome.json").write_text(
        json.dumps([{ "nodeid": "tests/web/test_login.py::test_login", "category": "product_defect", "reason": "assertion", "message": "AssertionError" }]),
        encoding="utf-8",
    )
    (tmp_path / "quality-check-results.json").write_text(json.dumps([{ "area": "accessibility", "status": "passed", "details": {} }]), encoding="utf-8")
    (tmp_path / "healing-events.json").write_text(json.dumps([{ "safe_validation_passed": True }]), encoding="utf-8")

    dashboard = create_quality_dashboard(tmp_path)

    assert dashboard["risk_score"] == 10
    assert dashboard["healing"] == {"events": 1, "safe_events": 1}
    assert [item["area"] for item in dashboard["recommendations"]] == ["product behavior", "platform coverage", "performance", "security"]
    assert (tmp_path / "quality-dashboard.html").is_file()