class TestData:
    # Статические данные для тестов, где нужно использовать существующие учетки
    correct_login = "Alex2025"
    correct_password = "secret123"
    correct_first_name = "Alex"
    valid_courier_credentials = {"login": "Alex2025", "password": "secret123", "firstName": "Alex"}
    courier_without_firstname = {"login": "Alex2025", "password": "1234"}
    courier_wrong_password = {"login": "Alex2025", "password": "invalid"}


class TestOrderData:
    order_data_grey = {
        "firstName": "Александр",
        "lastName": "Корбин",
        "address": "Шолоховский проспект, 17",
        "metroStation": 7,
        "phone": "+7 908 333 56 99",
        "rentTime": 2,
        "deliveryDate": "2025-10-26",
        "comment": "Ну-с..прокатимся наконец-то?!",
        "color": [
            "GREY"
        ]
    }

    order_data_black = {
        "firstName": "Иоганн",
        "lastName": "Себастьян",
        "address": "Москва, улица Колотушкина, 67",
        "metroStation": 10,
        "phone": "+7 988 888 67 90",
        "rentTime": 4,
        "deliveryDate": "2025-10-23",
        "comment": "Маэстро,быстрей вези мой байк.",
        "color": [
            "BLACK"
        ]
    }

    order_data_two_colors = {
        "firstName": "Михаил",
        "lastName": "Гельфант",
        "address": "Москва, ул.Бульвар Комарова, 99",
        "metroStation": 25,
        "phone": "+7 900 333 33 33",
        "rentTime": 1,
        "deliveryDate": "2025-10-31",
        'comment': "Давай мне в двух цветах и тыкву для Хэллоуина!",
        "color": [
            "BLACK", "GREY"
        ]
    }

    order_data_no_colors = {
        "firstName": "Adriano",
        "lastName": "Chelentano",
        "address": "Milan, Maestro street",
        "metroStation": 20,
        "phone": "+7 670 567 89 10",
        "rentTime": 3,
        "deliveryDate": "2025-10-18",
        "comment": "Оо,мама мия..жду не дождусь!",
        "color": []
    }
    all_orders = [
        order_data_grey,
        order_data_black,
        order_data_two_colors,
        order_data_no_colors
    ]