import requests
import allure
from urls import Urls


class TestOrderGetByTrack:

    @allure.title('Проверка успешного получения заказа по номеру')
    def test_order_get_by_track_success(self, new_order):
        with allure.step('Получение заказа по track номеру'):
            get_response = requests.get(f"{Urls.URL_orders_get}?t={new_order['track_id']}")

        # Проверка успешного получения заказа (код 200) и наличия объекта заказа
        assert get_response.status_code == 200 and 'order' in get_response.json()

    @allure.title('Проверка ошибки при получении заказа без номера')
    def test_order_get_by_track_error_without_track(self):
        with allure.step('Попытка получить заказ без указания track номера'):
            get_response = requests.get(f"{Urls.URL_orders_get}")

        # Проверка ошибки (код 400)
        assert get_response.status_code == 400

    @allure.title('Проверка ошибки при получении заказа с несуществующим номером')
    def test_order_get_by_track_error_with_wrong_track(self):
        # Использование несуществующего track номера
        wrong_track_id = "999999999"

        with allure.step('Попытка получить заказ с несуществующим track номером'):
            get_response = requests.get(f"{Urls.URL_orders_get}?t={wrong_track_id}")

        # Проверка ошибки "заказ не найден" (код 404)
        assert get_response.status_code == 404