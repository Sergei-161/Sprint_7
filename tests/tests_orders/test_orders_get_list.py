import requests
import allure
import pytest
from urls import Urls


class TestOrdersGetList:

    @allure.title('Проверка получения списка заказов')
    @allure.description('Проверяются код и тело ответа.')
    def test_orders_get_list(self):
        with allure.step('Отправка GET запроса для получения списка заказов'):
            response = requests.get(Urls.URL_orders_list)

        # Проверка успешного ответа (код 200)
        assert response.status_code == 200
        # Проверка что в теле ответа возвращается список заказов
        assert type(response.json()['orders']) == list
        # Проверка что список не пустой и содержит заказы с id
        assert len(response.json()['orders']) > 0 and 'id' in response.json()['orders'][0]