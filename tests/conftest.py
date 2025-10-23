import pytest
import requests
import json
import allure
import helpers as h
from urls import Urls
from data import TestOrderData


@pytest.fixture
def new_courier():
    """Универсальная фикстура для создания курьера"""
    courier_data = {
        'login': h.create_random_login(),
        'password': h.create_random_password(),
        'firstName': h.create_random_firstname()
    }

    with allure.step('Создание курьера для теста'):
        create_response = requests.post(Urls.URL_courier_create, data=courier_data)
        assert create_response.status_code == 201

    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = login_response.json()["id"]

    yield {
        'data': courier_data,
        'id': courier_id
    }

    # После выполнения теста — удаляем курьера
    with allure.step('Удаление курьера после теста'):
        delete_response = requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
        assert delete_response.status_code in [200, 202, 204,404], (
            f"Ошибка при удалении курьера: {delete_response.text}"
        )

@pytest.fixture
def new_order():
    """Универсальная фикстура для создания заказа"""
    order_payload = json.dumps(TestOrderData.order_data_grey)
    headers = {'Content-Type': 'application/json'}

    with allure.step('Создание заказа'):
        create_response = requests.post(Urls.URL_orders_create, data=order_payload, headers=headers)
        track_id = create_response.json()["track"]

    with allure.step('Получение id заказа по track номеру'):
        get_response = requests.get(f"{Urls.URL_orders_get}?t={track_id}")
        order_id = get_response.json()['order']['id']

    return {
        'track_id': track_id,
        'order_id': order_id
    }


@pytest.fixture
def courier_and_order(new_courier, new_order):
    """Универсальная фикстура для создания курьера и заказа"""
    return {
        'courier': new_courier,
        'order': new_order
    }


@pytest.fixture(params=TestOrderData.all_orders)
def order_data(request):
    """Фикстура для параметризации данных заказа"""
    return request.param