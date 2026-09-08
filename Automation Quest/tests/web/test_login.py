import pytest
from playwright.sync_api import expect

from src.config import settings
from src.pages.login_page import LoginPage


@pytest.mark.web
@pytest.mark.smoke
def test_valid_user_can_log_in(page):
    login_page = LoginPage(page)
    login_page.open(settings.web_base_url)
    login_page.login(settings.web_username, settings.web_password)

    expect(page).to_have_url("https://practicetestautomation.com/logged-in-successfully/")
    expect(page.get_by_role("heading", name="Logged In Successfully")).to_be_visible()
    expect(page.get_by_role("link", name="Log out")).to_be_visible()


@pytest.mark.web
def test_invalid_username_shows_specific_error(page):
    login_page = LoginPage(page)
    login_page.open(settings.web_base_url)
    login_page.login("incorrectUser", settings.web_password)

    expect(login_page.error_message).to_have_text("Your username is invalid!")


@pytest.mark.web
def test_invalid_password_shows_specific_error(page):
    login_page = LoginPage(page)
    login_page.open(settings.web_base_url)
    login_page.login(settings.web_username, "incorrectPassword")

    expect(login_page.error_message).to_have_text("Your password is invalid!")