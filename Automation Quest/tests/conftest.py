import pytest
import socket
import subprocess
import json
import os
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from src.config import PROJECT_ROOT, settings
from src.failure_classifier import classify_failure


_failure_classifications = []


@pytest.fixture(scope="session", autouse=True)
def artifact_directories() -> None:
    for folder in ("output/reports", "output/screenshots", "output/traces", "output/videos"):
        (PROJECT_ROOT / folder).mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    del call
    outcome = yield
    report = outcome.get_result()
    if report.when in ("setup", "call") and report.failed:
        _failure_classifications.append(classify_failure(item.nodeid, report.longreprtext))


def pytest_sessionfinish(session, exitstatus) -> None:
    del session, exitstatus
    label = os.getenv("QUALITY_RUN_LABEL", "").strip()
    suffix = f"-{label}" if label else ""
    path = PROJECT_ROOT / "output" / "reports" / f"failure-classifications{suffix}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([item.to_dict() for item in _failure_classifications], indent=2) + "\n",
        encoding="utf-8",
    )
    _failure_classifications.clear()


@pytest.fixture
def android_driver():
    app_path = PROJECT_ROOT / settings.android_app_path
    if not app_path.is_file():
        pytest.skip(f"Android APK is not available at {app_path}")
    if not _android_device_is_available():
        pytest.skip("No authorized Android device or emulator is available; start an AVD or connect a device.")
    if not _appium_server_is_available():
        pytest.skip(f"Appium server is unavailable at {settings.appium_server_url}; start Appium before running Android tests.")

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = settings.android_device_name
    options.automation_name = "UiAutomator2"
    if settings.android_udid:
        options.udid = settings.android_udid
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


def _android_device_is_available() -> bool:
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=False)
    return any(line.rstrip().endswith("\tdevice") for line in result.stdout.splitlines())


def _appium_server_is_available() -> bool:
    host, port = "127.0.0.1", 4723
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False