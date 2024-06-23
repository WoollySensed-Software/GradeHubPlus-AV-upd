import streamlit as st

from sys import version_info

from streamlit_extras.mention import mention


class InformationUI:

    def __init__(self):
        pass

    def setupUI(self):
        # --- О разработке сайта ---
        st.subheader(':red[О разработке сайта]', anchor=False, divider='red')
        col_left, _, col_right = st.columns([0.45, 0.1, 0.45])

        with col_left:
            text_1 = """
                Мы **:red[WoollySensed Software]** - Ваш партнер в разработке 
                программного обеспечения, сайтов и приложений. Мы являемся 
                IT-компанией, специализирующейся на разработке программного 
                обеспечения, сайтов, API и приложений для ПК.
            """
            st.markdown(text_1)
            
            _, col_center, _ = st.columns([0.25, 0.5, 0.25])
            col_center.image(
                './GradeHubPlusApp/resources/media/Final_logo_WS_512x512.png', 
                width=300
            )

        with col_right:
            text_2 = """
                **:red[Наши качества в работе]**: 
                - **:red[Опыт и экспертиза]**: Мы ведем деятельность в сфере IT 
                с февраля 2023 года. За это время мы накопили богатый 
                опыт и построили крепкую репутацию в качестве надежного 
                партнера для наших клиентов.
                - **:red[Индивидуальный подход]**: Мы полностью погружаемся в проекты 
                наших клиентов и стремимся понять их потребности и цели. 
                Мы гарантируем индивидуальный подход к каждому проекту, 
                чтобы предоставить решения, которые наилучшим образом 
                соответствуют вашим требованиям.
                - **:red[Качество и надежность]**: Мы придерживаемся высоких стандартов 
                качества и стремимся к безупречности в каждом аспекте нашей работы. 
                Мы предлагаем надежные и эффективные решения, которые помогут вам 
                достичь ваших целей и преуспеть в вашем бизнесе.
            """
            st.markdown(text_2)

        # --- Про GradeHub+ ---
        st.subheader(':red[Про GradeHub+]', anchor=False, divider='red')
        text_3 = f"""
            Целью сайта является улучшение взаимодействия между студентом 
            и преподавателем. Преподаватель выставляет баллы студентам - 
            студенты видят их у себя, все довольны.

            Сайт написан на фреймворке `Streamlit {st.__version__}` на языке 
            `Python {version_info.major}.{version_info.minor}.{version_info.micro}`. 
            Давайте разберемся с особенностями сайта, без понимания которых у Вас 
            могут возникнуть вопросы:
        """
        text_4 = """
            1. **:red[Обноление страницы сайта]**: Для того, чтобы обновить данные на 
            странице сайта, нужно нажать на клавиатуре `R` (*только англ. раскладка*) 
            или нажать `три точки в правом верхнем углу -> Rerun`. Если Вы попытаетесь 
            вручную обновить страницу, например через `F5`, то текущая сессия браузера 
            сбросится до начального состояния (*данные могут не сохраниться*) и Вам 
            придется снова входить в свой аккаунт.

            2. **:red[Вход в аккаунт]**: После успешной авторизации в аккаунт, 
            Вы увидите соответствующую надпись под формой. Чтобы дальше попасть на 
            главную страницу или профиль, Вы можете самостоятельно обновить страницу 
            (*как это правильно сделать написано в 1 пункте*) или еще раз нажать 
            на кнопку `Войти`.

            3. **:red[Навигация]**: Для переключения страниц на сайте используется 
            боковая выдвижная панель, чтобы ее убрать/выдвинуть нужно нажать на 
            стрелочку напротив логотипа сайта `GradeHub+`. По умолчанию боковая 
            панель уже выдвинута на версии для ПК, но на версии для портативных 
            устройств ее нужно выдвигать самостоятельно.

            4. **:red[Главная страница]**: В зависимости от того, кем Вы являетесь, 
            главная страница будет выглядеть по разному. Например: у студента будет 
            отображаться таблица с его баллами по предмету (*таблица будет пуста, 
            если в базе данных, далее БД, нет записи с баллами*); у преподавателя 
            будет отображаться таблица с баллами студентов (*только тех студентов, 
            которым преподаватель выставил баллы*) и дополнительный функционал для 
            работы со студентами.

            5. **:red[Профиль]**: На странице профиля Вы сможете найти два раздела: 
            `Аккаунт` и `Настройки`. В первом разделе можно увидеть некоторую 
            информацию о Вас, а во втором можно, например, изменить пароль 
            от Вашего аккаунта и тп.
        """
        st.markdown(text_3)
        
        col_left_2, _, col_right_2 = st.columns([0.3, 0.1, 0.6])
        col_right_2.markdown(text_4)

        col_left_2.image('./GradeHubPlusApp/resources/media/media_file_1.gif')
        col_left_2.image('./GradeHubPlusApp/resources/media/media_file_2.gif')
        col_left_2.image('./GradeHubPlusApp/resources/media/media_file_3.gif')


        # st.subheader(':red[Руководство для преподавателей]', anchor=False, divider='red')
        
        # st.subheader(':red[Руководство для студентов]', anchor=False, divider='red')

        # --- Футер ---
        st.subheader(':red[Связь с нами]', anchor=False, divider='red')
        col_left, col_right = st.columns(2)

        with col_left:
            mention(
                ':red[Почта] — woollysensed.software@gmail.com', 
                'woollysensed.software@gmail.com', 
                'https://cdn-icons-png.flaticon.com/128/732/732200.png'
            )
        
        with col_right:
            mention(
                ':red[Вконтакте] — Данила Расстригин (:red[администратор])', 
                'https://vk.com/huayrav', 
                'https://cdn-icons-png.flaticon.com/128/3536/3536582.png'
            )
