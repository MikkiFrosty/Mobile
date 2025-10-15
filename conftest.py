
import os
import pytest
import allure
import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

def load_env():
    ctx = os.getenv("ENV_CONTEXT")
    if ctx and os.path.exists(f".env.{ctx}"):
        load_dotenv(f".env.{ctx}")
    else:
        load_dotenv(".env")

load_env()

def _endpoint_bstack():
    user = os.getenv("BROWSERSTACK_USERNAME")
    key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    host = os.getenv("BROWSERSTACK_HOST", "hub.browserstack.com")
    if user and key:
        return f"https://{user}:{key}@{host}/wd/hub"
    # Fallback (will likely 401, but we attach a hint)
    allure.attach("BROWSERSTACK_USERNAME/ACCESS_KEY not set -> expect 401 Authorization Required",
                  name="bstack auth warning", attachment_type=allure.attachment_type.TEXT)
    return f"https://{host}/wd/hub"

def _create_bstack_driver():
    app_id = os.getenv("APP") or os.getenv("BROWSERSTACK_APP_ID")
    desired_caps = {
        "platformName": "Android",
        "deviceName": os.getenv("DEVICE_NAME"),
        "os_version": os.getenv("OS_VERSION"),
        "app": app_id,
        "automationName": "UiAutomator2",
        "project": "QA-GURU Mobile",
        "build": os.getenv("BS_BUILD_NAME", "Default Build"),
        "name": os.getenv("BS_SESSION_NAME", "Pytest Session"),
        "autoGrantPermissions": True,
        "newCommandTimeout": 120
    }
    options = UiAutomator2Options().load_capabilities(desired_caps)
    drv = webdriver.Remote(_endpoint_bstack(), options=options)
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
    server = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")
    drv = webdriver.Remote(server, options=options)
    return drv

def _use_bstack_by_default():
    env = os.getenv("ENV")
    return not (env and env.strip().lower() == "local")

@pytest.fixture(scope="function")
def mobile_driver():
    bstack = _use_bstack_by_default()
    endpoint = _endpoint_bstack() if bstack else os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")
    with allure.step(f"Инициализация драйвера ({'BrowserStack' if bstack else 'Local'})"):
        drv = _create_bstack_driver() if bstack else _create_local_driver()
        safe_endpoint = endpoint.replace(os.getenv("BROWSERSTACK_ACCESS_KEY",""), "***") if "@" in endpoint else endpoint
        allure.attach(f"env={'bstack' if bstack else 'local'}\nendpoint={safe_endpoint}",
                      name="driver context", attachment_type=allure.attachment_type.TEXT)
    try:
        yield drv
    finally:
        try:
            allure.attach(drv.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
        try:
            allure.attach(drv.page_source, name="page source", attachment_type=allure.attachment_type.XML)
        except Exception:
            pass
        if bstack:
            user = os.getenv("BROWSERSTACK_USERNAME")
            key = os.getenv("BROWSERSTACK_ACCESS_KEY")
            session_id = getattr(drv, "session_id", None)
            if user and key and session_id:
                try:
                    url = f"https://api.browserstack.com/app-automate/sessions/{session_id}.json"
                    r = requests.get(url, auth=(user, key), timeout=10)
                    if r.status_code == 200:
                        v = r.json().get("automation_session", {}).get("video_url")
                        if v:
                            allure.attach(v, name="BrowserStack video", attachment_type=allure.attachment_type.URI_LIST)
                except Exception:
                    pass
        drv.quit()

@pytest.fixture(scope="function")
def driver(mobile_driver):
    return mobile_driver
