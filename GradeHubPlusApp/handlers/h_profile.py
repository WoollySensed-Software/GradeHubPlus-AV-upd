from GradeHubPlusApp.handlers.h_common import (
    ChangeEmailOutputMsg, ChangeEmailStates, Encryption
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class ProfileH(DatabaseH):

    def __init__(self):
        super().__init__()

    def get_reg_date(self, username: str):
        return self.db_users.fetch({'key': username}).items[0]['date'] # type: ignore

    def change_password(self, 
        username: str, 
        old_pw: str, 
        new_pw: str
    ) -> ChangeEmailOutputMsg:
        hash_pw = self.db_users.fetch({'key': username}).items[0]['password']
        password = Encryption.hash_pw(new_pw)
        if Encryption.check_pw(hash_pw, old_pw):
            self.db_users.update({
                'password': password
            }, username)
            output_msg = {
                'state': ChangeEmailStates.SUCCESS, 
                'msg': 'Пароль успешно изменен.'
            }
        else:
            output_msg = {
                'state': ChangeEmailStates.FAIL, 
                'msg': 'Вы ввели неверный старый пароль.'
            }
        
        return output_msg
