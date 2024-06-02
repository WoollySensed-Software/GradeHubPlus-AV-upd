import os
import hashlib

from datetime import datetime
from pytz import timezone
from enum import Enum


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

