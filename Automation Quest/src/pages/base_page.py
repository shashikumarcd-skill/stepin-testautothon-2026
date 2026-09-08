import logging

from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def first_visible(self, *candidates: str) -> Locator:
        """Return the first visible locator and log a fallback selection."""
        for index, selector in enumerate(candidates):
            locator = self.page.locator(selector).first
            if locator.is_visible():
                if index:
                    self.logger.warning("Locator fallback selected: %s", selector)
                return locator
        raise AssertionError(f"No visible locator found from: {candidates}")