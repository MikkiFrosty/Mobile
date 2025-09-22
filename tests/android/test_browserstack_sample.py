from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

def test_search_article(driver):
    with allure.step("Skipping onboarding"):
        skip = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
            )
        )
        skip.click()
    with allure.step("Article search"):
        search = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search.click()

    with allure.step("Checking for search results"):
        field = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        field.send_keys("Kropotova")

    with allure.step("Click on the article"):
        results = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.TextView"))
        )
        assert len(results) > 0
        assert results[0].is_displayed()