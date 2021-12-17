from rest_framework import exceptions
import json

def check_action(data):

    if not data.get('action',None):
        raise exceptions.NotAcceptable(detail="Campo Action Necessário")

    return True
