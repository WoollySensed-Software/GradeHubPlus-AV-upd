import streamlit as st

from streamlit_option_menu import option_menu
from GradeHubPlusApp.handlers.h_common import AddEmailStates, ChangeEmailStates
from GradeHubPlusApp.handlers.h_notify import EmailNotificationH
from GradeHubPlusApp.handlers.h_profile import ProfileH


class ProfileUI:

    def __init__(self, username: str, full_name: str, role: str):
        self.s_username = username
        self.s_full_name = full_name
        self.s_role = role
        self.h_profile = ProfileH()
        self.h_email_notify = EmailNotificationH()
    
    def setupUI(self):
        options = ('Аккаунт', 'Настройки')
        selector_mode = option_menu(
            menu_title=None, 
            orientation='horizontal', 
            options=options, 
            styles=None
        )

        # --- аккаунт ---
        if selector_mode == options[0]:
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
                st.markdown(f'### {info['kword']}: :red[{info['link']}]')

        # --- настройки ---
        if selector_mode == options[1]: self.__settings()

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
        else: notify_status = ':yellow[Выключена]'

        if notify_mode == 'Email':
            kword = 'Почта'
            notify_mode = f':red[{kword}]'
        elif notify_mode == 'Telegram':
            kword = 'Телеграм'
            notify_mode = f':red[{kword}]'
        else:
            kword = 'Не указано'
            notify_mode = f':yellow[{kword}]'

        if link == 'Undefined': link = ''

        return {
            'role': role, 
            'regDate': reg_date, 
            'notifyStatus': notify_status, 
            'notifyMode': notify_mode, 
            'link': link, 
            'kword': kword
        }

    def __settings(self):
        with st.expander(':red[Управление почтой]'):
            notify_mode = self.h_email_notify.get_notify_mode(self.s_username)

            # --- добавление ---
            if notify_mode == 'Undefined':
                self.__from_add_notify_mode()
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
                if notify_mode == 'Email':
                    self.__form_change_email_link()

    def __from_add_notify_mode(self):
        with st.form('Form_AddNotifyMode', clear_on_submit=True, border=True):
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
                    if self.h_email_notify.validate_email(anm_link):
                        output_msg = self.h_email_notify.add_email(
                            self.s_username, anm_link
                        )

                        if output_msg['state'] == AddEmailStates.SUCCESS:
                            st.success(output_msg['msg'], icon='✔️')
                        elif output_msg['state'] == AddEmailStates.FAIL:
                            st.warning(output_msg['msg'], icon='⚠️')
                    else: st.warning('Невалидная почта', icon='⚠️')
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

    def __form_change_email_link(self):
        with st.form('Form_ChangeEmailLink', clear_on_submit=True, border=True):
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
                    if cel_new_link == cel_confirm_link:
                        if self.h_email_notify.validate_email(cel_new_link):
                            output_msg = self.h_email_notify.change_email(
                                self.s_username, cel_old_link, cel_new_link
                            )

                            if output_msg['state'] == ChangeEmailStates.SUCCESS:
                                st.success(output_msg['msg'], icon='✔️')
                            elif output_msg['state'] == ChangeEmailStates.FAIL:
                                st.warning(output_msg['msg'], icon='⚠️')
                        else: st.warning('Невалидная почта', icon='⚠️')
                else: st.warning(
                    'Необходимо заполнить все поля.', icon='⚠️'
                )
