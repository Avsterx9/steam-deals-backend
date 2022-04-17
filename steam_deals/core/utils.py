import http
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi.responses import JSONResponse



def read_file_content(filepath: Path) -> str:
    with open(filepath, encoding='utf-8') as file:
        return file.read()


def create_status_response(status_code: int, description: str) -> dict:
    status_response = StatusResponse(status_code=status_code)
    return {'description': description, 'content': {'application/json': {'example': status_response.as_dict()}}}


def create_status_responses(response_with_description: Dict[int, str]) -> Dict[int, Any]:
    return {key: {**create_status_response(key, value)} for key, value in response_with_description.items()}


class StatusResponse(JSONResponse):
    def __init__(self, status_code: int = 200, detail: str = None, headers: Optional[Dict[str, Any]] = None):
        content = {
            'status_code': status_code,
            'phrase': http.HTTPStatus(status_code).phrase,
            'detail': detail,
        }

        super().__init__(content, status_code, headers)
        self.status_code = status_code
        self.phrase = http.HTTPStatus(status_code).phrase
        self.detail = detail

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, phrase={self.phrase!r}, detail={self.detail!r})"

    def as_dict(self):
        return {
            'status_code': self.status_code,
            'phrase': self.phrase,
            'detail': self.detail if self.detail else 'string',
        }
