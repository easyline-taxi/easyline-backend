from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import connection
from channels.db import database_sync_to_async
from rest_framework_jwt.utils import jwt_decode_handler
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
    def __init__(self,inner):
        self.inner = inner
    
    async def __call__(self,scope, receive, send):
        
        headers = dict(scope['headers'])
        scope['host'] = headers[b'host'].decode("utf-8").split(':')[0]

        # print(">>> ",scope['query_string'].decode("utf-8").split('&')[0].split('=')[1])

        if 'query_string' in scope:
            token_name, token_key = scope['query_string'].decode("utf-8").split('&')[0].split('=')[1].split('%20')
            token_decoded = jwt_decode_handler(token_key)
            if token_name == 'Bearer':
                scope['user'] = await get_user(token_decoded.get('user_id'))
            if not scope.get('user'):
                scope['user'] = AnonymousUser
            return await self.inner(scope,receive, send)
        
        # if b'authorization' in headers:
        #     token_name, token_key = headers[b'authorization'].decode().split()
        #     if token_name == 'Token':
        #         scope['user'] = await get_user(token_key)
        #     if not scope['user']:
        #         raise Exception("User Inválido")
        #     return await self.inner(scope,receive, send)
        # raise Exception("Sem Autenticação")
        
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))