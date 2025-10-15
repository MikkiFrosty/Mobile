import os
import pytest
import allure
import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

def load_env():
    env_context = os.getenv("ENV_CONTEXT")
    if env_context and os.path.exists(f".env.{env_context}"):
        load_dotenv(f".env.{env_context}")
    else:
        load_dotenv(".env")

load_env()

def _create_bstack_driver():
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
    drv = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    return drv

def _create_local_driver():
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
    drv = webdriver.Remote(appium_server, options=options)
    return drv

def _is_bstack_mode():
    # DEFAULT: BrowserStack, unless ENV explicitly set to 'local'
    env = os.getenv("ENV")
    if env and env.strip().lower() == "local":
        return False
    return True

def _attach_bstack_video(session_id: str):
    user = os.getenv("BROWSERSTACK_USERNAME")
    key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    if not (user and key):
        return
    try:
        url = f"https://api.browserstack.com/app-automate/sessions/{session_id}.json"
        resp = requests.get(url, auth=(user, key), timeout=10)
        if resp.status_code == 200:
            video_url = resp.json().get("automation_session", {}).get("video_url")
            if video_url:
                allure.attach(video_url, name="BrowserStack video", attachment_type=allure.attachment_type.URI_LIST)
    except Exception as e:
        allure.attach(str(e), name="bs_video_error", attachment_type=allure.attachment_type.TEXT)

@pytest.fixture(scope="function")
def mobile_driver():
    bstack = _is_bstack_mode()
    endpoint = "hub.browserstack.com" if bstack else os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")

    with allure.step(f"Инициализация драйвера ({'BrowserStack' if bstack else 'Local'})"):
        drv = _create_bstack_driver() if bstack else _create_local_driver()
        allure.attach(f"env={'bstack' if bstack else 'local'}\nendpoint={endpoint}",
                      name="driver context", attachment_type=allure.attachment_type.TEXT)

    try:
        yield drv
    finally:
        # attachments
        try:
            allure.attach(drv.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
        try:
            allure.attach(drv.page_source, name="page source", attachment_type=allure.attachment_type.XML)
        except Exception:
            pass
        if bstack:
            _attach_bstack_video(drv.session_id)
        drv.quit()

# Alias for tests that expect `driver`
@pytest.fixture(scope="function")
def driver(mobile_driver):
    return mobile_driver
