

from django.db import close_old_connections
# from django.conf import settings
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
# rest framework
from rest_framework_jwt.utils import jwt_decode_handler
from channels.db import database_sync_to_async
from api.models import User

@database_sync_to_async
def get_user(user_id):
    try:
        user = User.objects.get(pk=user_id)
        if user and user.is_active:
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

        # Get the token
        try:

            if 'query_string' in scope:
                token_name, token_key = scope['query_string'].decode("utf-8").split('&')[0].split('=')[1].split('%20')
                token_decoded = jwt_decode_handler(token_key)

                if token_name == 'Token':
                    scope['user'] = await get_user(token_decoded.get('user_id'))
                if not scope.get('user'):
                    scope['user'] = AnonymousUser
        except Exception as ex:
            print("Erro: ",ex)
            

        return await self.app(scope,receive,send)
        
        
        