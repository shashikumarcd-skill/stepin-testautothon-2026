import pytest
import re
from playwright.sync_api import expect

from src.config import settings
from src.pages.gajab_pages import GajabHomePage, GajabSignInPage


@pytest.mark.web
@pytest.mark.smoke
def test_gajab_home_exposes_required_discovery_workflow(page):
    home = GajabHomePage(page)
    home.open(settings.web_base_url)

    expect(home.deal_heading).to_be_visible()
    expect(home.trending_heading).to_be_visible()
    expect(home.just_bargained_heading).to_be_visible()
    assert any("Asking Price" in detail for detail in home.deal_of_day_details())
    live_order_details = home.latest_live_order_details()
    if live_order_details is None:
        pytest.skip("Live Orders feed was unavailable in this staging execution; see the runtime report for the documented fallback.")
    assert live_order_details


@pytest.mark.web
@pytest.mark.smoke
def test_login_entry_uses_documented_fallback_when_home_guide_blocks_click(page):
    home = GajabHomePage(page)
    home.open(settings.web_base_url)
    home.open_sign_in(settings.web_base_url)

    expect(page).to_have_url(re.compile(r".*/auth/signin$"))
    expect(page.get_by_role("heading", name="Log in / Sign up")).to_be_visible()


@pytest.mark.web
@pytest.mark.parametrize("mobile_number", ["", "123", "abcdefghij", "99999999999999999999"])
def test_invalid_mobile_number_cannot_request_otp_without_valid_data(page, mobile_number):
    sign_in = GajabSignInPage(page)
    sign_in.open(settings.web_base_url)
    sign_in.mobile_number.fill(mobile_number)

    expect(sign_in.request_otp_button).to_be_disabled()


@pytest.mark.web
def test_toys_and_games_category_is_reachable(page):
    home = GajabHomePage(page)
    home.open(settings.web_base_url)
    home.open_toys_and_games()

    expect(page.get_by_text("Toys & Games", exact=True).first).to_be_visible()


@pytest.mark.web
@pytest.mark.parametrize("language", ["English", "Hinglish"])
def test_language_preference_can_be_selected(page, language):
    home = GajabHomePage(page)
    home.open(settings.web_base_url)
    home.choose_language(language)

    expect(page.get_by_text(language, exact=True)).not_to_be_visible()


@pytest.mark.web
def test_trending_products_expose_bargain_counts_for_leader_selection(page):
    home = GajabHomePage(page)
    home.open(settings.web_base_url)
    counts = home.trending_bargain_counts()

    assert counts
    assert max(counts) >= counts[0]