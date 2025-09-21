
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time, os

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

def test_search_article():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "android",
        "platformVersion": "12.0",
        "deviceName": "Samsung Galaxy S22 Ultra",
        "app": "bs://b05576e26d6f90b589e9ff5293c2af443ee75633"
    })

    driver = webdriver.Remote(
        f"http://{USERNAME}:{ACCESS_KEY}@hub.browserstack.com/wd/hub",
        options=options
    )
    with allure.step("Skipping onboarding"):
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
            )
        ).click()
    with allure.step("Article search"):
        search_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()

        search_input = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        search_input.send_keys("Kropotova")
    with allure.step("Checking for search results"):
        time.sleep(5)
        search_results = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        assert len(search_results) > 0
    with allure.step("Click on the article"):
        search_results[1].click()

        driver.quit()
