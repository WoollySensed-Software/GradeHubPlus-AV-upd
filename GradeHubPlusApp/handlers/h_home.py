from GradeHubPlusApp.handlers.h_common import (
    AddStudentOutputMsg, AddSubjectOutputMsg, 
    ScoreModes, WorkTypes, DataFrame, FullName, 
    AddStundentStates, AddSubjectStates, DtTools
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class AdminH: pass


class ModeratorH(DatabaseH):

    def __init__(self):
        super().__init__()

    def get_all_directions(self) -> list[str]:
        data = self.db_students.fetch()

        if data.items != []:
            return list(set([i['direction'] for i in data.items]))
        else: return ['Список направлений пуст']
    
    def get_all_students(self) -> list[str]:
        data = self.db_students.fetch()

        if data.items != []:
            return [
                f'{i['key']} - {i['direction']} - {i['course']}' 
                for i in data.items
            ]
        else: return []
    
    def get_all_subjects(self) -> list[str]:
        data = self.db_subjects.fetch()

        return [i['key'] for i in data.items] if data.items != [] else []

    def get_all_moderators(self) -> list[tuple[str, list[str]]]:
        data = self.db_users.fetch()

        if data.items != []:
            return [
                (i['key'], [i['firstName'], i['lastName']]) 
                for i in data.items if i['role'] == 'Moderator'
            ]
        else: return []
    
    def add_student(self, 
        full_name: FullName, 
        direction: str, 
        course: int
    ) -> AddStudentOutputMsg:
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
        # проверка на пустые фильтры
        if students == []: students = self.get_all_students()
        if subjects == []: subjects = self.get_all_subjects()
        # if directions == []: directions = self.get_all_directions()
        if work_types == []: work_types = [
            'Лекция', 'Семинар', 'Лабораторная', 'Практика'
        ]
        # if courses == []: courses = [*range(1, 6)]

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
                data.items, students, subjects, work_types
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
    
    # FIXME: не работает фильтрация по направлению и курсу
    def __df_elements(self, 
        data: list, 
        students: list, 
        # directions: list, 
        # courses: list, 
        subjects: list, 
        work_types: list
    ) -> list:
        res = []

        while data != []:
            i = data.pop()

            for subject in subjects:
                for student in students:
                    for wtype in work_types:
                        if (
                            i['subject'] == subject and 
                            i['student'] == student and 
                            i['workType'] == wtype
                        ):
                            full_name, _dir, _course = student.split(' - ')
                            res += [(
                                full_name, _dir, _course, 
                                subject, wtype, i['score']
                            )]
                            break
        
        return res


class UserH: pass
