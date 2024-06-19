from deta import Deta

from GradeHubPlusApp.config.settings import KEY_DETA
from GradeHubPlusApp.handlers.common.API import DtTools
from GradeHubPlusApp.handlers.common.cache import Menippe
from GradeHubPlusApp.handlers.common.types import (
    AdminKeysElemsDB, 
    AdminScoresElemsDB, 
    AdminStudentsElemsDB, 
    AdminSubjectsElemsDB, 
    AdminUsersElemsDB, 
    Moderators, 
    Nothing, 
    WorkTypes
)


class DatabaseH:
    """
    Класс для работы с базой данных.
    """

    def __init__(self):
        self.db = Deta(KEY_DETA)
        self.db_keys = self.db.Base('keys')
        self.db_notify = self.db.Base('notify')
        self.db_users = self.db.Base('users')
        self.db_students = self.db.Base('students')
        self.db_subjects = self.db.Base('subjects')
        self.db_scores = self.db.Base('scores')
        
        self.menippe = Menippe()
    
    def users_elems_from_db(self, table: str) -> AdminUsersElemsDB | None:
        request = table
        _match, response = self.menippe.exists(request)

        if not _match:
            data = self.db_users.fetch().items
            self.menippe.insert({'request': request, 'response': data})
        else: data = response

        if data:
            res = []

            for i in data:
                res.append((
                    i['date'], i['key'], i['firstName'], 
                    i['lastName'], i['role']
                ))
            
            return res
        else: return None

    def scores_elems_from_db(self, table: str) -> AdminScoresElemsDB | None:
        request = table
        _match, response = self.menippe.exists(request)

        if not _match:
            data = self.db_scores.fetch().items
            self.menippe.insert({'request': request, 'response': data})
        else: data = response

        if data:
            res = []

            for i in data:
                res.append((
                    i['date'], i['student'], i['subject'], 
                    i['workType'], i['score'], i['moder']
                ))
            return res
        else: return

    def subjects_elems_from_db(self, table: str) -> AdminSubjectsElemsDB | None:
        request = table
        _match, response = self.menippe.exists(request)

        if not _match:
            data = self.db_subjects.fetch().items
            self.menippe.insert({'request': request, 'response': data})
        else: data = response
        
        return [i['key'] for i in data] if data else None

    def students_elems_from_db(self, table: str) -> AdminStudentsElemsDB | None:
        request = table
        _match, response = self.menippe.exists(request)

        if not _match:
            data = self.db_students.fetch().items
            self.menippe.insert({'request': request, 'response': data})
        else: data = response

        if data:
            return [(i['date'], i['key'], i['direction'], i['course']) for i in data]
        else: return None

    def keys_elems_from_db(self, data: list) -> AdminKeysElemsDB:
        return [('SECRET_KEY', i['date'], i['owner']) for i in data]

    def get_count_free_keys(self) -> int:
        """
        Возвращает кол-во незанятых ключей из БД.
        """

        return self.db_keys.fetch({'owner': 'Undefined'}).count

    def get_directions(self) -> list[str]:
        """
        Возвращает список всех направлений из БД.
        """

        data = self.db_students.fetch().items

        if data:
            return list(set(i['direction'] for i in data))
        else: return ['Список направлений пуст']

    def get_students(self) -> list[str]:
        """
        Возвращает список всех студентов из БД в формате: 
        Имя Фамилия - Направление - Курс.
        """

        data = self.db_students.fetch().items

        if data:
            return [f'{i['key']} - {i['direction']} - {i['course']}' for i in data]
        else: return []

    def get_subjects(self) -> list[str]:
        """
        Возвращает список всех предметов из БД.
        """

        data = self.db_subjects.fetch().items
        return [i['key'] for i in data] if data else []

    def get_moderators(self) -> Moderators:
        """
        Возвращает список, состоящий из кортежей, в которых 
        указано: логин модератора и список из 
        его имени и фамилии, из БД.
        """

        data = self.db_users.fetch({'role': 'Moderator'}).items

        if data:
            return [(i['key'], [i['firstName'], i['lastName']]) for i in data]
        else: return []

    def update_scores(self, score: int, key: str) -> Nothing:
        _dt = DtTools.dt_now()
        date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'
        self.db_scores.update({
            'date': date, 
            'score': score
        }, key)

    def put_scores(self, 
        moder: str, 
        student: str, 
        subject: str, 
        work_type: WorkTypes, 
        score: int
    ) -> Nothing:
        _dt = DtTools.dt_now()
        date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'
        self.db_scores.put({
            'date': date, 
            'moder': moder, 
            'student': student, 
            'subject': subject, 
            'workType': work_type, 
            'score': score
        })

    def zeroing_scores(self, moder: str, subject: str) -> Nothing:
        """
        Обнуляет все баллы у всех студентов, закрепленных за 
        модератором, по конкретному предмету.

        Параметры:
        - moder: str, принимает логин модератора;
        - subject: str, принимает название предмета.

        Ничего не возвращает.
        """

        data = self.db_scores.fetch({'moder': moder}).items

        if data:
            for i in data:
                if i['subject'] == subject:
                    self.update_scores(0, i['key'])

    def get_reg_date(self, username: str) -> str:
        """
        Получает дату и время создания аккаунта пользователя.

        Параметры:
        - username: str, принимает логин пользователя.

        Возвращает:
        - строку формата: `DD-MM-YYYY|H:M:S`.
        """

        return self.db_users.fetch({'key': username}).items[0]['date']
