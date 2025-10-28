import requests
import allure
from urls import Urls


@allure.epic("Управление заказами")
@allure.feature("Принятие заказа курьером")
class TestOrderAccept:
    """Тесты проверки принятия заказа курьером."""

    @allure.title('Проверка успешного принятия заказа курьером')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_accept_success(self, courier_and_order):
        courier_id = courier_and_order['courier']['id']
        order_id = courier_and_order['order']['order_id']

        with allure.step('Отправка запроса на принятие заказа'):
            response = requests.put(f"{Urls.URL_orders_accept}/{order_id}?courierId={courier_id}")

        with allure.step('Проверка успешного ответа'):
            assert response.status_code == 200, f"Ожидался код 200, получено: {response.status_code}"
            response_json = response.json()
            assert response_json == {"ok": True}, f"Неверное тело ответа: {response_json}"

    @allure.title('Проверка ошибки при принятии заказа без id курьера')
    def test_order_accept_error_without_courier_id(self, new_order):
        with allure.step('Попытка принять заказ без указания id курьера'):
            response = requests.put(f"{Urls.URL_orders_accept}/{new_order['order_id']}")

        with allure.step('Проверка тела ошибки'):
            assert response.status_code == 400, f"Ожидался код 400, получено: {response.status_code}"
            response_json = response.json()
            assert "message" in response_json, "Ответ не содержит поля 'message'"
            msg = response_json["message"].lower()
            assert "недостат" in msg or "ошибка" in msg, f"Неожиданное сообщение: {response_json}"

    @allure.title('Проверка ошибки при принятии заказа с неверным id курьера')
    def test_order_accept_error_with_wrong_courier_id(self, new_order):
        wrong_courier_id = "999999999"

        with allure.step('Попытка принять заказ с несуществующим id курьера'):
            response = requests.put(
                f"{Urls.URL_orders_accept}/{new_order['order_id']}?courierId={wrong_courier_id}"
            )

        with allure.step('Проверка тела ошибки'):
            assert response.status_code == 404, f"Ожидался код 404, получено: {response.status_code}"
            response_json = response.json()
            assert "message" in response_json, "Ответ не содержит поля 'message'"
            msg = response_json["message"].lower()
            assert "курьер" in msg and ("не существ" in msg or "не найден" in msg), f"Неожиданное сообщение: {response_json}"

    @allure.title('Проверка ошибки при принятии заказа без id заказа')
    def test_order_accept_error_without_order_id(self, new_courier):
        with allure.step('Попытка принять заказ без указания id заказа'):
            response = requests.put(f"{Urls.URL_orders_accept}/?courierId={new_courier['id']}")

        with allure.step('Проверка тела ошибки'):
            assert response.status_code == 404, f"Ожидался код 404, получено: {response.status_code}"
            response_json = response.json()
            assert "message" in response_json, "Ответ не содержит поля 'message'"
            msg = response_json["message"].lower()
            assert "not found" in msg or "не найден" in msg, f"Неожиданное сообщение: {response_json}"

    @allure.title('Проверка ошибки при принятии заказа с неверным id заказа')
    def test_order_accept_error_with_wrong_order_id(self, new_courier):
        wrong_order_id = "888888888"

        with allure.step('Попытка принять заказ с несуществующим id заказа'):
            response = requests.put(f"{Urls.URL_orders_accept}/{wrong_order_id}?courierId={new_courier['id']}")

        with allure.step('Проверка тела ошибки'):
            assert response.status_code == 404, f"Ожидался код 404, получено: {response.status_code}"
            response_json = response.json()
            assert "message" in response_json, "Ответ не содержит поля 'message'"
            msg = response_json["message"].lower()
            assert "заказ" in msg and ("не существ" in msg or "не найден" in msg), f"Неожиданное сообщение: {response_json}"

