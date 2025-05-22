from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchResultsPage:
    def __init__(self, browser):
        self.browser = browser

    def wait_for_results(self):
        """Ждет появления результатов поиска."""
        WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search_results"))
        )

    def get_movie_list(self):
        """Возвращает список элементов фильмов на странице результатов."""
        results_container = WebDriverWait(self.browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search_results"))
        )
        return results_container.find_elements(By.CLASS_NAME, "element")

    def check_error_message(self):
        """Проверяет наличие сообщения об ошибке при пустом поиске"""
        error_message = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((
                By.XPATH, "//h2[text()='К сожалению, по вашему запросу ничего не найдено...']"))
        )

        return error_message.text
