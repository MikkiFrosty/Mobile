import os
import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

if os.getenv("RUN_ENV") == "local":
    load_dotenv("utils/.env.local_emulator")
else:
    load_dotenv("utils/.env.bstack")

@pytest.fixture(scope="session")
def capabilities():
    if os.getenv("RUN_ENV") == "local":
        opts = UiAutomator2Options().load_capabilities({
            "platformName": os.getenv("PLATFORM_NAME", "Android"),
            "deviceName": os.getenv("DEVICE_NAME", "emulator-5554"),
            "appPackage": os.getenv("APP_PACKAGE"),
            "appActivity": os.getenv("APP_ACTIVITY"),
            "noReset": True,
        })
    else:
        opts = UiAutomator2Options().load_capabilities({
            "platformName": "Android",
            "deviceName": os.getenv("BS_DEVICE", "Google Pixel 7"),
            "app": os.getenv("BS_APP_ID"),
            "bstack:options": {
                "projectName": "Wikipedia Android",
                "buildName": "Android Build",
                "sessionName": "SKropotova",
                "debug": True,
                "networkLogs": True,
                "video": True
            }
        })
    return opts


@pytest.fixture(scope="function")
def driver(capabilities, request):
    if os.getenv("RUN_ENV") == "local":
        drv = webdriver.Remote(
            command_executor=os.getenv("APPIUM_SERVER", "http://localhost:4723/wd/hub"),
            options=capabilities
        )
    else:
        username = os.getenv("BROWSERSTACK_USERNAME")
        access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
        assert username and access_key, "BrowserStack credentials not set"

        drv = webdriver.Remote(
            command_executor=f"http://{username}:{access_key}@hub.browserstack.com/wd/hub",
            options=capabilities
        )

    yield drv
    try:
        allure.attach(
            drv.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    finally:
        drv.quit()
