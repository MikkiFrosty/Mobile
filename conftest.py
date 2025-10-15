
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

def _val(*names, default=None):
    for n in names:
        v = os.getenv(n)
        if v and str(v).strip():
            return v.strip()
    return default

def _endpoint_bstack():
    user = _val("BROWSERSTACK_USERNAME", "BS_USERNAME", "BSTACK_USERNAME")
    key  = _val("BROWSERSTACK_ACCESS_KEY", "BS_ACCESS_KEY", "BSTACK_ACCESS_KEY")
    host = _val("BROWSERSTACK_HOST", default="hub.browserstack.com")
    if user and key:
        return f"https://{user}:{key}@{host}/wd/hub"
    return f"https://{host}/wd/hub"

def _create_bstack_driver():
    # Accept multiple aliases and provide SAFE defaults to avoid 'MISSING_CAPS'
    device = _val("DEVICE_NAME", "BS_DEVICE", "BSTACK_DEVICE", "BROWSERSTACK_DEVICE", default="Google Pixel 7")
    os_version = _val("OS_VERSION", "BS_OS_VERSION", "BSTACK_OS_VERSION", "BROWSERSTACK_OS_VERSION", default="13.0")
    app_id = _val("APP", "BROWSERSTACK_APP_ID")

    desired_caps = {
        "platformName": "Android",
        "deviceName": device,
        "os_version": os_version,
        "app": app_id,  # может быть None — тогда BS вернёт понятную ошибку 'app required'
        "automationName": "UiAutomator2",
        "project": "QA-GURU Mobile",
        "build": _val("BS_BUILD_NAME", default="Default Build"),
        "name": _val("BS_SESSION_NAME", default="Pytest Session"),
        "autoGrantPermissions": True,
        "newCommandTimeout": 120
    }

    cap_copy = desired_caps.copy()
    if cap_copy.get("app"):
        cap_copy["app"] = cap_copy["app"][:8] + "..."  # маскируем bs://
    allure.attach(str(cap_copy), name="resolved capabilities", attachment_type=allure.attachment_type.TEXT)

    options = UiAutomator2Options().load_capabilities(desired_caps)
    drv = webdriver.Remote(_endpoint_bstack(), options=options)
    return drv

def _create_local_driver():
    desired_caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": _val("ANDROID_DEVICE_NAME", default="Android Emulator"),
        "platformVersion": _val("ANDROID_PLATFORM_VERSION", default="13"),
        "appPackage": _val("ANDROID_APP_PACKAGE", default="org.wikipedia.alpha"),
        "appActivity": _val("ANDROID_APP_ACTIVITY", default="org.wikipedia.main.MainActivity"),
        "autoGrantPermissions": True,
        "newCommandTimeout": 120,
    }
    options = UiAutomator2Options().load_capabilities(desired_caps)
    server = _val("APPIUM_SERVER", default="http://127.0.0.1:4723/wd/hub")
    drv = webdriver.Remote(server, options=options)
    return drv

def _use_bstack_by_default():
    env = os.getenv("ENV")
    return not (env and env.strip().lower() == "local")

@pytest.fixture(scope="function")
def mobile_driver():
    bstack = _use_bstack_by_default()
    with allure.step(f"Инициализация драйвера ({'BrowserStack' if bstack else 'Local'})"):
        drv = _create_bstack_driver() if bstack else _create_local_driver()
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
        # Вideo link for BS
        if bstack:
            user = _val("BROWSERSTACK_USERNAME", "BS_USERNAME", "BSTACK_USERNAME")
            key  = _val("BROWSERSTACK_ACCESS_KEY", "BS_ACCESS_KEY", "BSTACK_ACCESS_KEY")
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
