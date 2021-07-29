

from django.db import close_old_connections
# from django.conf import settings
from urllib.parse import parse_qs
# rest framework
from rest_framework_jwt.utils import jwt_decode_handler
from channels.db import database_sync_to_async
from api.models import User

@database_sync_to_async
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        if user != None and user.active:
            return user
    except User.DoesNotExist:
        pass
    return None

class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope,receive = None,send=None):

        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        try:
            token = [x[1].decode("utf8") for x in scope['headers'] if x[0].decode("utf8") == 'authorization']
            token_decoded = jwt_decode_handler(token[0].split(' ')[1])
            user = await get_user(token_decoded['user_id'])
            if user != None:
                scope['user'] = user
        except Exception as ex:
            print("Erro: ",ex)
            

        return await self.app(scope,receive,send)
        
        
        