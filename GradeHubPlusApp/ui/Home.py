import streamlit as st

from pandas import DataFrame as df
from GradeHubPlusApp.handlers.h_common import (
    AddStundentStates, AddSubjectStates
)
from GradeHubPlusApp.handlers.h_home import AdminH, ModeratorH, UserH


class HomeUI:

    def __init__(self, username: str, full_name: str, role: str):
        self.s_username = username
        self.s_full_name = full_name
        self.s_role = role

        self.h_admin = AdminH()
        self.h_moder = ModeratorH()
        self.h_user = UserH()

    def setupUI(self):
        st.markdown(f'### Добро пожаловать, :red[{self.s_full_name}]!')

        if self.s_role == 'Admin': self.__admin_ui()
        elif self.s_role == 'Moderator': self.__moder_ui()
        elif self.s_role == 'User': self.__user_ui()
    
    def __admin_ui(self):
        pass

    def __moder_ui(self):
        # --- фильры таблицы ---
        with st.sidebar:
            st.markdown('Фильтры сортировки таблицы:')
            selector_students = st.multiselect(
                'Студенты', options=self.h_moder.get_all_students(), 
                placeholder='Можно несколько'
            )
            selector_directions = st.multiselect(
                'Направления (скоро)', options=self.h_moder.get_all_directions(), 
                placeholder='Можно несколько'
            )
            selector_courses = st.multiselect(
                'Курсы (скоро)', options=(1, 2, 3, 4, 5), 
                placeholder='Можно несколько'
            )
            selector_subjects = st.multiselect(
                'Предметы', options=self.h_moder.get_all_subjects(), 
                placeholder='Можно несколько'
            )
            selector_wtypes = st.multiselect(
                'Типы работы', options=(
                    'Лекция', 'Семинар', 'Лабораторная', 'Практика'
                ), 
                placeholder='Можно несколько'
            )

        # --- отображение таблицы ---
        df_data = self.h_moder.display_df(
            self.s_username, selector_students, selector_directions, 
            selector_courses, selector_subjects, selector_wtypes
        )
        dataframe = df(df_data)
        dataframe.index += 1
        st.dataframe(dataframe, use_container_width=True)

        # --- добавление студентов ---
        with st.expander(':red[Добавление студентов]'):
            with st.form('From_AddStudent', clear_on_submit=True, border=True):
                col_as_fname, col_as_lname, col_as_course = st.columns(3)
                as_first_name = col_as_fname.text_input(
                    'Имя студента', max_chars=64, 
                    placeholder='Введите имя стундента'
                ).strip().capitalize()
                as_last_name = col_as_lname.text_input(
                    'Фамилия студента', max_chars=64, 
                    placeholder='Введите фамилию студента'
                ).strip().capitalize()
                as_course = int(col_as_course.number_input(
                    'Курс студента (1-5)', min_value=1, max_value=5
                ))

                col_as_dirs, col_as_flag = st.columns([0.7, 0.3])
                as_directions = col_as_dirs.selectbox(
                    'Направление студента (добавленные)', 
                    options=self.h_moder.get_all_directions()
                )
                as_flag = col_as_flag.toggle('Учитывать?')

                as_direction = st.text_input(
                    'Направление студента (добавить)', max_chars=256, 
                    placeholder='Введите направление студента или ' + 
                    'выберите доступные', 
                    help='Код направления указывать не обязательно'
                ).strip()

                if st.form_submit_button('Добавить студента', type='primary'):
                    if as_first_name != '' and as_last_name != '':
                        if not as_flag and as_direction != '':
                            output_msg = self.h_moder.add_student(
                                [as_first_name, as_last_name], 
                                as_direction, as_course
                            )

                            if output_msg['state'] == AddStundentStates.SUCCESS:
                                st.toast(output_msg['msg'], icon='✔️')
                            elif output_msg['state'] == AddStundentStates.FAIL:
                                st.warning(output_msg['msg'], icon='⚠️')
                        elif not as_flag and as_direction == '':st.warning(
                            'Если Вы самостоятельно указываете направление, ' + 
                            'то нужно его ввести в нижнее поле.', icon='⚠️'
                        )
                        else:
                            output_msg = self.h_moder.add_student(
                                [as_first_name, as_last_name], 
                                as_directions, as_course # type: ignore
                            )

                            if output_msg['state'] == AddStundentStates.SUCCESS:
                                st.toast(output_msg['msg'], icon='✔️')
                            elif output_msg['state'] == AddStundentStates.FAIL:
                                st.warning(output_msg['msg'], icon='⚠️')
                    else: st.warning(
                        'Необходимо заполнить все поля, чтобы добавить студента.', 
                        icon='⚠️'
                    )

        # --- добавление предметов ---
        with st.expander(':red[Добавление предмета]'):
            with st.form('Form_AddSubject', clear_on_submit=True, border=True):
                asu_subject = st.text_input(
                    'Предмет (без кода)', max_chars=256, 
                    placeholder='Введите название предмета'
                ).strip()

                if st.form_submit_button('Добавить предмет', type='primary'):
                    if asu_subject != '':
                        output_msg = self.h_moder.add_subject(asu_subject)

                        if output_msg['state'] == AddSubjectStates.SUCCESS:
                            st.toast(output_msg['msg'], icon='✔️')
                        elif output_msg['state'] == AddSubjectStates.FAIL:
                            st.warning(output_msg['msg'], icon='⚠️')
                    else: st.warning('Вы не указать название предмета!', icon='⚠️')

        # --- работа с баллами ---
        with st.expander(':red[Работа с баллами]'):
            with st.form('Form_EditScores', clear_on_submit=True, border=True):
                es_subject = st.selectbox(
                    'Выберите предмет', options=self.h_moder.get_all_subjects()
                )
                es_students = st.multiselect(
                    'Выберите студента(ов)', options=self.h_moder.get_all_students(), 
                    placeholder='Можно выбрать несколько'
                )
                col_es_mode, col_es_wtype, col_es_score = st.columns(3)
                es_mode = col_es_mode.selectbox(
                    'Выберите режим', options=('Добавить', 'Вычесть')
                )
                es_wtype = col_es_wtype.selectbox(
                    'Выберите тип работы', 
                    options=('Лекция', 'Семинар', 'Лабораторная', 'Практика')
                )
                es_score = int(col_es_score.number_input(
                    'Баллы (0-100)', min_value=0, max_value=100
                ))

                if st.form_submit_button('Выполнить', type='primary'):
                    if es_students != []:
                        self.h_moder.edit_scores(
                            self.s_username, es_students, es_subject,  # type: ignore
                            es_mode, es_wtype, es_score # type: ignore
                        )

                        # TODO: добавить отправку уведомлений...
                        st.toast('Изменения внесены в БД', icon='🔥')
                    else: st.warning('Укажите хотя бы одного студента', icon='⚠️')

        # --- обнудение баллов ---
        with st.expander(':red[Обнуление баллов]'):
            with st.form('Form_ZeroingScores', border=True):
                zs_subject = st.selectbox(
                    'Выберите предмет для обнуления', 
                    options=self.h_moder.get_all_subjects()
                )
                
                if st.form_submit_button('Обнулить', type='primary'):
                    if zs_subject is not None:
                        self.h_moder.zeroing_scores(self.s_username, zs_subject)
                        st.success('Баллы были успешно сброшены до 0', icon='✔️')

    def __user_ui(self):
        # --- фильры таблицы ---
        ...

        # --- отображение таблицы ---
        ...