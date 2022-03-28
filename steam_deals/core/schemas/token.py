from pydantic.main import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expires_in: int = 1800
