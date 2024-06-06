import streamlit as st

from pandas import DataFrame as df
from streamlit_option_menu import option_menu
from GradeHubPlusApp.handlers.h_common import (
    AddStundentStates, AddSubjectStates, 
    AddSecretKeyStates, DelSecretKeyStates
)
from GradeHubPlusApp.handlers.h_home import AdminH, ModeratorH, UserH
from GradeHubPlusApp.handlers.h_notify import EmailNotificationH


class HomeUI:

    def __init__(self, username: str, full_name: str, role: str):
        self.s_username = username
        self.s_full_name = full_name
        self.s_role = role
        self.h_admin = AdminH()
        self.h_moder = ModeratorH()
        self.h_user = UserH()
        self.h_email_notify = EmailNotificationH()

    def setupUI(self):
        st.markdown(f'### Добро пожаловать, :red[{self.s_full_name}]!')

        if self.s_role == 'Admin': self.__admin_ui()
        elif self.s_role == 'Moderator': self.__moder_ui()
        elif self.s_role == 'User': self.__user_ui()
    
    def __admin_ui(self):
        options = ('Таблицы', 'Уведомления', 'Ключи')
        selector_mode = option_menu(
            menu_title=None, 
            icons=['table', 'bell-fill', 'key-fill'], 
            orientation='horizontal', 
            options=options, 
            styles=None
        )

        # --- выбор таблицы ---
        if selector_mode == options[0]:
            table = st.radio(
                'Таблица', options=('users', 'scores', 'subjects', 'students'), 
                horizontal=True
            )

            df_data = self.h_admin.display_selected_df(table) # type: ignore
            dataframe = df(df_data)
            dataframe.index += 1
            st.dataframe(dataframe, use_container_width=True)

        # --- работа с уведомлениями ---
        elif selector_mode == options[1]:
            ...

        # --- работа с ключами ---
        elif selector_mode == options[2]:
            # --- таблица с ключами ---
            df_data = self.h_admin.display_keys_df()
            dataframe = df(df_data)
            dataframe.index += 1
            st.dataframe(dataframe, use_container_width=True)

            # --- работа с ключами ---
            self.__form_keys_handler()

    def __form_keys_handler(self):
        with st.form('Form_KeysHandler', clear_on_submit=True, border=True):
            st.markdown(':red[Работа с ключами]')
            st.markdown('Кол-во свободных ключей: ' + 
                f'{self.h_admin.get_free_keys_count()} шт.'
            )

            kh_mode = st.radio(
                'Режим работы', options=('Добавить', 'Удалить'), 
                horizontal=True, label_visibility='collapsed'
            )
            kh_key = st.text_input('Ключ', max_chars=16, type='password')

            if st.form_submit_button('Выполнить', type='primary'):
                if kh_mode == 'Добавить' and kh_key != '':
                    output_msg = self.h_admin.add_auth_key(kh_key)

                    if output_msg['state'] == AddSecretKeyStates.SUCCESS:
                        st.success(output_msg['msg'], icon='✔️')
                    elif output_msg['state'] == AddSecretKeyStates.FAIL:
                        st.warning(output_msg['msg'], icon='⚠️')
                elif kh_mode == 'Удалить' and kh_key != '':
                    output_msg = self.h_admin.del_auth_key(kh_key)

                    if output_msg['state'] == DelSecretKeyStates.SUCCESS:
                        st.success(output_msg['msg'], icon='✔️')
                    elif output_msg['state'] == DelSecretKeyStates.FAIL:
                        st.warning(output_msg['msg'], icon='⚠️')
                else: st.warning('Необходимо ввести ключ', icon='⚠️')

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
            self.__form_add_student()

        # --- добавление предметов ---
        with st.expander(':red[Добавление предмета]'):
            self.__form_add_subject()

        # --- работа с баллами ---
        with st.expander(':red[Работа с баллами]'):
            self.__form_edit_scores()

        # --- обнудение баллов ---
        with st.expander(':red[Обнуление баллов]'):
            self.__form_zeroing_scores()

    def __form_add_student(self):
        with st.form('From_AddStudent', clear_on_submit=True, border=False):
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

    def __form_add_subject(self):
        with st.form('Form_AddSubject', clear_on_submit=True, border=False):
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

    def __form_edit_scores(self):
        with st.form('Form_EditScores', clear_on_submit=True, border=False):
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
                    self.h_email_notify.send_score_notify(
                        self.s_username, self.s_full_name, es_subject,  # type: ignore
                        es_wtype, es_score, es_students # type: ignore
                    )
                    st.toast('Изменения внесены в БД', icon='🔥')
                else: st.warning('Укажите хотя бы одного студента', icon='⚠️')

    def __form_zeroing_scores(self):
        with st.form('Form_ZeroingScores', border=False):
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
        with st.sidebar:
            st.markdown('Фильтры сортировки таблицы:')
            selector_moders = st.multiselect(
                'Преподаватели', options=[
                    f'{i[1][0]} {i[1][1]}' for i in self.h_user.get_all_moderators()
                ], 
                placeholder='Можно несколько'
            )
            selector_subjects = st.multiselect(
                'Предметы', options=self.h_moder.get_all_subjects(), 
                placeholder='Можно несколько'
            )
            selector_wtypes = st.multiselect(
                'Типы работы', 
                options=('Лекция', 'Семинар', 'Лабораторная', 'Практика'), 
                placeholder='Можно несколько'
            )

        # --- отображение таблицы ---
        df_data = self.h_user.display_df(
            self.s_full_name, selector_moders, 
            selector_subjects, selector_wtypes
        )
        dataframe = df(df_data)
        dataframe.index += 1
        st.dataframe(dataframe, use_container_width=True)
