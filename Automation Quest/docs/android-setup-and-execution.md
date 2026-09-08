# Android Setup And Execution

This guide prepares Windows for the Appium Android smoke test in `tests/android/test_android_smoke.py`. The test uses Appium's UiAutomator2 driver and connects to the Appium server at `http://127.0.0.1:4723` by default.

## 1. Install Host Tools

Open PowerShell as Administrator and run:

```powershell
choco install temurin17 -y
choco install androidstudio -y
```

Close and reopen PowerShell after installation. Verify Java is available:

```powershell
java -version
```

Open Android Studio. On the first-run wizard, keep the **Standard** setup. Then open **More Actions > SDK Manager** and install these SDK Tools:

- Android SDK Platform-Tools
- Android SDK Build-Tools
- Android SDK Command-line Tools (latest)
- Android Emulator

Install at least one Android SDK platform, such as the latest stable platform offered in the **SDK Platforms** tab. Record the displayed Android SDK Location, which normally is `%LOCALAPPDATA%\Android\Sdk`.

Set the SDK variables for your user account, then restart PowerShell:

```powershell
$androidSdk = "$env:LOCALAPPDATA\Android\Sdk"
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidSdk, "User")
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", $androidSdk, "User")
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$androidSdk\platform-tools;$androidSdk\emulator", "User")
```

Confirm the Android Debug Bridge is available:

```powershell
adb version
```

## 2. Create Or Connect A Device

For an emulator, in Android Studio open **More Actions > Virtual Device Manager**, create a phone virtual device with the installed system image, and start it. For a physical device, enable Developer options and USB debugging, then accept the computer authorization prompt.

Confirm the connection before continuing:

```powershell
adb devices
```

The output must include one device with the state `device`. Use `emulator -list-avds` to list configured emulator names when needed.

## 3. Prepare The Project

From the workspace root, activate the shared virtual environment and install the pinned Python dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location "Automation Quest"
python -m pip install -r requirements.txt
```

Install the Appium server and Android driver if they are not already installed:

```powershell
npm install -g appium
appium driver install uiautomator2
appium driver list --installed
```

The last command must list `uiautomator2`. The framework requires `Appium-Python-Client==5.1.1`; it is installed by `requirements.txt`.

Copy the environment template and configure the application. Put the supplied APK in `apps\challenge.apk`, or change `ANDROID_APP_PATH` to its local path.

```powershell
Copy-Item .env.example .env
```

For an APK launch, retain these values in `.env` and set the platform version only when a specific version is required:

```dotenv
ANDROID_APP_PATH=apps/challenge.apk
APPIUM_SERVER_URL=http://127.0.0.1:4723
ANDROID_DEVICE_NAME=Android Emulator
ANDROID_PLATFORM_VERSION=
```

To test an already-installed application instead of an APK, leave `ANDROID_APP_PATH` pointing to a nonexistent path and set both package values:

```dotenv
ANDROID_APP_PACKAGE=com.example.application
ANDROID_APP_ACTIVITY=.MainActivity
```

## 4. Start Appium And Execute

Keep the emulator/device running. In one PowerShell window, start Appium:

```powershell
appium
```

In a second PowerShell window, activate the virtual environment, enter `Automation Quest`, and run the Android tests:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location "Automation Quest"
pytest tests/android
```

For the smoke test only:

```powershell
pytest tests/android -m smoke
```

Reports are written to `output\reports\report.html` and `output\reports\junit.xml`. Android failure evidence should be placed under `output\screenshots\` or `output\videos\` when captured by the selected driver/tooling; retain the test name, device, Android version, command, and timestamp with each item.

## Evidence And Defect Handoff

Before reporting a mobile failure as a product defect, rerun it on the documented device or emulator and classify it. Record whether it is a product, automation, environment, test-data, locator, synchronization, or unknown failure. For a reproducible potential product defect, redact and copy the relevant evidence to `..\Bug Quest\evidence\`, then reference the source test and output paths from the Bug Quest report. A driver or locator error alone is not a product defect.

## Troubleshooting

| Symptom | Check or resolution |
| --- | --- |
| `adb` is not recognized | Restart PowerShell after setting the user environment variables. Confirm `%ANDROID_HOME%\platform-tools\adb.exe` exists. |
| No devices in `adb devices` | Start an AVD, reconnect the phone, or run `adb kill-server` followed by `adb start-server`. Accept USB debugging authorization on the phone. |
| Appium cannot find the Android SDK | Confirm `ANDROID_HOME` and `ANDROID_SDK_ROOT` point to the SDK Location from Android Studio. Restart Appium after changing variables. |
| `UiAutomator2` driver is missing | Run `appium driver install uiautomator2`, then confirm it with `appium driver list --installed`. |
| APK cannot be installed | Verify `ANDROID_APP_PATH` is relative to `Automation Quest` or use an absolute path. Ensure the APK supports the emulator/device Android version and CPU architecture. |
| Session fails for an installed app | Set both `ANDROID_APP_PACKAGE` and `ANDROID_APP_ACTIVITY`; obtain them from the application team or inspect the package with `adb shell cmd package resolve-activity --brief <package>`. |