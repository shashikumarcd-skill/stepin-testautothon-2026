import pytest
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from src.config import PROJECT_ROOT, settings


@pytest.fixture(scope="session", autouse=True)
def artifact_directories() -> None:
    for folder in ("output/reports", "output/screenshots", "output/traces", "output/videos"):
        (PROJECT_ROOT / folder).mkdir(parents=True, exist_ok=True)


@pytest.fixture
def android_driver():
    app_path = PROJECT_ROOT / settings.android_app_path
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = settings.android_device_name
    options.automation_name = "UiAutomator2"
    if settings.android_platform_version:
        options.platform_version = settings.android_platform_version
    if app_path.exists():
        options.app = str(app_path)
    else:
        options.app_package = settings.android_app_package
        options.app_activity = settings.android_app_activity

    driver = WebDriver(settings.appium_server_url, options=options)
    yield driver
    driver.quit()