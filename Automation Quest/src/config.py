from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    web_base_url: str = os.getenv(
        "WEB_BASE_URL", "https://stg.gajab.com/"
    )
    gajab_mobile_number: str = os.getenv("GAJAB_MOBILE_NUMBER", "")
    gajab_default_otp: str = os.getenv("GAJAB_DEFAULT_OTP", "123456")
    gajab_pincode: str = os.getenv("GAJAB_PINCODE", "560037")
    gajab_email_recipient: str = os.getenv("GAJAB_EMAIL_RECIPIENT", "")
    appium_server_url: str = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    android_app_path: str = os.getenv("ANDROID_APP_PATH", "apps/gajab-hackathon-sep4.apk")
    android_device_name: str = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
    android_udid: str = os.getenv("ANDROID_UDID", "")
    android_platform_version: str = os.getenv("ANDROID_PLATFORM_VERSION", "")
    android_app_package: str = os.getenv("ANDROID_APP_PACKAGE", "")
    android_app_activity: str = os.getenv("ANDROID_APP_ACTIVITY", "")


settings = Settings()