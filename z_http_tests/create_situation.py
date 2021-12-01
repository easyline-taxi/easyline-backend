import requests
from random import randint

url_base = "http://127.0.0.1:8000/api"
# url_base = "http://easyline.ml/api"
email_base = "myTester{}@gmail.com"
name_base = "Nome examplo {}"
password = "mytester123"



def generate_cpf():
    """
        Gera um CPF válido
    """
    cpf = [randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)

users = []
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

users.append(admin1)
users.append(admin2)
users.append(prancheteiro1)
users.append(motorista1)
users.append(motorista2)


# Registra todos

for x in users:
    res = requests.post(url=url_base+'/auth/register/', json=x)
    res = requests.post(url=url_base+'/auth/login/',json=x)
    x['token'] = res.json().get('token')
    
    

ponto1 = {
    "name": "Os Ponto admin 1",
    "city":"Rio de Fevereiro",
    "country":"RJ"
}

ponto2 = {
    "name": "Os Ponto admin 2",
    "city":"Rio de Janeiro",
    "country":"DF"
}

# Cria os pontos

token = 'Bearer {}'.format(users[0].get('token'))
headers={'Authorization': token }
res = requests.post(url=url_base+'/point/register/', headers=headers, json=ponto1)
ponto1['id'] = res.json().get('data').get('id')

# Seleciona o ponto que quer trabalhar
point = {
    "point": ponto1['id']
}
res = requests.post(url=url_base+'/point/', headers=headers, json=point)



# Adicionar os usuários
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=prancheteiro1)
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=motorista1)

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


# Troca usuário para cargo de prancheteiro

payload = {
    "function": "P",
    "email": prancheteiro1.get('email')
}

res = requests.put(url=url_base+'/admin/transfer/',headers=headers, json = payload)


# Coloca os usuários nos respectivos pontos

# Seleciona o ponto que quer trabalhar
point = {
    "point": ponto1['id']
}
headers={'Authorization': 'Bearer '+prancheteiro1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
headers={'Authorization': 'Bearer '+motorista1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)


token = 'Bearer {}'.format(users[1].get('token'))
headers={'Authorization': token }
res = requests.post(url=url_base+'/point/register/', headers=headers, json=ponto2)
ponto2['id'] = res.json().get('data').get('id')

# Seleciona o ponto que quer trabalhar
point = {
    "point": ponto2['id']
}

res = requests.post(url=url_base+'/point/', headers=headers, json=point)

# Adiciona os usuários
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=motorista1)
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=motorista2)
res = requests.post(url=url_base+'/admin/actions/', headers=headers, json=prancheteiro1)

payload = {
    "function": "P",
    "email": prancheteiro1.get('email')
}

res = requests.put(url=url_base+'/admin/transfer/',headers=headers, json = payload)

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

# Coloca os usuários nos respectivos pontos
# Seleciona o ponto que quer trabalhar

point = {
    "point": ponto2['id']
}
headers={'Authorization': 'Bearer '+prancheteiro1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
headers={'Authorization': 'Bearer '+motorista1.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)
headers={'Authorization': 'Bearer '+motorista2.get('token') }
res = requests.post(url=url_base+'/point/', headers=headers, json=point)