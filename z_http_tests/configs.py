
url_base = "http://127.0.0.1:8000/api"
email_base = "myTester{}@gmail.com"
name_base = "Nome examplo {}"
password = "mytester123"
urls_tests = []

from random import randint
import logging


def generate_cpf():
    """
        Gera um CPF válido
    """
    cpf = [randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)

admin1 = {
    "email": email_base.format('admin1'),
    "username": email_base.format('admin1'),
    "deviceid": generate_cpf(),
    "cpf": generate_cpf(),
    "name": name_base.format('admin1'),
    "password": password,
    "confirm_password": password
}

admin2 = {
    "email": email_base.format('admin2'),
    "username": email_base.format('admin2'),
    "deviceid": generate_cpf(),
    "cpf": generate_cpf(),
    "name": name_base.format('admin2'),
    "password": password,
    "confirm_password": password
}

# ! A quantidade pontos será a quantidade de admins

prancheteiro1 = {
    "email": email_base.format('prancheteiro1'),
    "username": email_base.format('prancheteiro1'),
    "deviceid": generate_cpf(),
    "cpf": generate_cpf(),
    "name": name_base.format('prancheteiro1'),
    "password": password,
    "confirm_password": password
}

motorista1 = {
    "email": email_base.format('motorista1'),
    "deviceid": generate_cpf(),
    "username": email_base.format('motorista1'),
    "cpf": generate_cpf(),
    "name": name_base.format('motorista1'),
    "password": password,
    "confirm_password": password
}

motorista2 = {
    "email": email_base.format('motorista2'),
    "deviceid": generate_cpf(),
    "username": email_base.format('motorista2'),
    "cpf": generate_cpf(),
    "name": name_base.format('motorista2'),
    "password": password,
    "confirm_password": password
}

motorista3 = {
    "email": email_base.format('motorista3'),
    "deviceid": generate_cpf(),
    "username": email_base.format('motorista3'),
    "cpf": generate_cpf(),
    "name": name_base.format('motorista3'),
    "password": password,
    "confirm_password": password
}
users = []
users.append(admin1)
users.append(admin2)
users.append(prancheteiro1)
users.append(motorista1)
users.append(motorista2)
users.append(motorista3)

points =[]

points.append({
    "name": "Os Ponto admin 1",
    "city":"Rio de Fevereiro",
    "country":"RJ"
})

points.append({
    "name": "Os Ponto admin 2",
    "city":"Brasilia",
    "country":"DF"
})


def request_print(res):
    global urls_tests
    print("method: {} -- url: {} -- status: {}".format(res.request,res.url, res.status_code))
    if res.status_code > 206:
        print(res.content)
    assert res.status_code < 206
    logging.info(res.status_code, " - ",res.url)
    if res.url not in urls_tests:
        urls_tests.append(res.url)
    if res.status_code >= 300:
        logging.warning(res.content)