from faker import Faker

fake_en = Faker()  # отдельный экземпляр для английского
fake_ru = Faker(locale='ru_RU')  # отдельный экземпляр для русского


def create_random_login():
    login = fake_en.text(max_nb_chars=7) + str(fake_en.random_int(0, 999))  # используем fake_en
    return login


def create_random_password():
    password = fake_en.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)  # используем fake_en
    return password


def create_random_firstname():
    first_name = fake_ru.first_name()  # используем fake_ru
    return first_name


def create_random_courier_data():
    """Создает полный набор случайных данных для курьера"""
    return {
        'login': create_random_login(),
        'password': create_random_password(),
        'firstName': create_random_firstname()
    }