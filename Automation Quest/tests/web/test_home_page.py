import pytest
from playwright.sync_api import expect

from src.config import settings
from src.pages.gajab_pages import GajabHomePage


@pytest.mark.web
@pytest.mark.smoke
def test_home_page_loads(page):
    home_page = GajabHomePage(page)
    home_page.open(settings.web_base_url)

    assert home_page.title()
    expect(page.get_by_role("heading", name="Gajab: India’s Bargain Bazaar | Bargain Online & Save")).to_be_visible()