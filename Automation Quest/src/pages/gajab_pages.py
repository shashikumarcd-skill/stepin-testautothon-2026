from __future__ import annotations

import re
from urllib.parse import urljoin

from playwright.sync_api import Error, Locator, Page, TimeoutError, expect

from src.pages.base_page import BasePage


class GajabHomePage(BasePage):
    guide_overlay_selector = "#home-bargain-guide-portal-overlay"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.login_link = page.get_by_role("link", name="Log in / Sign up")
        self.toys_and_games_link = page.get_by_role("link", name="Toys & Games")
        self.deal_heading = page.get_by_role("heading", name="Gajab Deal Of The Day")
        self.trending_heading = page.get_by_role("heading", name="Trending 🔥")
        self.just_bargained_heading = page.get_by_role("heading", name="Just Bargained")

    def open(self, base_url: str) -> None:
        self._navigate(base_url)

    def open_sign_in(self, base_url: str) -> None:
        if self.page.locator(self.guide_overlay_selector).is_visible():
            self.logger.warning("Home guide overlay blocks login; using the verified sign-in route fallback.")
            self._navigate(urljoin(base_url, "/auth/signin"))
            return
        self.login_link.click()

    def section(self, heading: Locator) -> Locator:
        return heading.locator("xpath=..").locator("xpath=..")

    def deal_of_day_details(self) -> list[str]:
        return self.section(self.deal_heading).locator("p").all_text_contents()

    def latest_live_order_details(self) -> list[str] | None:
        live_orders = self.page.get_by_text("LIVE ORDERS", exact=False)
        if not live_orders.is_visible():
            return None
        live_orders.scroll_into_view_if_needed()
        return self.page.locator("text=/bought|saved/i").all_text_contents()

    def open_toys_and_games(self) -> None:
        self.toys_and_games_link.click()
        expect(self.page).to_have_url(re.compile(r".*/product-list/toys-games/17\?offset=0$"))

    def choose_language(self, language: str) -> None:
        self.page.get_by_role("button", name=re.compile("English|Hinglish")).click()
        self.page.get_by_text(language, exact=True).click()

    def trending_bargain_counts(self) -> list[int]:
        values = self.section(self.trending_heading).locator("text=/Times Bargained/").all_text_contents()
        return [int("".join(character for character in value if character.isdigit())) for value in values]

    def _navigate(self, url: str) -> None:
        last_error: Error | None = None
        for _ in range(3):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                return
            except (Error, TimeoutError) as error:
                last_error = error
        raise AssertionError(f"Gajab staging could not be reached after three attempts: {url}") from last_error


class GajabSignInPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.mobile_number = page.get_by_role("textbox", name="Enter your Mobile Number here")
        self.consent = page.get_by_role("checkbox")
        self.request_otp_button = page.get_by_role("button", name="Request OTP")

    def open(self, base_url: str) -> None:
        GajabHomePage(self.page)._navigate(urljoin(base_url, "/auth/signin"))

    def request_otp(self, mobile_number: str) -> None:
        self.mobile_number.fill(mobile_number)
        self.consent.check()
        self.request_otp_button.click()