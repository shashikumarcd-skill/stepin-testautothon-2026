from __future__ import annotations

import json
from typing import Any

from playwright.sync_api import Page, Response

from src.config import PROJECT_ROOT


def record_quality_result(area: str, status: str, details: dict[str, Any]) -> None:
    path = PROJECT_ROOT / "output" / "reports" / "quality-check-results.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    results = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
    results.append({"area": area, "status": status, "details": details})
    path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


def accessibility_findings(page: Page) -> dict[str, Any]:
    missing_names = page.locator("button, input:not([type=hidden]), a[href]").evaluate_all(
        """elements => elements.filter(element => {
            const label = element.getAttribute('aria-label') || element.getAttribute('title') ||
                element.getAttribute('placeholder') || element.innerText || element.value ||
                (element.id && document.querySelector(`label[for='${element.id}']`)?.innerText);
            return !label || !label.trim();
        }).map(element => element.outerHTML)"""
    )
    return {
        "semantic_headings": page.locator("h1, h2, h3, h4, h5, h6, [role=heading]").count(),
        "unnamed_interactive_controls": missing_names,
    }


def keyboard_focus_is_available(page: Page) -> bool:
    page.locator("body").press("Tab")
    return bool(page.evaluate("document.activeElement !== document.body"))


def navigation_metrics(response: Response) -> dict[str, float]:
    timing = response.request.frame.page.evaluate(
        """() => {
            const entry = performance.getEntriesByType('navigation')[0];
            return { domContentLoaded: entry?.domContentLoadedEventEnd || 0, load: entry?.loadEventEnd || 0 };
        }"""
    )
    return {key: round(float(value), 2) for key, value in timing.items()}


def security_findings(response: Response) -> dict[str, bool]:
    headers = {key.lower(): value for key, value in response.headers.items()}
    return {
        "content_security_policy": "content-security-policy" in headers,
        "x_content_type_options": headers.get("x-content-type-options", "").lower() == "nosniff",
        "strict_transport_security": "strict-transport-security" in headers,
    }