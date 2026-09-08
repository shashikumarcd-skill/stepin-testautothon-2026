import pytest
from appium.webdriver.common.appiumby import AppiumBy


@pytest.mark.android
@pytest.mark.smoke
def test_android_application_opens(android_driver):
    assert android_driver.current_package
    assert android_driver.find_elements(AppiumBy.XPATH, "//*")