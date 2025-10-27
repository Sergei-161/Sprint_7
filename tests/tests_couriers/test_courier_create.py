import requests
import allure
import pytest
import helpers as h
from urls import Urls


class TestCourierCreate:

    @allure.title('Проверка создания аккаунта курьера с валидными данными')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_create_courier_account(self, new_courier):
        """Создание курьера и проверка успешной авторизации"""
        courier_data = new_courier['data']
        courier_id = new_courier['id']

        with allure.step('Проверка, что курьер создан и доступен для логина'):
            login_resp = requests.post(Urls.URL_courier_login, data={
                'login': courier_data['login'],
                'password': courier_data['password']
            })
            assert login_resp.status_code == 200, f"Не удалось авторизовать курьера: {login_resp.text}"
            assert login_resp.json().get("id") == courier_id

    @allure.title('Проверка ошибки при создании курьера с существующим логином')
    def test_create_courier_login_conflict(self, new_courier):
        """Создаём второго курьера с тем же логином"""
        conflict_data = {
            'login': new_courier['data']['login'],
            'password': h.create_random_password(),
            'firstName': h.create_random_firstname()
        }

        with allure.step('Создание второго курьера с тем же логином'):
            resp = requests.post(Urls.URL_courier_create, data=conflict_data)

        with allure.step('Проверка кода и текста ошибки'):
            assert resp.status_code == 409
            assert resp.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка ошибки при создании курьера с пустыми полями')
    @pytest.mark.parametrize('empty_data', [
        {'login': '', 'password': h.create_random_password(), 'firstName': h.create_random_firstname()},
        {'login': h.create_random_login(), 'password': '', 'firstName': h.create_random_firstname()}
    ])
    def test_create_courier_with_empty_fields(self, empty_data):
        """Создание курьера с незаполненными обязательными полями"""
        with allure.step('Отправка запроса'):
            response = requests.post(Urls.URL_courier_create, data=empty_data)

        with allure.step('Проверка корректного ответа об ошибке'):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
