import streamlit as st

from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu

from GradeHubPlusApp.handlers.common.types import (
    FormUI, 
    OptionUI, 
    PageUI, 
    SignInStates, 
    SignUpStates
)
from GradeHubPlusApp.handlers.h_authorization import AuthorizationH


class AuthorizationAUI:
    
    def __init__(self):
        self.h_auth = AuthorizationH()
    
    def setupUI(self) -> OptionUI:
        options = ('Регистрация', 'Вход')
        selector_mode = option_menu(
            menu_title=None, 
            icons=['person-plus-fill', 'box-arrow-in-right'], 
            default_index=1, 
            orientation='horizontal', 
            options=options
        )

        self.__sign_up() if selector_mode == options[0] else self.__sign_in()

    def __sign_up(self) -> PageUI:
        with st.form('Form_SignUp', border=False):
            st.markdown(':red[Регистрация]')
            col_su_fname, col_su_lname = st.columns(2)
            su_first_name = col_su_fname.text_input(
                'Имя', max_chars=64, placeholder='Введите Ваше имя'
            ).strip().capitalize()
            su_last_name = col_su_lname.text_input(
                'Фамилия', max_chars=64, placeholder='Введите Вашу фамилию'
            ).strip().capitalize()
            add_vertical_space(2)
            su_username = st.text_input(
                'Логин', max_chars=32, placeholder='Необходим для входа'
            ).strip()
            su_password = st.text_input(
                'Пароль', max_chars=32, type='password', 
                placeholder='Не используйте простой пароль'
            ).strip()

            with st.expander(':red[Для преподавателей]'):
                su_moder = st.toggle('Вы являетесь преподавателем?')
                su_key = st.text_input(
                    'Ключ активации', max_chars=16, type='password', 
                    placeholder='Укажите ключ для авторизации', 
                    help='Если Вы студент, то просто пропустите это поле'
                ).upper()
            
            if st.form_submit_button('Зарегистрироваться', type='primary'):
                if su_moder and su_key != '':
                    res = self.h_auth.create_account(
                        [su_first_name, su_last_name], su_username, 
                        su_password, su_moder, moder_key=su_key
                    )

                    if res['state'] == SignUpStates.SUCCESS:
                        st.success(res['msg'], icon='✔️')
                    elif res['state'] == SignUpStates.FAIL:
                        st.warning(res['msg'], icon='⚠️')
                elif su_moder and su_key == '':
                    st.warning(
                        'Чтобы убедиться, что Вы преподаватель, ' + 
                        'введите ключ авторизации.', icon='⚠️'
                    )
                elif (
                    su_first_name != '' and su_last_name != '' and 
                    su_username != '' and su_password != ''
                ):
                    res = self.h_auth.create_account(
                        [su_first_name, su_last_name], su_username, 
                        su_password, su_moder
                    )

                    if res['state'] == SignUpStates.SUCCESS:
                        st.success(res['msg'], icon='✔️')
                    elif res['state'] == SignUpStates.FAIL:
                        st.warning(res['msg'], icon='⚠️')
                else: st.warning(
                    'Необходимо заполнить все поля! (исключение: ' + 
                    'раздел для преподавателей).'
                )

    def __sign_in(self) -> PageUI:
        with st.form('Form_SignIn', border=False):
            st.markdown(':red[Вход в аккаунт]')
            si_username = st.text_input(
                'Логин', max_chars=32, placeholder='Введите логин'
            ).strip()
            si_password = st.text_input(
                'Пароль', max_chars=32, type='password', 
                placeholder='Введите пароль'
            ).strip()

            if st.form_submit_button('Войти', type='primary'):
                if si_username != '' and si_password != '':
                    res = self.h_auth.login_account(si_username, si_password)

                    if res['state'] == SignInStates.SUCCESS:
                        # изменить состояние сессии
                        st.session_state['Auth-Status'] = True
                        st.session_state['Fullname'] = res['Fullname']
                        st.session_state['Username'] = res['Username']
                        st.session_state['Role'] = res['Role']
                        st.session_state['Selector-Menu'] = (
                            'Главная', 'Профиль', 'Информация'
                        )
                        st.session_state['Selector-Icons'] = (
                            'house', 'person-lines-fill', 'info-circle-fill'
                        )

                        st.success(res['msg'], icon='✔️')
                    elif res['state'] == SignInStates.FAIL:
                        st.warning(res['msg'], icon='⚠️')
                else: st.warning(
                    'Необходимо ввести как логин, так и пароль.', icon='⚠️'
                )

    # Возможность восстановить пароль
    def __form_forget_password(self) -> FormUI:
        with st.form('Form_ForgetPassword', clear_on_submit=True, border=False):
            fp_email = st.text_input(
                'Введите почту', max_chars=128, 
                placeholder='Вам придет новый пароль'
            )

            if st.form_submit_button('Восстановить', type='primary'):
                if fp_email != '':
                    st.write('Вот новый пароль')
                else: st.warning('Нужно указать свою почту', icon='⚠️')