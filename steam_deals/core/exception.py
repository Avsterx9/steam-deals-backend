import http
from typing import Any, Dict, Final, Optional

from starlette.status import HTTP_401_UNAUTHORIZED


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, detail, headers)
        self.status_code = status_code
        self.phrase = http.HTTPStatus(status_code).phrase
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


CREDENTIALS_VALIDATION_EXCEPTION: Final[HTTPException] = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)
