from GradeHubPlusApp.handlers.common.API import DtTools, Encryption
from GradeHubPlusApp.handlers.common.types import (
    FullName, 
    SignInOutputMsg, 
    SignUpOutputMsg, 
    SignInStates, 
    SignUpStates, 
    ValidationStates
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class AuthorizationH(DatabaseH):
    """
    Класс для авторизации пользователей.
    
    Наследуется от класса `DatabaseH`.
    """
    
    def __init__(self):
        super().__init__()
    
    def create_account(self, 
        full_name: FullName, 
        username: str, 
        password: str, 
        moderator: bool, 
        *, 
        moder_key: str = ''
    ) -> SignUpOutputMsg:
        """
        Обрабатывает данные пользователя при создании аккаунта.
        
        Параметры:
        - full_name: FullName, принимает имя и фамилию пользователя;
        - username: str, принимает логин пользователя;
        - password: str, принимает пароль пользователя;
        - moderator: bool, принимает статус пользователя;
        - moder_key: str = '', принимает ключ авторизации для модератора.
        
        Возвращает:
        - словарь типа `SignUpOutputMsg`.
        """
        
        valid_account = self.__create_account_validation(username)
        if not valid_account:
            return {
                'state': SignUpStates.FAIL, 
                'msg': 'Такой логин уже используется другим пользователем'
            }

        if moderator:
            output_msg = self.__create_account_to_moder(
                full_name, username, password, moder_key
            )
        else:
            output_msg = self.__create_account_to_user(
                full_name, username, password
            )
        
        return output_msg
    
    def __create_account_validation(self, username: str) -> bool:
        data = self.db_users.fetch().items

        if data:
            return True if self.db_users.get(username) is None else False
        else: return True

    def __create_account_to_moder(self, 
        full_name: FullName, 
        username: str, 
        password: str, 
        key: str
    ) -> SignUpOutputMsg:
        hash_key, validation = self.__validation_moder_key(key)
        _dt = DtTools.dt_now()
        date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'
        password = Encryption.hash_pw(password)

        if validation == ValidationStates.VALID:
            self.db_users.put({
                'key': username, 
                'date': date, 
                'firstName': full_name[0], 
                'lastName': full_name[1], 
                'password': password, 
                'role': 'Moderator'
            })
            self.db_keys.update({'owner': username}, hash_key)
            self.db_notify.put({
                'key': username, 
                'fullName': f'{full_name[0]} {full_name[1]}', 
                'mode': 'Undefined', 
                'link': 'Undefined', 
                'isEnable': 'No'
            })
            
            return {
                'state': SignUpStates.SUCCESS, 
                'msg': 'Аккаунт был успешно создан.'
            }
        elif validation == ValidationStates.INVALID:
            return {
                'state': SignUpStates.FAIL, 
                'msg': 'Не удалось создать аккаунт! Ключ не был опознан.'
            }
        else:
            return {
                'state': SignUpStates.FAIL, 
                'msg': 'В базе данных нет ключей, чтобы провести проверку.'
            }

    def __validation_moder_key(self, key: str) -> tuple[str, ValidationStates]:
        keys = self.db_keys.fetch().items

        if keys:
            for i in keys:
                valid = Encryption.check_pw(i['key'], key)

                if valid and i['owner'] == 'Undefined':
                    validation = (i['key'], ValidationStates.VALID)
                    break
                else:
                    validation = ('', ValidationStates.INVALID)
                    continue
        else: validation = ('', ValidationStates.NULL)

        return validation

    def __create_account_to_user(self, 
        full_name: FullName, 
        username: str, 
        password: str
    ) -> SignUpOutputMsg:
        _dt = DtTools.dt_now()
        date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'
        password = Encryption.hash_pw(password)

        self.db_users.put({
            'key': username, 
            'date': date, 
            'firstName': full_name[0], 
            'lastName': full_name[1], 
            'password': password, 
            'role': 'User'
        })
        self.db_notify.put({
            'key': username, 
            'fullName': f'{full_name[0]} {full_name[1]}', 
            'mode': 'Undefined', 
            'link': 'Undefined', 
            'isEnable': 'No'
        })
        
        return {
            'state': SignUpStates.SUCCESS, 
            'msg': 'Аккаунт был успешно создан.'
        }

    def login_account(self, 
        username: str, 
        password: str
    ) -> SignInOutputMsg:
        """
        Обрабатывает данные пользователя при входе.

        Параметры:
        - username: str, принимает логин пользователя;
        - password: str, принимает пароль пользователя.

        Возвращает:
        - словарь типа `SignInOutputMsg`.
        """
        
        data = self.db_users.fetch().items

        if data:
            for i in data:
                valid = Encryption.check_pw(i['password'], password)

                if valid and i['key'] == username:
                    output_msg = {
                        'state': SignInStates.SUCCESS, 
                        'msg': 'Вы успешно вошли в аккаунт.', 
                        'Fullname': f'{i['firstName']} {i['lastName']}', 
                        'Username': i['key'], 
                        'Role': i['role']
                    }
                    break
                else:
                    output_msg = {
                        'state': SignInStates.FAIL, 
                        'msg': 'Неверный логин или пароль!' + 
                        'Перепроверьте вводимые данные.'
                    }
                    continue
        else: 
            output_msg = {
                'state': SignInStates.SUCCESS, 
                'msg': 'Вы успешно вошли в аккаунт.'
            }

        return output_msg
