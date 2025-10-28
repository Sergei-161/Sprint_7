import pytest
import requests
import json
import allure
import helpers as h
from urls import Urls
from data.data import TestOrderData


@pytest.fixture
def new_courier():
    """Фикстура для создания и последующего удаления курьера."""
    courier_data = {
        'login': h.create_random_login(),
        'password': h.create_random_password(),
        'firstName': h.create_random_firstname()
    }

    with allure.step('Создание курьера'):
        create_response = requests.post(Urls.URL_courier_create, data=courier_data)
        assert create_response.status_code == 201, f"Ошибка при создании курьера: {create_response.text}"

    with allure.step('Авторизация курьера для получения ID'):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = login_response.json().get("id")
        assert courier_id, "Не удалось получить ID курьера"

    yield {
        'data': courier_data,
        'id': courier_id
    }

    with allure.step('Удаление курьера после теста'):
        delete_response = requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
        assert delete_response.status_code in [200, 202, 204, 404], (
            f"Ошибка при удалении курьера: {delete_response.text}"
        )


@pytest.fixture
def new_order():
    """Фикстура для создания и последующего удаления заказа."""
    headers = {'Content-Type': 'application/json'}
    order_payload = json.dumps(TestOrderData.order_data_grey)

    with allure.step('Создание заказа'):
        create_response = requests.post(Urls.URL_orders_create, data=order_payload, headers=headers)
        assert create_response.status_code == 201, f"Ошибка при создании заказа: {create_response.text}"
        track_id = create_response.json().get("track")
        assert track_id, "Не удалось получить track заказа"

    with allure.step('Получение ID заказа по track номеру'):
        get_response = requests.get(f"{Urls.URL_orders_get}?t={track_id}")
        order_id = get_response.json()['order']['id']
        assert order_id, "Не удалось получить ID заказа по track номеру"

    yield {
        'track_id': track_id,
        'order_id': order_id
    }


@pytest.fixture
def courier_and_order(new_courier, new_order):
    """Фикстура, создающая курьера и заказ одновременно."""
    return {
        'courier': new_courier,
        'order': new_order
    }
