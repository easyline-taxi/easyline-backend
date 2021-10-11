# Backend_EasyLine


## Parte de websocket

### Autenticação é feita na URL de conexão

ws://127.0.0.1:8000/ws/row/?authorization=Bearer <TOKEN JWT>

### OBSERVAÇOES

Qualquer erro por parte das requisições, resulta na desconexão do usuário na aplicação, sendo necessário reconectar!


### As funcionalidades são feitas baseada em JSON

{
    "action":"<FUNCIONALIDADE>",
    "params": {
        <PARAMETRAGEM>
        }
}

### Função atual é a função para setar a localização do usuário

#### SET_LOCALE
seta a sua localização atual

PARAMS: 
{
        "coordinate":"(1.96,4.57)"
    }

----

{
    "action":"SET_LOCALE",
    "params": {
        "coordinate":"(40.4196863603187,20.8270955825833)"
        }
}


Dentro dessa funcionalidade, qualquer usuário que entrar dentro do ponto, automaticamente entra na fila, ao menos que esteja tripulado

caso o usuário saia do range do ponto, então ele é colocado como ausente.
#### GET_ROW
pega a fila atual de objetos usuários

PARAMS:
NONE


