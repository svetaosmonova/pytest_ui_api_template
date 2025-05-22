import allure
from Ui_main_page import MainPage
from UI_AdvancedSearchPage import AdvancedSearchPage
from UI_SearchResultsPage import SearchResultsPage
import pytest


@pytest.mark.ui
@allure.feature("Поиск фильмов")
@allure.story("Тестирование поиска по названию фильма")
def test_search_movies_by_title(browser):
    with allure.step("Создание объекта MainPage"):
        main_page = MainPage(browser)

    with allure.step("Переход на главную страницу"):
        main_page.open()

    with allure.step("Выполнение поиска по фильму \"Аватар\""):
        main_page.search_by_title("Аватар")

    with allure.step("Проверка наличия искомого фильма в результатах поиска"):
        found = main_page.verify_search_result_contains("Аватар")
        if not found:
            screenshot_name = "no_movie_found.png"
            browser.save_screenshot(screenshot_name)
            allure.attach.file(screenshot_name, attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Фильм не найден.")

    assert found, "Фильм не найден"


@pytest.mark.ui
@allure.feature("Расширенный поиск фильмов")
@allure.story("Поиск фильмов по жанрам")
def test_search_movies_by_genre(browser):
    main_page = MainPage(browser)
    adv_search_page = AdvancedSearchPage(browser)
    results_page = SearchResultsPage(browser)

    with allure.step("Переходим на главную страницу"):
        main_page.open()

    with allure.step("Переходим на страницу расширенного поиска"):
        adv_search_page.navigate_to_advanced_search()

    with allure.step("Выбираем жанр 'Драма' (код жанра '8')"):
        adv_search_page.filter_by_genre('8')

    with allure.step("Отправляем запрос на поиск"):
        adv_search_page.submit_search()

    with allure.step("Ожидание загрузки результатов поиска"):
        results_page.wait_for_results()

    with allure.step("Получаем список фильмов из результатов поиска"):
        movies = results_page.get_movie_list()

    with allure.step("Проверяем наличие фильмов в списке результатов"):
        assert len(movies) > 0, "Нет фильмов в результатах поиска."


@pytest.mark.ui
@allure.feature("Расширенный поиск фильмов")
@allure.story("Фильтрация фильмов по году выпуска")
def test_filter_movies_by_release_year(browser):
    main_page = MainPage(browser)
    adv_search_page = AdvancedSearchPage(browser)
    results_page = SearchResultsPage(browser)

    with allure.step("Переход на главную страницу"):
        main_page.open()

    with allure.step("Переход на страницу расширенного поиска"):
        adv_search_page.navigate_to_advanced_search()

    with allure.step("Выбор года выпуска '2019'"):
        adv_search_page.filter_by_release_year("2019")

    with allure.step("Отправка запроса на поиск"):
        adv_search_page.submit_search()

    with allure.step("Ожидание загрузки результатов поиска"):
        results_page.wait_for_results()

    with allure.step("Получение списка фильмов из результатов поиска"):
        movies = results_page.get_movie_list()

    with allure.step("Проверка наличия фильмов в списке результатов"):
        assert len(movies) > 0, "Нет фильмов в результатах поиска."


@pytest.mark.ui
@allure.feature("Расширенный поиск фильмов")
@allure.story("Фильтрация фильмов по прокатчику")
def test_filter_movies_by_company(browser):
    main_page = MainPage(browser)
    adv_search_page = AdvancedSearchPage(browser)
    results_page = SearchResultsPage(browser)

    with allure.step("Переход на главную страницу"):
        main_page.open()

    with allure.step("Переход на страницу расширенного поиска"):
        adv_search_page.navigate_to_advanced_search()

    with allure.step("Применение фильтра по прокатчику ('A Company')"):
        adv_search_page.filter_by_company("A Company")

    with allure.step("Отправка формы поиска"):
        adv_search_page.submit_search()

    with allure.step("Ожидание загрузки результатов поиска"):
        results_page.wait_for_results()

    with allure.step("Получение списка фильмов из результатов поиска"):
        movies = results_page.get_movie_list()

    with allure.step("Проверка наличия фильмов в результатах поиска"):
        assert len(movies) > 0, "Нет фильмов в результатах поиска."


@pytest.mark.ui
@allure.feature("Расширенный поиск фильмов")
@allure.story("Искать фильм по названию")
def test_filter_movies_by_title(browser):
    main_page = MainPage(browser)
    adv_search_page = AdvancedSearchPage(browser)
    results_page = SearchResultsPage(browser)

    with allure.step("Переход на главную страницу"):
        main_page.open()

    with allure.step("Переход на страницу расширенного поиска"):
        adv_search_page.navigate_to_advanced_search()

    with allure.step("Установка фильтра по названию фильма («Изгой»)"):
        adv_search_page.filter_by_title("Изгой")

    with allure.step("Отправка запроса на поиск"):
        adv_search_page.submit_search()

    with allure.step("Ожидание загрузки результатов поиска"):
        results_page.wait_for_results()

    with allure.step("Получение списка фильмов из результатов поиска"):
        movies = results_page.get_movie_list()

    with allure.step("Проверка наличия фильмов в результатах поиска"):
        assert len(movies) > 0, "Нет фильмов в результатах поиска."


@pytest.mark.ui
@allure.feature("Фильтры фильмов")
@allure.story("Негативный тест фильтрации по некорректному году")
def test_negative_filter_by_incorrect_release_year(browser):
    main_page = MainPage(browser)
    adv_search_page = AdvancedSearchPage(browser)
    results_page = SearchResultsPage(browser)

    with allure.step("Переход на главную страницу"):
        main_page.open()

    with allure.step("Переход на страницу расширенного поиска"):
        adv_search_page.navigate_to_advanced_search()

    with allure.step("Установка фильтра по неверному году выпуска (например, 'abc')"):
        adv_search_page.filter_by_release_year("abc")

    with allure.step("Отправка запроса на поиск"):
        adv_search_page.submit_search()

    with allure.step("Получение списка фильмов из результатов поиска"):
        error = results_page.check_error_message()

    with (allure.step("Проверка отсутствия фильмов в результатах поиска")):
        assert error == ('К сожалению, по вашему запросу ничего не '
        'найдено...') ,"Фильмы были найдены, хотя введен некорректный год выпуска."
