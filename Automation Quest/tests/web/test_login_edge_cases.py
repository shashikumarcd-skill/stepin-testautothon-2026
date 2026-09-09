import pytest
from playwright.sync_api import expect

from src.config import settings
from src.pages.login_page import LoginPage
from src.test_data_factory import invalid_login_cases


@pytest.mark.web
@pytest.mark.parametrize("case", invalid_login_cases(), ids=lambda case: case.name)
def test_invalid_boundary_inputs_do_not_authenticate(page, case):
    login_page = LoginPage(page)
    login_page.open(settings.web_base_url)
    login_page.login(case.username, case.password)

    expect(page).to_have_url(settings.web_base_url)
    expect(login_page.error_message).to_be_visible()
    expect(page.get_by_role("heading", name="Logged In Successfully")).not_to_be_visible()