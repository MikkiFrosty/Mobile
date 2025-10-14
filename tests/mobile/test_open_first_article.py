import pytest, allure
from appium.webdriver.common.appiumby import AppiumBy

pytestmark = pytest.mark.mobile

@allure.title("Открытие статьи из подсказок")
def test_open_first_article(mobile_driver):
    d = mobile_driver
    d.find_element(AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia").click()
    search = d.find_element(AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
    search.send_keys("Python")
    items = d.find_elements(AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
    assert items, "Подсказки не появились"
    items[0].click()
    title = d.find_elements(AppiumBy.ID, "org.wikipedia.alpha:id/view_page_title_text")
    assert title, "Заголовок статьи не найден"
