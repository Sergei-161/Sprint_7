import pytest
import requests
import allure
from data.data import TestOrderData
from urls import Urls


@allure.epic("Создание заказов")
@allure.feature("Создание заказа с разными параметрами цвета")
class TestCreateOrderColor:
    """Сьют тестов для проверки создания заказа с различными параметрами цвета."""

    @allure.title("Создание заказа с параметрами цвета")
    @allure.description(
        "Система должна позволять указать один, оба или ни одного цвета самоката. "
        "Тест передает данные: серый, черный, оба цвета, без цвета. "
        "Проверяется код ответа и наличие track в ответе."
    )
    @pytest.mark.parametrize("order_data", TestOrderData.all_orders)
    def test_order_create_color_parametrize_success(self, order_data):
        """Проверка успешного создания заказа с разными цветами."""
        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(Urls.URL_orders_create, json=order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 201, (
                f"Неверный код ответа: {response.status_code}, тело: {response.text}"
            )

        with allure.step('Проверка наличия track в ответе'):
            response_json = response.json()
            assert "track" in response_json, "Ответ не содержит track номера"
