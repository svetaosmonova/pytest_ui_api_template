import requests
import allure
from config import BASE_URL, HEADERS
from API_Class import ApiClass
import pytest


# Позитивные тесты
@pytest.mark.api
@allure.feature('API')
@allure.story('Возможные значения полей')
def test_get_genres_list():

    api = ApiClass(BASE_URL, HEADERS)
    params = {'field': 'genres.name'}
    resp = api.send_requests("/v1/movie/possible-values-by-field", params)

    with allure.step('Проверка статуса ответа'):
        assert resp.status_code == 200, f'Ошибка: статус {resp.status_code}'

    with allure.step('Логирование тела ответа'):
        allure.attach(resp.text, name='Response Body', attachment_type=allure.attachment_type.TEXT)


@pytest.mark.api
@allure.feature('API')
@allure.story('Поиск фильмов по рейтингу')
def test_search_by_rating():

    api = ApiClass(BASE_URL, HEADERS)
    params = {'rating.imdb': '8-10'}

    with allure.step(f'Запрашиваем фильмы с рейтингом IMDB {params["rating.imdb"]}'):
        resp = api.send_requests('/v1/movie', params)

    with allure.step('Проверяем успешность ответа (ожидаем 200)'):
        assert resp.status_code == 200, f'Ошибка: неверный статус ({resp.status_code})'

    with allure.step('Прикрепляем тело ответа для анализа'):
        allure.attach(str(
            resp.json()), name='Response Body', attachment_type=allure.attachment_type.JSON)


@pytest.mark.api
@allure.feature('API')
@allure.story('Поиск фильма по ID')
def test_search_by_id():
    api = ApiClass(BASE_URL, HEADERS)
    movie_id = 251733

    with allure.step(f'Отправляем GET-запрос для фильма с ID={movie_id}'):
        response = api.send_requests(f"/v1.4/movie/{movie_id}", None)

    with allure.step('Проверяем успешность запроса (ожидаемый статус 200)'):
        assert response.status_code == 200, f'Ошибка: неверный статус ({response.status_code})'

    with allure.step('Проверяем наличие названия фильма («Аватар») в ответе'):
        assert 'Аватар' in response.text, 'Ошибка: название фильма не найдено в ответе.'

    with allure.step('Прикрепляем тело ответа для анализа'):
        allure.attach(
            response.text, name=f'Ответ API для фильма с ID={movie_id}',
            attachment_type=allure.attachment_type.TEXT)


@pytest.mark.api
@allure.feature('API')
@allure.story('Фильтрация фильмов по жанрам')
def test_search_drama_without_crime():

    filters = [
        ('genres.name', '+драма'),
        ('genres.name', '!криминал')
    ]
    api = ApiClass(BASE_URL, HEADERS)

    with allure.step('Отправляем GET-запрос с заданными фильтрами'):
        response = api.send_requests('/v1.4/movie', filters)

    with allure.step('Проверяем успешность запроса (код 200)'):
        assert response.status_code == 200, \
               f'Ошибка! Сервер вернул статус {response.status_code}, ожидался 200'

    with allure.step('Приложение тела ответа для дополнительной диагностики'):
        allure.attach(response.text, name='Тело ответа', attachment_type=allure.attachment_type.TEXT)


@pytest.mark.api
@allure.feature('API')
@allure.story('Фильтрация фильмов')
def test_search_drama_and_crime():

    api_client = ApiClass(BASE_URL, HEADERS)

    with allure.step('Отправляем запрос с фильтром по жанрам "драма" и "криминал"'):
        response = api_client.send_requests('/v1.4/movie', {'genres.name': ['драма', 'криминал']})

    with allure.step('Проверяем успешность запроса (ожидаемый статус 200)'):
        assert response.status_code == 200, f'Ошибка: статус-код отличен от 200 ({response.status_code}).'

    with allure.step('Присоединяем тело ответа для последующего анализа'):
        allure.attach(response.text, name='Body of Response', attachment_type=allure.attachment_type.TEXT)


