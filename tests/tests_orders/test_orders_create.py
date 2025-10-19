import requests
import allure
import json
from urls import Urls


class TestOrderCreate:

    @allure.title('Проверка создания заказа с разными параметрами цвета')
    @allure.description('Согласно требованиям, система должна позволять указать в заказе один цвет самоката, выбрать '
                        'сразу оба или не указывать совсем. В тест по очереди передаются наборы данных с разными '
                        'параметрами: серый, черный, оба цвета, цвет не указан. Проверяются код и тело ответа.')
    def test_order_create_color_parametrize_success(self, order_data):
        # Преобразование данных в JSON-формат для отправки
        order_data_json = json.dumps(order_data)
        # Установка заголовков для JSON-запроса
        headers = {'Content-Type': 'application/json'}

        with allure.step('Отправка POST запроса на создание заказа'):
            response = requests.post(Urls.URL_orders_create, data=order_data_json, headers=headers, timeout=5)

        # Проверка успешного создания заказа (код 201) и наличия track-номера
        assert response.status_code == 201 and 'track' in response.text