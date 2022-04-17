from datetime import timedelta
from pathlib import Path
from typing import Final

from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from jinja2 import Template
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from steam_deals.config import ROOT_DIRECTORY
from steam_deals.config import settings
from steam_deals.core import authentication
from steam_deals.core import schemas
from steam_deals.core import utils
from steam_deals.core.db import crud
from steam_deals.core.exception import CREDENTIALS_VALIDATION_EXCEPTION
from steam_deals.core.exception import HTTPException

EMAIL_TEMPLATE: Final[Path] = ROOT_DIRECTORY / 'core/templates/email_template.html'

config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=settings.MAIL_TLS,
    MAIL_SSL=settings.MAIL_SSL,
    USE_CREDENTIALS=settings.MAIL_USER_CREDENTIALS,
)

fast_mail = FastMail(config=config)


async def verify_user(db: Session, user: schemas.UserDetailed) -> None:
    if settings.REQUIRE_MAIL_CONFIRMATION:
        await send_verification_email(user=user)
        return

    user.verified = True
    crud.users.update_user(db=db, user=user)


async def send_verification_email(user: schemas.UserDetailed) -> None:
    if user.verified:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f'User with username `{user.username}` is already verified!'
        )

    expires_secs = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    expires_delta = timedelta(seconds=expires_secs)

    token = authentication.create_access_token(data={'sub': user.username, 'type': 'mail'}, expires_delta=expires_delta)

    template_content = utils.read_file_content(filepath=EMAIL_TEMPLATE)
    template = Template(template_content).render(
        first_name=user.first_name, last_name=user.last_name, host=settings.DNS, port=settings.PORT, token=token
    )

    message = MessageSchema(
        subject=f'steam-deals account verification for {user.username}',
        recipients=[user.email],
        body=template,
        subtype='html',
    )

    await fast_mail.send_message(message=message)


def verify_email_token(db: Session, token: str) -> schemas.UserDetailed:
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get('sub')
        type_: str = payload.get('type')

        if username is None or type_ != 'mail':
            raise CREDENTIALS_VALIDATION_EXCEPTION
    except JWTError as exception:
        raise CREDENTIALS_VALIDATION_EXCEPTION from exception

    user = crud.users.get_user_by_username(db=db, username=username)
    if user is None:
        raise CREDENTIALS_VALIDATION_EXCEPTION
    return user
