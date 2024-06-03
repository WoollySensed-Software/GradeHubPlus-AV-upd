import os
import hashlib

from streamlit import session_state
from typing import Any
from datetime import datetime
from pytz import timezone
from enum import Enum


type FullName = list[str]
type SignUpOutputMsg = dict[str, SignUpStates | str]
type SignInOutputMsg = dict[str, SignInStates | Any]


def logout():
    session_state['Auth-Status'] = False
    session_state['Fullname'] = None
    session_state['Username'] = None
    session_state['Role'] = None
    session_state['Selector-Menu'] = ('Авторизация', 'Информация')


class SignUpStates(Enum):
    SUCCESS = 1
    FAIL = 2


class SignInStates(Enum):
    SUCCESS = 1
    FAIL = 2


class ValidationStates(Enum):
    VALID = 1
    INVALID = 2
    NULL = 3


class Encryption:

    @staticmethod
    def hash_pw(_password: str) -> str:
        salt = os.urandom(32).hex()
        return hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest() + ':' + salt

    @staticmethod
    def check_pw(_hash: str, _password: str) -> bool:
        password, salt = _hash.split(':')
        return password == hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest()


class DtTools:

    @staticmethod
    def dt_now() -> datetime:
        return datetime.now(timezone('Europe/Moscow'))

