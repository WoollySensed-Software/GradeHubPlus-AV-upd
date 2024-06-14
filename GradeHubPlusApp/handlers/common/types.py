from enum import Enum
from typing import Any, Literal


type AddEmailOutputMsg = dict[str, AddEmailStates | str]
type AddSecretKeyOutputMsg = dict[str, AddSecretKeyStates | str]
type AddStudentOutputMsg = dict[str, AddStundentStates | str]
type AddSubjectOutputMsg = dict[str, AddSubjectStates | str]
type AdminKeysElemsDB = list[tuple[str, str, str]]
type AdminScoresElemsDB = list[tuple[str, str, str, str, int, str]]
type AdminStudentsElemsDB = list[tuple[str, str, str, int]]
type AdminSubjectsElemsDB = list[str]
type AdminUsersElemsDB = list[tuple[str, str, str, str, str]]
type Cache = tuple[bool, list[dict[str, Any]]]
type ChangeEmailOutputMsg = dict[str, ChangeEmailStates | str]
type ChangePasswordOutputMsg = dict[str, ChangePasswordStates | str]
type DataFrame = dict[str, list[Any]]
type DelSecretKeyOutputMsg = dict[str, DelSecretKeyStates | str]
type FormUI = None
type FullName = list[str]
type Moderators = list[tuple[str, list[str]]]
type ModerElementsDB = list[tuple[str, str, int, str, str, int]]
type Nothing = None
type OptionUI = None
type PageUI = None
type ScoreModes = Literal['Добавить', 'Вычесть']
type SignInOutputMsg = dict[str, SignInStates | Any]
type SignUpOutputMsg = dict[str, SignUpStates | str]
type UserElementsDB = list[tuple[str, str, int, str]]
type WorkTypes = Literal['Лекция', 'Семинар', 'Лабораторная', 'Практика']


class AddEmailStates(Enum):
    SUCCESS = 1
    FAIL = 2
class AddSecretKeyStates(Enum):
    SUCCESS = 1
    FAIL = 2
class AddStundentStates(Enum):
    SUCCESS = 1
    FAIL = 2
class AddSubjectStates(Enum):
    SUCCESS = 1
    FAIL = 2
class ChangeEmailStates(Enum):
    SUCCESS = 1
    FAIL = 2
class ChangePasswordStates(Enum):
    SUCCESS = 1
    FAIL = 2
class DelSecretKeyStates(Enum):
    SUCCESS = 1
    FAIL = 2
class SignInStates(Enum):
    SUCCESS = 1
    FAIL = 2
class SignUpStates(Enum):
    SUCCESS = 1
    FAIL = 2
class ValidationStates(Enum):
    VALID = 1
    INVALID = 2
    NULL = 3
