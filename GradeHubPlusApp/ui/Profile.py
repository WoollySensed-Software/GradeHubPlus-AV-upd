import streamlit as st

from streamlit_option_menu import option_menu

from GradeHubPlusApp.handlers.common.cache import Menippe
from GradeHubPlusApp.handlers.common.types import (
    FormUI, 
    OptionUI, 
    PageUI, 
    AddEmailStates, 
    ChangeEmailStates, 
    ChangePasswordStates
)
from GradeHubPlusApp.handlers.h_notify import EmailNotificationH
from GradeHubPlusApp.handlers.h_profile import ProfileH


class ProfileUI:

    def __init__(self, username: str, full_name: str, role: str):
        self.s_username = username
        self.s_full_name = full_name
        self.s_role = role
        self.h_profile = ProfileH()
        self.h_email_notify = EmailNotificationH()
        self.menippe = Menippe()
    
    def setupUI(self) -> OptionUI:
        options = ('Аккаунт', 'Настройки')
        selector_mode = option_menu(
            menu_title=None, 
            icons=['person-lines-fill', 'gear-fill'], 
            orientation='horizontal', 
            options=options, 
            styles=None
        )

        if selector_mode == options[0]: self.__account_info()  # аккаунт
        elif selector_mode == options[1]: self.__settings()  # настройки

    def __account_info(self) -> PageUI:
        info = self.__get_needed_info()
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown('## :blue[Имя и Фамилия]:')
            st.markdown(f'### :red[{self.s_full_name}]')
            st.markdown('## :blue[Данные аккаунта]:')
            st.markdown(f'### Статус: :red[{info['role']}]')
            st.markdown(f'### Логин: :red[{self.s_username}]')
            st.markdown(f'### Дата регистрации: :red[{info['regDate']}]')

        with col_right:
            st.markdown('## :blue[Система оповещения]:')
            st.markdown(f'### Отправка уведомлений: {info['notifyStatus']}')
            st.markdown(f'### Способ доставки уведомлений: {info['notifyMode']}')
            if info['kword'] != 'Не указано':
                st.markdown(f'### {info['kword']}: :red[{info['link']}]')

    def __get_needed_info(self) -> dict[str, str]:
        # Получение данных из БД
        reg_date = self.h_profile.get_reg_date(self.s_username)
        notify_status = self.h_email_notify.get_notify_status(self.s_username)
        notify_mode = self.h_email_notify.get_notify_mode(self.s_username)
        link = self.h_email_notify.get_link(self.s_username)

        # Корректировка для правильного отображения в st.markdown
        if self.s_role == 'Admin': role = 'Администратор'
        elif self.s_role == 'Moderator': role = 'Преподаватель'
        else: role = 'Пользователь'
        
        if notify_status == 'Yes': notify_status = ':red[Включена]'
        else: notify_status = ':orange[Выключена]'

        if notify_mode == 'Email':
            kword = 'Почта'
            notify_mode = f':red[{kword}]'
        elif notify_mode == 'Telegram':
            kword = 'Телеграм'
            notify_mode = f':red[{kword}]'
        else:
            kword = 'Не указано'
            notify_mode = f':orange[{kword}]'

        if link == 'Undefined': link = ''

        return {
            'role': role, 
            'regDate': reg_date, 
            'notifyStatus': notify_status, 
            'notifyMode': notify_mode, 
            'link': link, 
            'kword': kword
        }

    def __settings(self) -> PageUI:
        # --- управление уведомлениями ---
        with st.expander(':red[Управление уведомлениями]'):
            notify_mode = self.h_email_notify.get_notify_mode(self.s_username)

            # --- добавление ---
            if notify_mode == 'Undefined':
                self.__form_add_notify_mode()
            else:
                # --- уведомления ---
                notify = self.h_email_notify.get_notify_status(self.s_username)

                if notify == 'Yes':
                    switch_status = st.toggle(
                        'отправлять оповещения?', value=True
                    )

                    if not switch_status:
                        self.h_email_notify.change_notify_status(self.s_username)
                else:
                    switch_status = st.toggle(
                        'отправлять оповещения?', value=False
                    )

                    if switch_status:
                        self.h_email_notify.change_notify_status(self.s_username)

                # --- изменение ---
                if notify_mode == 'Email': self.__form_change_email_link()  # почта
                # elif notify_mode == 'Telegram': self.__form_change_tg_link()  # тг
        
        # --- изменение пароля ---
        with st.expander(':red[Изменение пароля]'):
            self.__form_change_password()
        
        # --- кэширование ---
        with st.expander(':red[Кэширование]'):
            col_vault_size, _ = st.columns([0.3, 0.7])
            st.session_state['Cache-settings-vault_size'] = int(col_vault_size.selectbox(
                'Какое максимальное кол-во кэша хранить?', options=[*range(1, 16)], 
                index=[*range(1, 16)].index(st.session_state['Cache-settings-vault_size'])
            )) # type: ignore
            st.session_state['Cache-settings-optimization'] = st.toggle(
                'Оптимизировать кэширование?', value=st.session_state['Cache-settings-optimization']
            )

    def __form_add_notify_mode(self) -> FormUI:
        with st.form('Form_AddNotifyMode', clear_on_submit=True, border=False):
            anm_selected_mode = st.selectbox(
                'Выберите систему для отправки оповещений', 
                options=('Почта', 'Телеграм')
            )
            anm_link = st.text_input(
                'Куда отправлять оповещения?', max_chars=128, 
                placeholder='Почта: example@gmail.com | Телеграм: @Username'
            ).strip()

            if st.form_submit_button('Добавить', type='primary'):
                if anm_selected_mode == 'Почта' and anm_link != '':
                    output_msg = self.h_email_notify.add_email(
                        self.s_username, anm_link
                    )

                    if output_msg['state'] == AddEmailStates.SUCCESS:
                        st.success(output_msg['msg'], icon='✔️')
                    elif output_msg['state'] == AddEmailStates.FAIL:
                        st.warning(output_msg['msg'], icon='⚠️')
                elif anm_selected_mode == 'Телеграм':
                    st.error(
                        'На данный момент отправка оповещений через ' + 
                        'Телеграм недоступна. Попробуйте выбрать ' + 
                        'другой метод для отправки оповещений.', icon='😟'
                    )
                else: st.warning(
                    'Чтобы отправлять оповещения, нужно знать ' + 
                    'куда их отправлять.', icon='⚠️'
                )

    def __form_change_email_link(self) -> FormUI:
        with st.form('Form_ChangeEmailLink', clear_on_submit=True, border=False):
            cel_old_link = st.text_input(
                'Введите старую почту', max_chars=128, 
                placeholder='Можно найти в разделе "Аккаунт"'
            ).strip()
            cel_new_link = st.text_input(
                'Введите новую почту', max_chars=128, 
                placeholder='Эта почта заменит предыдущую'
            ).strip()
            cel_confirm_link = st.text_input(
                'Введите новую почту еще раз', max_chars=128, 
                placeholder='Эта и новая почта должны совпадать'
            ).strip()

            if st.form_submit_button('Изменить', type='primary'):
                if cel_old_link != '' and cel_new_link != '':
                    if (
                        cel_new_link == cel_confirm_link and 
                        cel_new_link != cel_old_link
                    ):
                        output_msg = self.h_email_notify.change_email(
                            self.s_username, cel_old_link, cel_new_link
                        )

                        if output_msg['state'] == ChangeEmailStates.SUCCESS:
                            st.success(output_msg['msg'], icon='✔️')
                        elif output_msg['state'] == ChangeEmailStates.FAIL:
                            st.warning(output_msg['msg'], icon='⚠️')
                else: st.warning(
                    'Необходимо заполнить все поля.', icon='⚠️'
                )

    def __form_change_password(self) -> FormUI:
        with st.form('Form_ChangePassword', clear_on_submit=True, border=False):
            cp_old_pw = st.text_input(
                'Введите старый пароль', max_chars=32, type='password', 
                placeholder='Не должен совпадать с новым паролем'
            )

            col_new_pw, col_confirm_pw = st.columns(2)
            cp_new_pw = col_new_pw.text_input(
                'Введите новый пароль', max_chars=32, type='password', 
                placeholder='Не используйте простой пароль'
            )
            cp_confirm_pw = col_confirm_pw.text_input(
                'Подтвердите новый пароль', max_chars=32, type='password', 
                placeholder='Должен совпадать с новым паролем'
            )

            if st.form_submit_button('Изменить', type='primary'):
                if cp_old_pw != '' and cp_new_pw != '':
                    if (
                        cp_new_pw == cp_confirm_pw and 
                        cp_new_pw != cp_old_pw
                    ):
                        output_msg = self.h_profile.change_password(
                            self.s_username, cp_old_pw, cp_new_pw
                        )

                        if output_msg['state'] == ChangePasswordStates.SUCCESS:
                            st.success(output_msg['msg'], icon='✔️')
                        elif output_msg['state'] == ChangePasswordStates.FAIL:
                            st.warning(output_msg['msg'], icon='⚠️')
                    else: st.warning('Пароли не совпадают.', icon='⚠️')
                else: st.warning('Необходимо заполнить все поля.', icon='⚠️')
