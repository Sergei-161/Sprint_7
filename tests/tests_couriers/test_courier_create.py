import requests
import allure
import pytest
from urls import Urls
import helpers as h


@pytest.fixture
def courier_data():
    """Фикстура подготавливает данные для создания курьера (предусловие)."""
    return {
        'login': h.create_random_login(),
        'password': h.create_random_password(),
        'firstName': h.create_random_firstname()
    }


class TestCourierCreate:

    @allure.title('Проверка создания аккаунта курьера с валидными данными')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_create_courier_account(self, courier_data):
        """Тест выполняет само действие — создание курьера."""
        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(Urls.URL_courier_create, data=courier_data)

        with allure.step('Проверка успешного создания курьера'):
            assert response.status_code == 201, f"Некорректный код ответа: {response.text}"
            assert response.json().get('ok') is True, f"Некорректное тело ответа: {response.text}"

        with allure.step('Авторизация созданного курьера для проверки доступности'):
            login_resp = requests.post(Urls.URL_courier_login, data={
                'login': courier_data['login'],
                'password': courier_data['password']
            })
            assert login_resp.status_code == 200, f"Не удалось авторизовать курьера: {login_resp.text}"
            courier_id = login_resp.json().get("id")
            assert courier_id is not None, "В ответе не вернулся id курьера"

        with allure.step('Удаление курьера после теста'):
            delete_resp = requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
            assert delete_resp.status_code in [200, 202, 204], f"Не удалось удалить курьера: {delete_resp.text}"

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    @allure.description('Проверяются код и тело ответа.')
    def test_create_courier_account_login_conflict(self, courier_data):
        """Создаём курьера, затем пробуем создать второго с тем же логином."""
        with allure.step('Создание первого курьера'):
            first_resp = requests.post(Urls.URL_courier_create, data=courier_data)
            assert first_resp.status_code == 201

        with allure.step('Создание второго курьера с тем же логином'):
            conflict_data = {
                'login': courier_data['login'],
                'password': h.create_random_password(),
                'firstName': h.create_random_firstname()
            }
            second_resp = requests.post(Urls.URL_courier_create, data=conflict_data)

        with allure.step('Проверка кода и текста ошибки'):
            assert second_resp.status_code == 409
            assert second_resp.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_impossibility_create_two_similar(self, courier_data):
        with allure.step('Первое создание курьера (ожидаем успех)'):
            first_response = requests.post(Urls.URL_courier_create, data=courier_data)
            assert first_response.status_code == 201

        with allure.step('Второе создание курьера с теми же данными (ожидаем конфликт)'):
            second_response = requests.post(Urls.URL_courier_create, data=courier_data)
            assert second_response.status_code == 409
            assert second_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка получения ошибки при создании курьера с незаполненными обязательными полями')
    @allure.description('Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': h.create_random_password(), 'firstName': h.create_random_firstname()},
        {'login': h.create_random_login(), 'password': '', 'firstName': h.create_random_firstname()}
    ])
    def test_create_courier_account_with_empty_required_fields(self, empty_credentials):
        with allure.step('Отправка запроса с пустыми обязательными полями'):
            response = requests.post(Urls.URL_courier_create, data=empty_credentials)

        with allure.step('Проверка ответа при отсутствии обязательных данных'):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