@pytest.mark.api
@allure.feature('API')
@allure.story('Поиск фильмов по названию')
def test_search_by_title():

    api_client = ApiClass(BASE_URL, HEADERS)

    with allure.step('Отправляем запрос на поиск фильма с названием "Аватар"'):
        response = api_client.send_requests('/v1.4/movie/search', {'page': 1, 'limit': 10, 'query': 'Аватар'})

    with allure.step('Проверяем успешность запроса (ожидаемый статус 200)'):
        assert response.status_code == 200, (f'Ошибка: неправильный статус-код '
                                             f'({response.status_code}), ожидается 200')

    with allure.step('Оцениваем время отклика (не больше 500 мс)'):
        elapsed_time_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_time_ms < 500, f'Ошибка: отклик дольше 500 мс ({elapsed_time_ms:.2f} ms)'

    with allure.step('Логируем тело ответа для дополнительного анализа'):
        allure.attach(response.text, name='Response Body', attachment_type=allure.attachment_type.TEXT)


# Негативные тесты
@pytest.mark.api
@allure.feature('API Authentification')
@allure.story('Ошибка при отсутствии токена')
def test_search_without_token():

    with allure.step('Отправляем запрос без API-токена'):
        api = ApiClass(BASE_URL, {})
        response = api.send_requests('/v1.4/movie/251733', None)

    with allure.step('Проверяем статус ответа (ожидаем 401)'):
        assert response.status_code == 401, f'Ошибка: ожидался статус 401, фактически получил {response.status_code}'

    with allure.step('Проверяем сообщение об ошибке'):
        expected_message = "В запросе не указан токен!"
        assert expected_message in response.text, f'Ошибка: в тексте ответа отсутствует строка "{expected_message}"'

    with allure.step('Сохраняем тело ответа для последующего анализа'):
        allure.attach(response.text, name='Response Text', attachment_type=allure.attachment_type.TEXT)


@pytest.mark.api
@allure.feature('API')
@allure.story('Неправильный HTTP-метод')
def test_wrong_http_method():

    with allure.step('Отправляем запрос методом DELETE'):
        response = requests.delete(f'{BASE_URL}/v1.4/movie/251733', headers=HEADERS)

    with allure.step('Проверяем статус ответа (ожидаем 404)'):
        assert response.status_code == 404, f'Ошибка: ожидался статус 404, реально получили {response.status_code}'

    with allure.step('Проверяем наличие сообщения об ошибке'):
        assert "Cannot DELETE" in response.text, 'Ошибка: в ответе не обнаружено сообщение "Cannot DELETE"'

    with allure.step('Приложили тело ответа для анализа'):
        allure.attach(
            response.text, name='Response Body', attachment_type=allure.attachment_type.TEXT)


@pytest.mark.api
@allure.feature('API')
@allure.story('Проверка диапазона  годов')
def test_old_year_range():

    wrong_years = '1000-1100'
    api = ApiClass(BASE_URL, HEADERS)

    with allure.step(f'Отправляем запрос с неверным диапазоном годов {wrong_years}'):
        response = api.send_requests('/v1.4/movie/random',
                                     {'type': 'cartoon', 'year': wrong_years})

    with allure.step('Проверяем статус ответа (ожидаем 400)'):
        assert response.status_code == 400, (f'Ошибка: ожидался статус 400, '
                                             f'получен {response.status_code}')

    with allure.step('Проверяем сообщение об ошибке'):
        error_message = ("Значение поля year должно "
                         "быть в диапазоне от 1874 до 2050!")
        assert error_message in response.text, (f'Ошибка: не найдено сообщение '
                                                f'"{error_message}" в ответе')

    with allure.step('Приложили тело ответа для анализа'):
        allure.attach(response.text, name='Response Body', attachment_type=allure.attachment_type.TEXT)
