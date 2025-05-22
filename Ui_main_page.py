from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, browser):
        self.browser = browser

    def open(self):
        self.browser.get("https://www.kinopoisk.ru/")

    def click_advanced_search(self):
        icon = WebDriverWait(self.browser, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/s/']"))
        )
        icon.click()

        if len(self.browser.window_handles) > 1:
            self.browser.switch_to.window(self.browser.window_handles[-1])

    def search_by_title(self, title):
        search_field = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, ".kinopoisk-header-search-form-input__input"))
        )
        search_field.send_keys(title)
        search_field.submit()

    def verify_search_result_contains(self, title):
        results_container = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search_results"))
        )
        movie_elements = results_container.find_elements(
            By.CLASS_NAME, "element")
        titles = [elem.find_element(By.CLASS_NAME, "name").text for elem in movie_elements]

        return any(title in t for t in titles)
