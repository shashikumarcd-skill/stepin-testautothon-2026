from playwright.sync_api import Page

from src.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.page.goto(base_url, wait_until="domcontentloaded")

    def title(self) -> str:
        return self.page.title()

    def has_primary_heading(self) -> bool:
        return self.first_visible("h1", "[role='heading'][aria-level='1']").is_visible()