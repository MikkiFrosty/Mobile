from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

@allure.title("Поиск статьи в Wikipedia")
def test_search_article(driver):
    with allure.step("Открыть поиск"):
        search = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search.click()

    with allure.step("Ввести запрос"):
        field = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        field.send_keys("BrowserStack")

    with allure.step("Проверить, что появились результаты"):
        results = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.TextView"))
        )
        assert len(results) > 0
        assert results[0].is_displayed()