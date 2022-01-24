from typing import Annotated
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token):
    decoded_data = jwt_decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )
    user = get_user_model().objects.get(id=decoded_data["user_id"])
    return user


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        parsed_query_string = parse_qs(query_string)
        if len(parsed_query_string) == 0:
            scope['user'] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        token = parsed_query_string.get("token")[0]
        if token is None:
            scope['user'] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            scope['user'] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        scope['user'] = await get_user(token)

        return await super().__call__(scope, receive, send)
