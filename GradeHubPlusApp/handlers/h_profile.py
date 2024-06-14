from GradeHubPlusApp.handlers.common.API import Encryption
from GradeHubPlusApp.handlers.common.types import (
    ChangePasswordOutputMsg, 
    ChangePasswordStates
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class ProfileH(DatabaseH):
    """
    Класс для обработки профиля пользователя.

    Наследуется от класса `DatabaseH`.
    """

    def __init__(self):
        super().__init__()

    def change_password(self, 
        username: str, 
        old_pw: str, 
        new_pw: str
    ) -> ChangePasswordOutputMsg:
        """
        Меняет старый пароль пользователя на новый.

        Параметры:
        - username: str, принимает логин паользователя;
        - old_pw: str, принимает старый пароль;
        - new_pw: str, принимает новый пароль.

        Возвращает:
        - словарь типа `ChangePasswordOutputMsg`.
        """

        hash_pw = self.db_users.fetch({'key': username}).items[0]['password']
        password = Encryption.hash_pw(new_pw)
        
        if Encryption.check_pw(hash_pw, old_pw):
            self.db_users.update({
                'password': password
            }, username)
            output_msg = {
                'state': ChangePasswordStates.SUCCESS, 
                'msg': 'Пароль успешно изменен.'
            }
        else:
            output_msg = {
                'state': ChangePasswordStates.FAIL, 
                'msg': 'Вы ввели неверный старый пароль.'
            }
        
        return output_msg
