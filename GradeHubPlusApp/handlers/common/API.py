import os
import hashlib

from pytz import timezone
from datetime import datetime

from streamlit import session_state


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
