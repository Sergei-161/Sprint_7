import requests
import allure
import pytest
from urls import Urls
import helpers as h


class TestCourierCreate:

    @allure.title('Проверка создания аккаунта курьера с валидными данными')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_create_courier_account(self, new_courier):
        # Фикстура new_courier уже создала курьера, проверяем что данные вернулись
        assert 'data' in new_courier and 'id' in new_courier

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    @allure.description('Проверяются код и тело ответа.')
    def test_create_courier_account_login_conflict(self, new_courier):
        # Пытаемся создать второго курьера с тем же логином
        payload_conflict = {
            'login': new_courier['data']['login'],
            'password': h.create_random_password(),
            'firstName': h.create_random_firstname()
        }

        with allure.step('Попытка создания второго курьера с тем же логином'):
            response = requests.post(Urls.URL_courier_create, data=payload_conflict)

        # Проверка конфликта (код 409) и сообщения об ошибке
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_impossibility_create_two_similar(self):
        # Создаем уникальные данные для курьера
        payload = {
            'login': h.create_random_login(),
            'password': h.create_random_password(),
            'firstName': h.create_random_firstname()
        }

        with allure.step('Первое создание курьера (должно быть успешным)'):
            first_response = requests.post(Urls.URL_courier_create, data=payload)

        with allure.step('Второе создание курьера с теми же данными (должно вызвать ошибку)'):
            second_response = requests.post(Urls.URL_courier_create, data=payload)

        # Проверка: первый успешен, второй возвращает ошибку конфликта
        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert second_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка получения ошибки при создании курьера с незаполненными обязательными полями')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': h.create_random_password(), 'firstName': h.create_random_firstname()},
        {'login': h.create_random_login(), 'password': '', 'firstName': h.create_random_firstname()}
    ])
    def test_create_courier_account_with_empty_required_fields(self, empty_credentials):
        with allure.step('Отправка запроса с незаполненными обязательными полями'):
            response = requests.post(Urls.URL_courier_create, data=empty_credentials)

        # Проверка ошибки валидации (код 400) и сообщения
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"