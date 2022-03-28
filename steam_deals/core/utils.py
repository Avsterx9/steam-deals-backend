import http
from typing import Any, Dict, Optional

from fastapi.responses import JSONResponse
import git


def get_version() -> str:
    repo = git.Repo(search_parent_directories=True)
    # if there are any changes (staged, tracked or untracked) do not refer the SHA of last commit
    return (
        'UNCOMMITTED'
        if repo.index.diff(None) or repo.index.diff('HEAD') or repo.untracked_files
        else repo.head.object.hexsha
    )


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
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
