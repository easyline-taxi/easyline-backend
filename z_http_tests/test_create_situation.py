import requests
from random import randint
import logging
import pytest
import configs

url_base = configs.url_base
email_base = configs.email_base
name_base = configs.name_base
password = configs.password
urls_tests = configs.urls_tests

print("Test Create Situation")


def generate_cpf():
    """
        Gera um CPF válido
    """
    cpf = [randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)


def reset_tests(users):
    
    for x in users:
        token = 'Bearer {}'.format(x.get('token'))
        headers={'Authorization': token }
        res = requests.post(url=url_base+'/auth/login/',json=x)
        if res.json().get('token',None) is not None:
            token = 'Bearer {}'.format(res.json().get('token'))
            headers={'Authorization': token }
            res = requests.delete(url=url_base+'/user/',headers=headers)
            # print("deleting {} - {}".format(x.get("email"), res.status_code ))
            if res.status_code >= 206:
                print(res.content)
        


users = configs.users

reset_tests(users)



# Registra todos

for x in users:
    res = requests.post(url=url_base+'/auth/register/', json=x)
    configs.request_print(res)
    res = requests.post(url=url_base+'/auth/login/',json=x)
    configs.request_print(res)
    x['token'] = res.json().get('token')


points = configs.points

# Cria os pontos

for i,point in enumerate(points):
    
    token = 'Bearer {}'.format(users[i].get('token'))
    headers={'Authorization': token }
    res = requests.post(url=url_base+'/point/register/', headers=headers, json=point)
    configs.request_print(res)
    point['id'] = res.json().get('data').get('id')
    
    
    # Seleciona o ponto que quer trabalhar
    
    req_point = {
        "point": point['id']
    }
    res = requests.post(url=url_base+'/point/', headers=headers, json=req_point)
    configs.request_print(res)
    
    # Seta coordenadas

    locale = {
    "coordinates": [
            {
            "latitude": 1.96,
            "longitude": 4.57
            },
            {
            "latitude": 6.38,
            "longitude": 7.09
            },
            {
            "latitude": 7.76,
            "longitude": 0.49
            },
            {
            "latitude": 1.72,
            "longitude": 0.23
            },
            {
            "latitude": 1.96,
            "longitude":  4.57
            }
        ]
    }
    res = requests.put(url=url_base+'/admin/config/', headers=headers, json=locale)
    configs.request_print(res)


# ? Adicionar os usuários ADMIN 0

token = 'Bearer {}'.format(users[0].get('token'))
headers={'Authorization': token }
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=configs.prancheteiro1)
configs.request_print(res)
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=configs.motorista1)
configs.request_print(res)

# Troca usuário para cargo de prancheteiro
payload = {
    "function": "P",
    "email": configs.prancheteiro1.get('email')
}
res = requests.put(url=url_base+'/admin/transfer/',headers=headers, json = payload)
configs.request_print(res)


# Coloca os usuários nos respectivos pontos para trabalhar
point = {
    "point": points[0]['id']
}
headers={'Authorization': 'Bearer '+configs.prancheteiro1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
configs.request_print(res)
headers={'Authorization': 'Bearer '+configs.motorista1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
configs.request_print(res)



# ? Adicionar os usuários ADMIN 1

token = 'Bearer {}'.format(users[1].get('token'))
headers={'Authorization': token }


# Adiciona os usuários
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=configs.motorista1)
configs.request_print(res)
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=configs.motorista2)
configs.request_print(res)
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=configs.prancheteiro1)
configs.request_print(res)

payload = {
    "function": "P",
    "email": configs.prancheteiro1.get('email')
}

res = requests.put(url=url_base+'/admin/transfer/',headers=headers, json = payload)
configs.request_print(res)


# Coloca os usuários nos respectivos pontos
# Seleciona o ponto que quer trabalhar

point = {
    "point": points[1]['id']
}
headers={'Authorization': 'Bearer '+configs.prancheteiro1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
configs.request_print(res)
headers={'Authorization': 'Bearer '+configs.motorista1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
configs.request_print(res)
headers={'Authorization': 'Bearer '+configs.motorista2.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
configs.request_print(res)

print("Urls testadas: ", list(map(lambda x: x.replace(url_base,''),urls_tests)))

print("Test Create Situation Completed")