import json

import pytest

from src.pages.base_page import BasePage


class FakeLocator:
    def __init__(self, visible: bool, attributes: dict[str, str] | None = None) -> None:
        self.visible = visible
        self.attributes = attributes or {}
        self.first = self

    def is_visible(self) -> bool:
        return self.visible

    def get_attribute(self, name: str) -> str | None:
        return self.attributes.get(name)


class FakePage:
    def __init__(self, locators: dict[str, FakeLocator]) -> None:
        self.locators = locators

    def locator(self, selector: str) -> FakeLocator:
        return self.locators[selector]


def test_fallback_records_confident_validated_event(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pages.base_page.PROJECT_ROOT", tmp_path)
    page = FakePage({"#old": FakeLocator(False), "#new": FakeLocator(True, {"role": "button", "aria-label": "Sign in"})})

    locator = BasePage(page).first_visible("#old", "#new", expected_role="button", expected_name="Sign in")

    assert locator is page.locators["#new"]
    event = json.loads((tmp_path / "output/reports/healing-events.json").read_text(encoding="utf-8"))[0]
    assert event["selected_selector"] == "#new"
    assert event["safe_validation_passed"] is True
    assert event["confidence"] == 0.5


def test_missing_candidates_preserves_assertion_failure():
    page = FakePage({"#old": FakeLocator(False), "#new": FakeLocator(False)})

    with pytest.raises(AssertionError, match="No visible locator"):
        BasePage(page).first_visible("#old", "#new")