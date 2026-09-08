from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator("#submit")
        self.error_message = page.locator("#error")

    def open(self, base_url: str) -> None:
        self.page.goto(base_url, wait_until="domcontentloaded")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()