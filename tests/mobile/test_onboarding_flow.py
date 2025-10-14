import pytest, allure
from appium.webdriver.common.appiumby import AppiumBy

pytestmark = pytest.mark.mobile

@allure.title("Проход через онбординг (если он есть)")
def test_onboarding_flow(mobile_driver):
    d = mobile_driver
    with allure.step("Кликаем по кнопкам онбординга, если отображаются"):
        next_ids = [
            "org.wikipedia.alpha:id/fragment_onboarding_forward_button",
            "org.wikipedia.alpha:id/fragment_onboarding_forward_button",
            "org.wikipedia.alpha:id/fragment_onboarding_done_button",
        ]
        for _id in next_ids:
            els = d.find_elements(AppiumBy.ID, _id)
            if els:
                els[0].click()
    with allure.step("Проверяем наличие поиска"):
        d.find_element(AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")
