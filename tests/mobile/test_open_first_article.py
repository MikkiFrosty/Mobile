import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from utils.onboarding import skip_onboarding_if_present
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.locators import (
    SEARCH_WIKIPEDIA_ACCESSIBILITY,
    SEARCH_TEXT_INPUT_ID,
    SEARCH_RESULTS_ID,
    FIRST_SEARCH_RESULT_ID,
    ARTICLE_TITLE_ID,
)
pytestmark = pytest.mark.mobile


@allure.title("Открытие первой статьи из поиска (игнорируем попапы)")
def test_open_first_article(mobile_driver):
    driver = mobile_driver
    try:
        driver.execute_script('browserstack_executor: {"action": "setSessionName", "arguments": {"name": \"test_open_first_article"}}')
    except Exception:
        pass
    skip_onboarding_if_present(driver)

    wait = WebDriverWait(driver, 10)

    with allure.step("Открываем поиск"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, SEARCH_WIKIPEDIA_ACCESSIBILITY))).click()

    with allure.step("Вводим запрос"):
        wait.until(EC.presence_of_element_located((AppiumBy.ID, SEARCH_TEXT_INPUT_ID))).send_keys("Python")

    with allure.step("Ждём выдачу и кликаем по первой статье"):
        wait.until(EC.presence_of_element_located((AppiumBy.ID, SEARCH_RESULTS_ID)))
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, FIRST_SEARCH_RESULT_ID))).click()

    with allure.step("Подтверждаем переход на экран статьи"):
        try:
            wait.until(EC.presence_of_element_located((AppiumBy.ID, ARTICLE_TITLE_ID)))
        except TimeoutException:
            wait.until(EC.invisibility_of_element_located((AppiumBy.ID, SEARCH_RESULTS_ID)))
