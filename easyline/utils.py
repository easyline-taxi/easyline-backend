from django.utils import timezone


def genAction(user,action:str,motive:str):
    # Retorna a Action
    return dict({"action": user.name+" - "+action,"id": user.id,"motive": motive,"date": str(timezone.now())})

def genEmployee(user,function:str,name_of_point:str):
    # Adiciona o no histórico do Funcionário
    user.historic=[]
    user.historic.append(genAction(user,"adicionado em "+ name_of_point,function))
    user.save()
    # Retorna a Action
    return dict({"name": str(user.name),"id": user.id,"vtr": user.vtr,"cpf":user.cpf,"deviceid": user.deviceid,"function": function})
