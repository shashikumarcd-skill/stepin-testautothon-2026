from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

from src.quality_models import FailureCategory, FailureClassification
from src.quality_navigator import recommend_next_tests, risk_score


def create_quality_dashboard(reports_dir: Path) -> dict[str, Any]:
    execution = _read_json(reports_dir / "execution-summary.json", {"runs": [], "totals": {}})
    classifications = [
        FailureClassification(
            nodeid=item["nodeid"],
            category=FailureCategory(item["category"]),
            reason=item["reason"],
            message=item["message"],
        )
        for path in reports_dir.glob("failure-classifications*.json")
        for item in _read_json(path, [])
    ]
    quality_results = _read_json(reports_dir / "quality-check-results.json", [])
    healing_events = _read_json(reports_dir / "healing-events.json", [])
    totals = execution.get("totals", {})
    category_counts = Counter(item.category.value for item in classifications)
    quality_areas = {item["area"] for item in quality_results}
    dashboard = {
        "execution": execution,
        "risk_score": risk_score(classifications, skipped=int(totals.get("skipped", 0))),
        "failure_categories": dict(sorted(category_counts.items())),
        "quality_results": quality_results,
        "healing": {
            "events": len(healing_events),
            "safe_events": sum(bool(item.get("safe_validation_passed")) for item in healing_events),
        },
        "recommendations": [
            item.to_dict()
            for item in recommend_next_tests(classifications, skipped=int(totals.get("skipped", 0)), quality_areas=quality_areas)
        ],
    }
    (reports_dir / "quality-dashboard.json").write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    (reports_dir / "quality-dashboard.html").write_text(_render_html(dashboard), encoding="utf-8")
    return dashboard


def _read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def _render_html(dashboard: dict[str, Any]) -> str:
    totals = dashboard["execution"].get("totals", {})
    rows = "".join(
        f"<tr><td>{html.escape(run.get('target', 'unknown'))}</td><td>{run.get('passed', 0)}</td><td>{run.get('failures', 0) + run.get('errors', 0)}</td><td>{run.get('skipped', 0)}</td></tr>"
        for run in dashboard["execution"].get("runs", [])
    )
    recommendations = "".join(
        f"<li><strong>{html.escape(item['priority'])} {html.escape(item['area'])}</strong>: {html.escape(item['action'])}<br><small>{html.escape(item['reason'])}</small></li>"
        for item in dashboard["recommendations"]
    ) or "<li>No additional recommendations.</li>"
    quality = "".join(
        f"<li>{html.escape(item['area'])}: <strong>{html.escape(item['status'])}</strong></li>"
        for item in dashboard["quality_results"]
    ) or "<li>No quality-gate results were captured.</li>"
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Automation Quest Quality Dashboard</title>
<style>body{{font-family:Segoe UI,sans-serif;margin:32px;color:#182026}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #b8c2cc;padding:8px;text-align:left}}.risk{{font-size:2rem;font-weight:700;color:#b54708}}li{{margin:10px 0}}</style></head>
<body><h1>Automation Quest Quality Dashboard</h1><p class=\"risk\">Risk score: {dashboard['risk_score']}/100</p>
<p>Tests: {totals.get('tests', 0)} | Passed: {totals.get('passed', 0)} | Failed/errors: {totals.get('failures', 0) + totals.get('errors', 0)} | Skipped: {totals.get('skipped', 0)}</p>
<h2>Cross-browser and platform results</h2><table><thead><tr><th>Target</th><th>Passed</th><th>Failed/errors</th><th>Skipped</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Quality gates</h2><ul>{quality}</ul><h2>Locator healing</h2><p>{dashboard['healing']['safe_events']} safely validated event(s) out of {dashboard['healing']['events']} fallback event(s).</p>
<h2>Prioritized actions</h2><ul>{recommendations}</ul></body></html>"""