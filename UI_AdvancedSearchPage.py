from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class AdvancedSearchPage:
    def __init__(self, browser):
        self.browser = browser

    def navigate_to_advanced_search(self):
        advanced_search_link = WebDriverWait(self.browser, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/s/']"))
        )
        advanced_search_link.click()

    def switch_to_new_tab_if_needed(self):
        if len(self.browser.window_handles) > 1:
            self.browser.switch_to.window(self.browser.window_handles[-1])

    def filter_by_genre(self, genre_id):
        genre_select = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.NAME, "m_act[genre][]"))
        )
        select = Select(genre_select)
        select.select_by_value(str(genre_id))  # Например, '8' для драмы

    def filter_by_release_year(self, year):
        release_year_input = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.NAME, "m_act[year]"))
        )
        release_year_input.clear()
        release_year_input.send_keys(year)

    def filter_by_company(self, company_name):
        company_select = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.NAME, "m_act[company]"))
        )
        select = Select(company_select)
        select.select_by_visible_text(company_name)

    def filter_by_title(self, title):
        title_input = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.NAME, "m_act[find]"))
        )
        title_input.clear()
        title_input.send_keys(title)

    def filter_by_actor(self, actor_name):
        actor_select = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.NAME, "cr_search_field_1"))
        )
        select = Select(actor_select)
        select.select_by_visible_text(actor_name)

    def submit_search(self):
        submit_button = WebDriverWait(self.browser, 40).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "input.submit.nice_button"))
        )
        submit_button.click()
