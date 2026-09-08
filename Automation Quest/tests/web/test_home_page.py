import pytest
from playwright.sync_api import expect

from src.config import settings
from src.pages.home_page import HomePage


@pytest.mark.web
@pytest.mark.smoke
def test_home_page_loads(page):
    home_page = HomePage(page)
    home_page.open(settings.web_base_url)

    assert home_page.title()
    expect(page.get_by_role("heading", name="Test login")).to_be_visible()