import logging
import json

from playwright.sync_api import Locator, Page

from src.config import PROJECT_ROOT
from src.quality_models import HealingEvent


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def first_visible(
        self,
        *candidates: str,
        expected_role: str | None = None,
        expected_name: str | None = None,
    ) -> Locator:
        """Return the first visible locator and record any safe fallback selection."""
        for index, selector in enumerate(candidates):
            locator = self.page.locator(selector).first
            if locator.is_visible():
                if index:
                    validation_passed = self._validate_locator(locator, expected_role, expected_name)
                    confidence = round((len(candidates) - index) / len(candidates), 2)
                    self._record_healing_event(
                        HealingEvent(
                            primary_selector=candidates[0],
                            selected_selector=selector,
                            candidate_index=index,
                            confidence=confidence if validation_passed else 0.0,
                            safe_validation_passed=validation_passed,
                            expected_role=expected_role,
                            expected_name=expected_name,
                        )
                    )
                    self.logger.warning("Locator fallback selected: %s (safe=%s)", selector, validation_passed)
                return locator
        raise AssertionError(f"No visible locator found from: {candidates}")

    @staticmethod
    def _validate_locator(locator: Locator, expected_role: str | None, expected_name: str | None) -> bool:
        if expected_role and locator.get_attribute("role") != expected_role:
            return False
        if expected_name:
            accessible_name = locator.get_attribute("aria-label") or locator.get_attribute("title")
            if accessible_name != expected_name:
                return False
        return True

    @staticmethod
    def _record_healing_event(event: HealingEvent) -> None:
        path = PROJECT_ROOT / "output" / "reports" / "healing-events.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        events = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
        events.append(event.to_dict())
        path.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")