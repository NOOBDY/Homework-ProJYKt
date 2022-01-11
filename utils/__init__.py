from typing import Dict, Tuple
from requests import Session

from .login import _login
from .get_question_statuses import _get_question_statuses
from .get_test_status import _get_test_status
from .get import _get
from .submit import _submit, _delete


class JykuoSession:
    def __init__(self, base_url: str):
        self.session = Session()
        self.base_url = base_url

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return Session.__exit__(
            self.session,
            exception_type,
            exception_value,
            traceback)

    def login(self, login_data: Dict[str, str]) -> None:
        return _login(self, login_data)

    def get(self, index: str) -> str:
        return _get(self, index)
    
    def get_question_statuses(self) -> Dict[str, Dict[str, str]]:
        return _get_question_statuses(self)

    def get_test_status(self, id_: int, index: str) -> Dict[str, Tuple[bool, str]]:
       return _get_test_status(self, id_, index)

    def submit(self, index: str, filepath: str) -> None:
        return _submit(self, index, filepath)

    def delete(self, index: str) -> None:
        return _delete(self, index)
