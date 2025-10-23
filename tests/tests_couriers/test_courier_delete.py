import requests
import allure
from urls import Urls

class TestCourierDelete:

    @allure.title('Проверка успешного удаления курьера')
    def test_courier_delete_success(self, new_courier):
        with allure.step('Отправка DELETE запроса на удаление курьера по id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{new_courier['id']}")
            response_data = delete_response.json()

        # Проверяем статус кода и содержимое ответа
        assert delete_response.status_code == 200, f"Ожидался код 200, получен {delete_response.status_code}"
        assert response_data == {"ok": True}, f"Ожидалось {{'ok': True}}, получен {response_data}"

    @allure.title('Проверка ошибки при попытке удаления курьера без указания id')
    def test_courier_delete_error_without_id(self):
        with allure.step('Отправка DELETE запроса на удаление с пустым id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/")
            response_data = delete_response.json()

        # Проверяем статус кода и содержимое ответа
        assert delete_response.status_code == 404, f"Ожидался код 404, получен {delete_response.status_code}"


    @allure.title('Проверка ошибки при попытке удаления курьера с несуществующим id')
    def test_courier_delete_error_with_nonexistent_id(self):
        # Создание несуществующего id курьера
        nonexistent_id = "1234567890"

        with allure.step('Отправка DELETE запроса на удаление с несуществующим id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{nonexistent_id}")
            response_data = delete_response.json()

        # Проверяем статус кода и содержимое ответа
        assert delete_response.status_code == 404, f"Ожидался код 404, получен {delete_response.status_code}"


    @allure.title('Проверка неуспешного запроса на удаление курьера')
    def test_courier_delete_unsuccessful_request(self):
        # Отправка запроса на удаление с некорректным id
        invalid_id = "invalid_id_123"

        with allure.step('Отправка DELETE запроса на удаление с некорректным id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{invalid_id}")
            response_data = delete_response.json()

        # Проверяем статус кода и содержимое ответа
        assert delete_response.status_code == 500, f"Ожидался код 500, получен {delete_response.status_code}"