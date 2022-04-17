from typing import Dict
from typing import Optional

from fastapi import Request
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from steam_deals.core.exception import HTTPException

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(secret=plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={'tokenUrl': tokenUrl, 'scopes': scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get('access_token')

        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)

        authorization = True
        scheme = param = None

        if header_scheme.lower() == 'bearer':
            scheme, param = header_scheme, header_param
        elif cookie_scheme.lower() == 'bearer':
            scheme, param = cookie_scheme, cookie_param
        else:
            authorization = False

        if not authorization or scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            return None
        return param
