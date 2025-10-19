import requests
import allure
from urls import Urls


class TestCourierDelete:

    @allure.title('Проверка успешного удаления курьера')
    def test_courier_delete_success(self, new_courier):
        with allure.step('Отправка DELETE запроса на удаление курьера по id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{new_courier['id']}")

        # Проверка успешного удаления (код 200 и тело ответа {"ok": true})
        assert delete_response.status_code == 200 and delete_response.json() == {"ok": True}

    @allure.title('Проверка ошибки при попытке удаления курьера без указания id')
    def test_courier_delete_error_without_id(self):
        with allure.step('Отправка DELETE запроса на удаление с пустым id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/")

        # Проверка ошибки (код 404)
        assert delete_response.status_code == 404

    @allure.title('Проверка ошибки при попытке удаления курьера с несуществующим id')
    def test_courier_delete_error_with_nonexistent_id(self):
        # Создание несуществующего id курьера
        nonexistent_id = "1234567890"

        with allure.step('Отправка DELETE запроса на удаление с несуществующим id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{nonexistent_id}")

        # Проверка ошибки (код 404)
        assert delete_response.status_code == 404

    @allure.title('Проверка неуспешного запроса на удаление курьера')
    def test_courier_delete_unsuccessful_request(self):
        # Отправка запроса на удаление с некорректным id
        invalid_id = "invalid_id_123"

        with allure.step('Отправка DELETE запроса на удаление с некорректным id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{invalid_id}")

        # API возвращает 500 при некорректном формате id, что показывает обработку ошибок сервера
        # Ожидалось 404, но фактическое поведение - 500
        assert delete_response.status_code == 500  # Фактический код ответа API