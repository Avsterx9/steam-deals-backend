from pydantic.main import BaseModel


class StatusResponse(BaseModel):
    status_code: int = 200
    phrase: str = 'OK'
    detail: str = 'Successful response'
