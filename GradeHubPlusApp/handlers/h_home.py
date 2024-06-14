from GradeHubPlusApp.handlers.common.API import DtTools, Encryption
from GradeHubPlusApp.handlers.common.cache import Menippe
from GradeHubPlusApp.handlers.common.types import (
    AddSecretKeyOutputMsg, 
    AddStudentOutputMsg, 
    AddSubjectOutputMsg, 
    DataFrame, 
    DelSecretKeyOutputMsg, 
    FullName, 
    ModerElementsDB, 
    Nothing, 
    ScoreModes, 
    UserElementsDB, 
    WorkTypes, 
    AddSecretKeyStates, 
    AddStundentStates, 
    AddSubjectStates, 
    DelSecretKeyStates
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class AdminH(DatabaseH):
    """
    Класс обработчик для администратора.

    Наследуется от класса `DatabaseH`.
    """

    def __init__(self):
        super().__init__()
        self.menippe = Menippe()
        self.menippe.settings(cache_size=10)
    
    def display_selected_df(self, table: str) -> DataFrame:
        """
        Генерирует словарь для использования его в качестве датафрейма.
        
        Параметры:
        - table: str, принимает одну из таблиц БД.

        Возвращает:
        - сгенерированный `DataFrame`, если в БД есть данные;
        - пустой `DataFrame`, если в БД нет данных.
        """

        dataframe = self.__correct_dataframe(table)

        if table == 'users':
            elements = self.users_elems_from_db(table)

            if elements is not None:
                dataframe['Дата'] =     [i[0] for i in elements]
                dataframe['Логин'] =    [i[1] for i in elements]
                dataframe['Имя'] =      [i[2] for i in elements]
                dataframe['Фамилия'] =  [i[3] for i in elements]
                dataframe['Роль'] =     [i[4] for i in elements]
        elif table == 'scores':
            elements = self.scores_elems_from_db(table)

            if elements is not None:
                dataframe['Дата'] =             [i[0] for i in elements]
                dataframe['Студент'] =          [i[1] for i in elements]
                dataframe['Предмет'] =          [i[2] for i in elements]
                dataframe['Тип работы'] =       [i[3] for i in elements]
                dataframe['Баллы'] =            [i[4] for i in elements]
                dataframe['Преподаватель'] =    [i[5] for i in elements]
        elif table == 'subjects':
            elements = self.subjects_elems_from_db(table)

            if elements is not None:
                dataframe['Предмет'] = [i for i in elements]
        elif table == 'students':
            elements = self.students_elems_from_db(table)

            if elements is not None:
                dataframe['Дата'] =         [i[0] for i in elements]
                dataframe['Имя Фамилия'] =  [i[1] for i in elements]
                dataframe['Направление'] =  [i[2] for i in elements]
                dataframe['Курс'] =         [i[3] for i in elements]
        
        return dataframe
    
    def __correct_dataframe(self, table: str) -> dict[str, list]:
        if table == 'users':
            dataframe = {
                'Дата': [], 
                'Логин': [], 
                'Имя': [], 
                'Фамилия': [], 
                'Роль': []
            }
        elif table == 'scores':
            dataframe = {
                'Дата': [], 
                'Студент': [], 
                'Предмет': [], 
                'Тип работы': [], 
                'Баллы': [], 
                'Преподаватель': []
            }
        elif table == 'subjects':
            dataframe = {
                'Предмет': []
            }
        elif table == 'students':
            dataframe = {
                'Дата': [], 
                'Имя Фамилия': [], 
                'Направление': [], 
                'Курс': []
            }
        
        return dataframe

    def add_auth_key(self, key: str) -> AddSecretKeyOutputMsg:
        """
        Обрабатывает валидность ключа и добавляет его БД.

        Параметры:
        - key: str, принимает ключ для модераторов.

        Возвращает:
        - словарь типа `AddSecretKeyOutputMsg`.
        """

        data = self.db_keys.fetch().items
        hash_key = Encryption.hash_pw(key)
        _dt = DtTools.dt_now()
        date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'

        if data:
            for i in data:
                valid = Encryption.check_pw(i['key'], key)

                if valid:
                    output_msg = {
                        'state': AddSecretKeyStates.FAIL, 
                        'msg': 'Такой ключ уже есть в БД.'
                    }
                    break
                else:
                    self.db_keys.put({
                        'key': hash_key, 
                        'date': date, 
                        'owner': 'Undefined'
                    })
                    output_msg = {
                        'state': AddSecretKeyStates.SUCCESS, 
                        'msg': 'Ключ успешно добавлен в БД.'
                    }
                    continue
        else:
            self.db_keys.put({
                'key': hash_key, 
                'date': date, 
                'owner': 'Undefined'
            })
            output_msg = {
                'state': AddSecretKeyStates.SUCCESS, 
                'msg': 'Ключ успешно добавлен в БД.'
            }

        return output_msg

    def del_auth_key(self, key: str) -> DelSecretKeyOutputMsg:
        """
        Проверяет валидность ключа и удаляет его из БД.

        Параметры:
        - key: str, принимает ключ для модератора.

        Возвращает:
        - словарь типа `DelSecretKeyOutputMsg`.
        """

        data = self.db_keys.fetch().items

        if data:
            for i in data:
                valid = Encryption.check_pw(i['key'], key)

                if valid and i['owner'] == 'Undefined':
                    self.db_keys.delete(i['key'])
                    output_msg = {
                        'state': DelSecretKeyStates.SUCCESS, 
                        'msg': 'Ключ успешно удален из БД.'
                    }
                    break
                elif valid and i['owner'] != 'Undefined':
                    output_msg = {
                        'state': DelSecretKeyStates.FAIL, 
                        'msg': f'Этот ключ занят модератором {i['owner']}.'
                    }
                    break
                else:
                    output_msg = {
                        'state': DelSecretKeyStates.FAIL, 
                        'msg': 'Ключ не был распознан.'
                    }
                    continue
        else: output_msg = {
            'state': DelSecretKeyStates.FAIL, 
            'msg': 'Такого ключа нет в БД.'
        }
        
        return output_msg

    def display_keys_df(self) -> DataFrame:
        """
        Генерирует словарь для использования его в качестве датафрейма.

        Возвращает:
        - сгенерированный `DataFrame`, если в БД есть данные;
        - пустой `DataFrame`, если в БД нет данных.
        """

        dataframe = {
            'Ключ': [], 
            'Дата': [], 
            'Преподаватель': []
        }

        request = None
        _match, response = self.menippe.exists(request)

        if not _match:
            data = self.db_keys.fetch().items
            self.menippe.insert({'request': request, 'response': data})
        else: data = response

        # data = self.db_keys.fetch().items

        if data:
            elements = self.keys_elems_from_db(data)

            dataframe['Ключ'] =             [i[0] for i in elements]
            dataframe['Дата'] =             [i[1] for i in elements]
            dataframe['Преподаватель'] =    [i[2] for i in elements]

            return dataframe
        else: return dataframe


class ModeratorH(DatabaseH):
    """
    Класс обработчик для модератора.

    Наследуется от класса `DatabaseH`.
    """

    def __init__(self):
        super().__init__()
        self.menippe = Menippe()
        self.menippe.settings(cache_size=10)
 
    def add_student(self, 
        full_name: FullName, 
        direction: str, 
        course: int
    ) -> AddStudentOutputMsg:
        """
        Добавляет нового студента в БД.

        Параметры:
        - full_name: FullName, принимает имя и фамилию студента;
        - direction: str, принимает направление студента;
        - course: int, принимает курс студента.

        Возвращает:
        - словарь типа `AddStudentOutputMsg`.
        """
        
        data = self.db_students.fetch({
            'key': f'{full_name[0]} {full_name[1]}', 
            'direction': direction, 
            'course': course
        }).items

        if not data:
            _dt = DtTools.dt_now()
            date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'

            self.db_students.put({
                'key': f'{full_name[0]} {full_name[1]}', 
                'date': date, 
                'direction': direction, 
                'course': course
            })
            output_msg = {
                'state': AddStundentStates.SUCCESS, 
                'msg': 'Студент был успешно добавлен в БД.'
            }
        else: output_msg = {
            'state': AddStundentStates.FAIL, 
            'msg': 'Такой студент уже есть в БД.'
        }
        
        return output_msg
    
    def add_subject(self, subject: str) -> AddSubjectOutputMsg:
        """
        Добавляет новый предмет в БД.

        Параметры:
        - subject: str, принимает название предмета.

        Возвращает:
        - словарь типа `AddSubjectOutputMsg`.
        """

        data = self.db_subjects.fetch({'key': subject}).items

        if not data:
            self.db_subjects.put({'key': subject})
            output_msg = {
                'state': AddSubjectStates.SUCCESS, 
                'msg': 'Предмет был успешно добавлен в БД.'
            }
        else: output_msg = {
            'state': AddSubjectStates.FAIL, 
            'msg': 'Такой предмет уже есть в БД.'
        }

        return output_msg

    def edit_scores(self, 
        moder: str, 
        students: list, 
        subject: str, 
        mode: ScoreModes, 
        work_type: WorkTypes, 
        score: int
    ) -> Nothing:
        """
        Обрабатывает вводимые данные для изменения 
        баллов у студента(ов).

        Параметры:
        - moder: str, принимает логин модератора;
        - students: list, принимает список студентов (минимум один);
        - subject: str, принимает название предмета;
        - mode: ScoreModes, принимает добавление или вычитание баллов;
        - work_type: WorkTypes, принимает тип работы;
        - score: int, принимает кол-во баллов.

        Ничего не возвращает.
        """
        
        score = score if mode == 'Добавить' else -score
        data = self.db_scores.fetch({'moder': moder}).items

        if data:
            for student in students:
                updated = False

                for i in data:
                    if (
                        i['student'] == student and 
                        i['subject'] == subject and 
                        i['workType'] == work_type
                    ):
                        self.update_scores(
                            i['score'] + score, i['key']
                        )
                        updated = True
                        break

                if not updated:
                    self.put_scores(moder, student, subject, work_type, score)
        else:
            for student in students:
                self.put_scores(moder, student, subject, work_type, score)

    def display_df(self, 
        moder: str, 
        students: list, 
        directions: list, 
        courses: list, 
        subjects: list, 
        work_types: list
    ) -> DataFrame:
        """
        Генерирует словарь для использования его в качестве датафрейма, 
        используя фильтры.

        Параметры:
        - moder: str, принимает логин модератора;
        - students: list, принимает список выбранных студентов;
        - directions: list, принимает список выбранных направлений;
        - courses: list, принимает список выбранных курсов;
        - subjects: list, принимает список выбранных предметов;
        - work_types: list, принимает список выбранных типов работ.

        Возвращает:
        - сгенерированный `DataFrame`, если в БД есть данные, 
        с учетом фильтров;
        - пустой `DataFrame`, если в БД нет данных.
        """

        # проверка на пустые фильтры
        if not students: students = self.get_students()
        if not subjects: subjects = self.get_subjects()
        if not directions: directions = self.get_directions()
        if not work_types: work_types = [
            'Лекция', 'Семинар', 'Лабораторная', 'Практика'
        ]
        if not courses: courses = [1, 2, 3, 4, 5]

        dataframe = {
            'Студент': [], 
            'Направление': [], 
            'Курс': [], 
            'Предмет': [], 
            'Тип работы': [], 
            'Баллы': []
        }

        # Menippe - алгоритм кэширования
        request = [students, subjects, directions, work_types]
        _match, response = self.menippe.exists(request)

        if not _match:
            data = self.db_scores.fetch({'moder': moder}).items
            self.menippe.insert({'request': request, 'response': data})
        else: data = response


        if data:
            elements = self.__df_elements(
                data, students, directions, 
                courses, subjects, work_types
            )

            # заполнение отфильрованной таблицы
            dataframe['Студент'] =      [i[0] for i in elements]
            dataframe['Направление'] =  [i[1] for i in elements]
            dataframe['Курс'] =         [i[2] for i in elements]
            dataframe['Предмет'] =      [i[3] for i in elements]
            dataframe['Тип работы'] =   [i[4] for i in elements]
            dataframe['Баллы'] =        [i[5] for i in elements]
            
            return dataframe
        else: return dataframe

    def __df_elements(self, 
        data: list, 
        students: list, 
        directions: list, 
        courses: list, 
        subjects: list, 
        work_types: list
    ) -> ModerElementsDB:
        res = []

        # Создаем словарь студентов для быстрого доступа
        student_info = {}
        for student in students:
            parts = student.split(' - ')
            if len(parts) == 3:
                full_name, direction, course = parts
                student_info[student] = (full_name, direction, int(course))

        # Создаем множество допустимых комбинаций для быстрого поиска
        valid_combinations = set()
        for student in students:
            if student in student_info:
                full_name, direction, course = student_info[student]
                if direction in directions and course in courses:
                    for subject in subjects:
                        for wtype in work_types:
                            valid_combinations.add((subject, student, wtype))

        # Проверяем каждый элемент данных
        for i in data:
            student = i['student']
            subject = i['subject']
            wtype = i['workType']
            
            if (subject, student, wtype) in valid_combinations:
                full_name, direction, course = student_info[student]
                res.append((full_name, direction, course, subject, wtype, i['score']))

        return res


class UserH(DatabaseH):
    """
    Класс обработчик для пользователя.

    Наследуется от класса `DatabaseH`.
    """

    def __init__(self):
        super().__init__()
        self.menippe = Menippe()
        self.menippe.settings(cache_size=15)

    def display_df(self, 
        student: str, 
        moders: list, 
        subjects: list, 
        work_types: list
    ) -> DataFrame:
        """
        Генерирует словарь для использования его в качестве датафрейма, 
        используя фильтры.

        Параметры:
        - student: str, принимает имя и фамилию студента;
        - moders: list, принимает список из модераторов (имя и фамилия);
        - subjects: list, принимает список названий предметов;
        - work_types: list, принимает список типов работ.

        Возвращает:
        - сгенерированный DataFrame, если в БД есть данные, 
        с учетом фильтров;
        - пустой DataFrame, если в БД нет данных.
        """

        # Если список модераторов пуст, получаем всех модераторов
        if not moders:
            moders = self.get_moderators()
        else:
            moders_data = self.db_users.fetch({'role': 'Moderator'}).items
            moders_dict = {
                f'{mod['firstName']} {mod['lastName']}': mod['key'] 
                for mod in moders_data
            }
            moders = [
                (moders_dict[moder], moder.split()) 
                for moder in moders if moder in moders_dict
            ]

        # Если список предметов или типов работ пуст, заполняем их значениями по умолчанию
        if not subjects: subjects = self.get_subjects()
        if not work_types: work_types = [
            'Лекция', 'Семинар', 'Лабораторная', 'Практика'
        ]

        dataframe = {
            'Предмет': [], 
            'Тип работы': [], 
            'Баллы': [], 
            'Преподаватель': []
        }

        # Menippe - алгоритм кэширования
        request = student
        _match, response = self.menippe.exists(request)

        if not _match:
            students_data = self.db_students.get(student)
            self.menippe.insert({'request': request, 'response': students_data})
        else: students_data = response

        # students_data = self.db_students.get(student)

        if students_data is not None:
            student_key = (
                f'{students_data['key']} - ' +  #type: ignore
                f'{students_data['direction']} - ' +  #type: ignore
                f'{students_data['course']}' #type: ignore
            )

            # Menippe - алгоритм кэширования
            request = [moders, subjects, work_types]
            _match, response = self.menippe.exists(request)

            if not _match:
                data = self.db_scores.fetch({'student': student_key}).items
                self.menippe.insert({'request': request, 'response': data})
            else: data = response


            # data = self.db_scores.fetch({'student': student_key}).items

            if data:
                elements = self.__df_elements(data, moders, subjects, work_types)
                
                # Заполнение отфильтрованной таблицы
                dataframe['Предмет'] =          [i[0] for i in elements]
                dataframe['Тип работы'] =       [i[1] for i in elements]
                dataframe['Баллы'] =            [i[2] for i in elements]
                dataframe['Преподаватель'] =    [i[3] for i in elements]

                return dataframe
        return dataframe
    
    def __df_elements(self, 
        data: list, 
        moders: list, 
        subjects: list, 
        work_types: list
    ) -> UserElementsDB:
        res = []

        moders_dict = {moder[0]: f'{moder[1][0]} {moder[1][1]}' for moder in moders}

        for item in data:
            if (
                item['moder'] in moders_dict and 
                item['subject'] in subjects and 
                item['workType'] in work_types
            ):
                res.append((
                    item['subject'], item['workType'], item['score'], 
                    moders_dict[item['moder']]
                ))

        return res
