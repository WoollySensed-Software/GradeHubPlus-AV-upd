import os
import hashlib

from streamlit import session_state
from typing import Any, Literal
from datetime import datetime
from pytz import timezone
from enum import Enum


type SignUpOutputMsg = dict[str, SignUpStates | str]
type SignInOutputMsg = dict[str, SignInStates | Any]
type AddStudentOutputMsg = dict[str, AddStundentStates | str]
type AddSubjectOutputMsg = dict[str, AddSubjectStates | str]
type AddSecretKeyOutputMsg = dict[str, AddSecretKeyStates | str]
type DelSecretKeyOutputMsg = dict[str, DelSecretKeyStates | str]
type AddEmailOutputMsg = dict[str, AddEmailStates | str]
type ChangeEmailOutputMsg = dict[str, ChangeEmailStates | str]
type ChangePasswordOutputMsg = dict[str, ChangePasswordStates | str]
type FullName = list[str]
type ScoreModes = Literal['Добавить', 'Вычесть']
type WorkTypes = Literal['Лекция', 'Семинар', 'Лабораторная', 'Практика']
type DataFrame = dict[str, list[Any]]


def logout():
    """
    Возвращает состояние сессии в первоначальное состояние.
    """

    session_state['Auth-Status'] = False
    session_state['Fullname'] = None
    session_state['Username'] = None
    session_state['Role'] = None
    session_state['Selector-Menu'] = ('Авторизация', 'Информация')
    session_state['Selector-Icons'] = ('person-fill-lock', 'info-circle-fill')


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
class AddStundentStates(Enum):
    SUCCESS = 1
    FAIL = 2
class AddSubjectStates(Enum):
    SUCCESS = 1
    FAIL = 2
class AddSecretKeyStates(Enum):
    SUCCESS = 1
    FAIL = 2
class DelSecretKeyStates(Enum):
    SUCCESS = 1
    FAIL = 2
class AddEmailStates(Enum):
    SUCCESS = 1
    FAIL = 2
class ChangeEmailStates(Enum):
    SUCCESS = 1
    FAIL = 2
class ChangePasswordStates(Enum):
    SUCCESS = 1
    FAIL = 2


class Encryption:
    """
    Класс для шифрования и проверки паролей и ключей.
    """

    @staticmethod
    def hash_pw(_password: str) -> str:
        """
        Хэширует строку переданную в качестве аргумента.

        Параметры:
        - _password: str, принимает строку.

        Возвращает:
        - строку с последовательностью символов + соль.
        """
        
        salt = os.urandom(32).hex()
        return hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest() + ':' + salt

    @staticmethod
    def check_pw(_hash: str, _password: str) -> bool:
        """
        Сравнивает хэш со строкой переданной в качестве аргумента.

        Параметры:
        - _hash: str, принимает хэш-строку;
        - _password: str, принимает строку.
        
        Возвращает:
        - True, если переданный аргумент совпадает;
        - False, если переданный аргумент не совпадает.
        """

        password, salt = _hash.split(':')
        return password == hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest()


class DtTools:
    """
    Класс для работы с датой и временем.
    """

    @staticmethod
    def dt_now() -> datetime:
        """
        Возвращает:
        - объект `datetime` в формате: `YYYY-MM-DD H:M:S:ms+UTF`.
        """

        return datetime.now(timezone('Europe/Moscow'))
