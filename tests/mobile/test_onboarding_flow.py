import pytest, allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.mobile
# константы — можно оставить рядом с тестом или наверху файла
FORWARD_ID   = "org.wikipedia.alpha:id/fragment_onboarding_forward_button"  # Continue/Next
DONE_ID      = "org.wikipedia.alpha:id/fragment_onboarding_done_button"     # Done / Get started
INDICATOR_ID = "org.wikipedia.alpha:id/view_onboarding_page_indicator"      # "Page X of 4"

@allure.title("Проход через онбординг (если он есть)")
def test_onboarding_flow(driver):
    wait = WebDriverWait(driver, 10)
    by = AppiumBy.ID
    expected_pages = 4

    for i in range(1, expected_pages):
        with allure.step(f"Onboarding: страница {i} из {expected_pages} — жмём Continue"):
            indicator = driver.find_elements(by, INDICATOR_ID)
            if indicator:
                assert f"Page {i} of {expected_pages}" in (indicator[0].text or ""), \
                    f"Ожидали 'Page {i} of {expected_pages}', получили: {indicator[0].text!r}"
            wait.until(EC.element_to_be_clickable((by, FORWARD_ID))).click()

    with allure.step("Onboarding: финальный экран — жмём Done"):
        wait.until(EC.element_to_be_clickable((by, DONE_ID))).click()

    # дальше — твои шаги после онбординга (оставь как у тебя)
    with allure.step("Проверяем наличие поиска"):
        d.find_element(AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")
