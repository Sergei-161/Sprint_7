import requests
import allure
from urls import Urls
from data.data import CourierTestData

class TestCourierDelete:

    @allure.title('Проверка успешного удаления курьера')
    def test_courier_delete_success(self, new_courier):
        with allure.step('Отправка DELETE запроса на удаление курьера по id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{new_courier['id']}")
            response_data = delete_response.json()

        # Проверяем статус кода и содержимое ответа
        assert delete_response.status_code == 200, f"Ожидался код 200, получен {delete_response.status_code}"
        assert response_data.get("ok") is True, f"Ожидалось ok=True, получен {response_data}"


    @allure.title('Проверка ошибки при попытке удаления курьера без указания id')
    def test_courier_delete_error_without_id(self):
        with allure.step('Отправка DELETE запроса без ID'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/")
            response_data = delete_response.json()

        # Проверяем статус и сообщение
        assert delete_response.status_code == 404, f"Ожидался код 404, получен {delete_response.status_code}"
        assert "message" in response_data, "Ответ не содержит поле 'message'"
        assert response_data["message"].rstrip('.') in [
            "Недостаточно данных для удаления курьера",
            "Not Found"
        ]


    @allure.title('Проверка ошибки при попытке удаления курьера с несуществующим id')
    def test_courier_delete_error_with_nonexistent_id(self):
        nonexistent_id = CourierTestData.NONEXISTENT_ID

        with allure.step(f'Отправка DELETE запроса с несуществующим id {nonexistent_id}'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{nonexistent_id}")
            response_data = delete_response.json()

        # Проверяем статус и сообщение
        assert delete_response.status_code in [404, 500], f"Ожидался код 404 или 500, получен {delete_response.status_code}"
        assert isinstance(response_data, dict), "Ответ не является JSON-объектом"
        assert any(k in response_data for k in ["message", "error"]), "Ответ не содержит ни 'message', ни 'error'"


    @allure.title('Проверка неуспешного запроса на удаление курьера с некорректным id')
    def test_courier_delete_invalid_id(self):
        invalid_id = CourierTestData.INVALID_ID

        with allure.step(f'Отправка DELETE запроса с некорректным id {invalid_id}'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{invalid_id}")
            response_data = delete_response.json()

        # Проверяем статус и структуру ответа
        assert delete_response.status_code in [400, 404, 500], f"Неожиданный код {delete_response.status_code}"
        assert isinstance(response_data, dict), "Ответ не является JSON-объектом"
        assert any(k in response_data for k in ["message", "error"]), "Ответ не содержит ни 'message', ни 'error'"

