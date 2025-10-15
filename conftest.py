
import os
import pytest
import allure
import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

def load_env():
    env_context = os.getenv("ENV_CONTEXT")
    if env_context:
        env_file = f".env.{env_context}"
        if os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            load_dotenv(".env")
    else:
        load_dotenv(".env")

load_env()

@pytest.fixture(scope="function")
def driver():
    env_type = os.getenv("ENV", "local")

    if env_type == "bstack":
        desired_caps = {
            "platformName": "Android",
            "deviceName": os.getenv("DEVICE_NAME"),
            "os_version": os.getenv("OS_VERSION"),
            "app": os.getenv("APP"),
            "automationName": "UiAutomator2",
            "project": "QA-GURU Mobile",
            "build": os.getenv("BS_BUILD_NAME", "Default Build"),
            "name": os.getenv("BS_SESSION_NAME", "Pytest Session"),
            "autoGrantPermissions": True,
            "newCommandTimeout": 120
        }

        options = UiAutomator2Options().load_capabilities(desired_caps)
        driver = webdriver.Remote(
            command_executor="http://hub.browserstack.com/wd/hub",
            options=options
        )
    else:
        desired_caps = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
            "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION", "13"),
            "appPackage": os.getenv("ANDROID_APP_PACKAGE", "org.wikipedia.alpha"),
            "appActivity": os.getenv("ANDROID_APP_ACTIVITY", "org.wikipedia.main.MainActivity"),
            "autoGrantPermissions": True,
            "newCommandTimeout": 120,
        }
        options = UiAutomator2Options().load_capabilities(desired_caps)
        appium_server = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")
        driver = webdriver.Remote(appium_server, options=options)

    yield driver

    # Attachments after test
    try:
        png = driver.get_screenshot_as_png()
        allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
        src = driver.page_source
        allure.attach(src, name="page source", attachment_type=allure.attachment_type.XML)

        if env_type == "bstack":
            user = os.getenv("BROWSERSTACK_USERNAME")
            key = os.getenv("BROWSERSTACK_ACCESS_KEY")
            if user and key:
                session_id = driver.session_id
                url = f"https://api.browserstack.com/app-automate/sessions/{session_id}.json"
                try:
                    resp = requests.get(url, auth=(user, key), timeout=10)
                    if resp.status_code == 200:
                        data = resp.json().get("automation_session", {})
                        video_url = data.get("video_url")
                        if video_url:
                            allure.attach(video_url, name="BrowserStack video", attachment_type=allure.attachment_type.URI_LIST)
                except Exception as e:
                    allure.attach(str(e), name="bs_video_error", attachment_type=allure.attachment_type.TEXT)
    finally:
        driver.quit()
