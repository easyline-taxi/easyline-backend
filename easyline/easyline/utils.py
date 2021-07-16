from django.utils import timezone

def genAction(user,action:str,motive:str):
    # Retorna a Action
    return {"action": user.name+" - "+action,"id": user.id,"motive": motive,"date": timezone.now()}

def genEmployee(user,function:str,name_of_point:str):
    # Adiciona o no histórico do Funcionário
    user.historic['historic'].append(genAction(user,"adicionado em "+ name_of_point,function))
    user.save()
    # Retorna a Action
    return {"name": str(user.name),"id": user.id,"vtr": user.vtr,"deviceid": user.deviceid,"function": function}