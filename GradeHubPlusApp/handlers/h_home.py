from GradeHubPlusApp.handlers.h_common import (
    AddStudentOutputMsg, AddSubjectOutputMsg, 
    AddSecretKeyOutputMsg, DelSecretKeyOutputMsg, 
    ScoreModes, WorkTypes, DataFrame, FullName, 
    AddStundentStates, AddSubjectStates, AddSecretKeyStates, 
    DelSecretKeyStates, DtTools, Encryption
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class AdminH(DatabaseH):
    """
    Класс обработчик для администратора.

    Наследуется от класса `DatabaseH`.
    """

    def __init__(self):
        super().__init__()
    
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
            elements = self.__users_elements_from_db()

            if elements is not None:
                dataframe['Дата'] =     [i[0] for i in elements]
                dataframe['Логин'] =    [i[1] for i in elements]
                dataframe['Имя'] =      [i[2] for i in elements]
                dataframe['Фамилия'] =  [i[3] for i in elements]
                dataframe['Роль'] =     [i[4] for i in elements]
        elif table == 'scores':
            elements = self.__scores_elements_from_db()

            if elements is not None:
                dataframe['Дата'] =             [i[0] for i in elements]
                dataframe['Студент'] =          [i[1] for i in elements]
                dataframe['Предмет'] =          [i[2] for i in elements]
                dataframe['Тип работы'] =       [i[3] for i in elements]
                dataframe['Баллы'] =            [i[4] for i in elements]
                dataframe['Преподаватель'] =    [i[5] for i in elements]
        elif table == 'subjects':
            elements = self.__subjects_elements_from_db()

            if elements is not None:
                dataframe['Предмет'] = [i for i in elements]
        elif table == 'students':
            elements = self.__students_elements_from_db()

            if elements is not None:
                dataframe['Дата'] =         [i[0] for i in elements]
                dataframe['Имя Фамилия'] =  [i[1] for i in elements]
                dataframe['Направление'] =  [i[2] for i in elements]
                dataframe['Курс'] =         [i[3] for i in elements]
        
        return dataframe
    
    def __correct_dataframe(self, table: str) -> DataFrame:
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

    def __users_elements_from_db(self) -> list | None:
        data = self.db_users.fetch().items

        if data != []:
            res = []

            for i in data:
                res += [(
                    i['date'], i['key'], i['firstName'], 
                    i['lastName'], i['role']
                )]
            return res
                
        else: return

    def __scores_elements_from_db(self) -> list | None:
        data = self.db_scores.fetch().items

        if data != []:
            res = []

            for i in data:
                res += [(
                    i['date'], i['student'], i['subject'], 
                    i['workType'], i['score'], i['moder']
                )]
            return res
        else: return

    def __subjects_elements_from_db(self) -> list | None:
        data = self.db_subjects.fetch().items
        return [i['key'] for i in data] if data != [] else None

    def __students_elements_from_db(self) -> list | None:
        data = self.db_students.fetch().items

        if data != []:
            return [(i['date'], i['key'], i['direction'], i['course']) for i in data]
        else: return

    def get_free_keys_count(self) -> int:
        """
        Возвращает кол-во незанятых ключей из БД.
        """

        return self.db_keys.fetch({'owner': 'Undefined'}).count

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

        if data != []:
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

        if data != []:
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

        data = self.db_keys.fetch().items

        if data != []:
            elements = self.__keys_elements_from_db(data)

            dataframe['Ключ'] =             [i[0] for i in elements]
            dataframe['Дата'] =             [i[1] for i in elements]
            dataframe['Преподаватель'] =    [i[2] for i in elements]

            return dataframe
        else: return dataframe

    def __keys_elements_from_db(self, data: list) -> list:
        return [('SECRET_KEY', i['date'], i['owner']) for i in data]


class ModeratorH(DatabaseH):
    """
    Класс обработчик для модератора.

    Наследуется от класса `DatabaseH`.
    """

    def __init__(self):
        super().__init__()

    def get_all_directions(self) -> list[str]:
        """
        Возвращает список всех направлений из БД.
        """

        data = self.db_students.fetch()

        if data.items != []:
            return list(set([i['direction'] for i in data.items]))
        else: return ['Список направлений пуст']
    
    def get_all_students(self) -> list[str]:
        """
        Возвращает список всех студентов из БД в формате: 
        Имя Фамилия - Направление - Курс.
        """

        data = self.db_students.fetch()

        if data.items != []:
            return [
                f'{i['key']} - {i['direction']} - {i['course']}' 
                for i in data.items
            ]
        else: return []
    
    def get_all_subjects(self) -> list[str]:
        """
        Возвращает список всех предметов из БД.
        """

        data = self.db_subjects.fetch()

        return [i['key'] for i in data.items] if data.items != [] else []
    
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
        })

        if data.items == []:
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

        data = self.db_subjects.fetch({'key': subject})

        if data.items == []:
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
    ) -> None:
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
        data = self.db_scores.fetch({'moder': moder})

        if data.items != []:
            for student in students:
                updated = False

                for i in data.items:
                    if (
                        i['student'] == student and 
                        i['subject'] == subject and 
                        i['workType'] == work_type
                    ):
                        self.__update_scores(
                            i['score'] + score, i['key']
                        )
                        updated = True
                        break

                if not updated:
                    self.__put_scores(moder, student, subject, work_type, score)
        else:
            for student in students:
                self.__put_scores(moder, student, subject, work_type, score)
    
    def __update_scores(self, 
        score: int, 
        key: str
    ) -> None:
        _dt = DtTools.dt_now()
        date = f'{_dt:%d-%m-%Y}|{_dt:%H:%M:%S}'
        self.db_scores.update({
            'date': date, 
            'score': score
        }, key)
    
    def __put_scores(self, 
        moder: str, 
        student: str, 
        subject: str, 
        work_type: WorkTypes, 
        score: int
    ) -> None:
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

    def zeroing_scores(self, moder: str, subject: str) -> None:
        """
        Обнуляет все баллы у всех студентов, закрепленных за 
        модератором, по конкретному предмету.

        Параметры:
        - moder: str, принимает логин модератора;
        - subject: str, принимает название предмета.

        Ничего не возвращает.
        """

        data = self.db_scores.fetch({'moder': moder})

        if data.items != []:
            for i in data.items:
                if i['subject'] == subject:
                    self.__update_scores(0, i['key'])

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
        if not students: students = self.get_all_students()
        if not subjects: subjects = self.get_all_subjects()
        if not directions: directions = self.get_all_directions()
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
        data = self.db_scores.fetch({'moder': moder})

        if data.items != []:
            elements = self.__df_elements(
                data.items, students, directions, 
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
    ):
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

    def get_all_subjects(self) -> list[str]:
        """
        Возвращает список всех предметов из БД.
        """

        data = self.db_subjects.fetch()

        return [i['key'] for i in data.items] if data.items != [] else []
    
    def get_all_moderators(self) -> list[tuple[str, list[str]]]:
        """
        Возвращает список, состоящий из кортежей, в которых 
        указано: логин модератора и список из 
        его имени и фамилии, из БД.
        """
        
        data = self.db_users.fetch({'role': 'Moderator'}).items

        if data != []:
            return [(i['key'], [i['firstName'], i['lastName']]) for i in data]
        else: return []
    
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
        - сгенерированный `DataFrame`, если в БД есть данные, 
        с учетом фильтров;
        - пустой `DataFrame`, если в БД нет данных.
        """

        # FIXME: очень странная реализация фильтрации по модеру
        # нужно оптимизировать данный участок
        if moders == []:
            moders = self.get_all_moderators()
        else:
            moders_data = self.db_users.fetch({'role': 'Moderator'})
            moders_full_name = moders
            res = []
            for i in moders_data.items:
                for j in moders_full_name:
                    fname, lname = j.split(' ')
                    if i['firstName'] == fname and i['lastName'] == lname:
                        res += [(i['key'], [fname, lname])]
            moders = res
        if subjects == []: subjects = self.get_all_subjects()
        if work_types == []: work_types = [
            'Лекция', 'Семинар', 'Лабораторная', 'Практика'
        ]
        
        dataframe = {
            'Предмет': [], 
            'Тип работы': [], 
            'Баллы': [], 
            'Преподаватель': []
        }
        students_data = self.db_students.get(student)

        if students_data is not None:
            student = (
                f'{students_data['key']} - ' +  # type: ignore
                f'{students_data['direction']} - ' + # type: ignore
                f'{students_data['course']}' # type: ignore
            )
            data = self.db_scores.fetch({'student': student})

            if data.items != []:
                elements = self.__df_elements(
                    data.items, moders, subjects, work_types
                )
                # заполнение отфильтрованной таблицы
                dataframe['Предмет'] =          [i[0] for i in elements]
                dataframe['Тип работы'] =       [i[1] for i in elements]
                dataframe['Баллы'] =            [i[2] for i in elements]
                dataframe['Преподаватель'] =    [i[3] for i in elements]

                return dataframe
            else: return dataframe
        else: return dataframe

    def __df_elements(self, 
        data: list, 
        moders: list, 
        subjects: list, 
        work_types: list
    ) -> list:
        res = []

        while data != []:
            i = data.pop()

            for subject in subjects:
                for moder in moders:
                    for wtype in work_types:
                        if (
                            i['moder'] == moder[0] and 
                            i['subject'] == subject and 
                            i['workType'] == wtype
                        ):
                            res += [(
                                subject, wtype, i['score'], 
                                f'{moder[1][0]} {moder[1][1]}'
                            )]
                            break
        
        return res
