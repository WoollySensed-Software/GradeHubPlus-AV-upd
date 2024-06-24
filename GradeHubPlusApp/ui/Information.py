import streamlit as st

from streamlit_extras.mention import mention

from GradeHubPlusApp.handlers.common.types import PageUI


class InformationUI:

    def setupUI(self) -> PageUI:
        # --- О разработке сайта ---
        st.subheader(':red[О разработке сайта]', anchor=False, divider='red')
        col_left, _, col_right = st.columns([0.45, 0.1, 0.45])

        with col_left:
            st.markdown(self.__extract_text('text_1.txt'))
            
            _, col_center, _ = st.columns([0.25, 0.5, 0.25])
            col_center.image(
                './GradeHubPlusApp/resources/media/Final_logo_WS_512x512.png', 
                width=300
            )

        col_right.markdown(self.__extract_text('text_2.txt'))

        # --- Про GradeHub+ ---
        st.subheader(':red[Про GradeHub+]', anchor=False, divider='red')
        st.markdown(self.__extract_text('text_3.txt'))
        
        col_left_2, _, col_right_2 = st.columns([0.3, 0.1, 0.6])
        col_right_2.markdown(self.__extract_text('text_4.txt'))

        col_left_2.image('./GradeHubPlusApp/resources/media/media_file_1.gif')
        col_left_2.image('./GradeHubPlusApp/resources/media/media_file_2.gif')
        col_left_2.image('./GradeHubPlusApp/resources/media/media_file_3.gif')


        # TODO: сделать раздел для преподавателей
        # st.subheader(':red[Руководство для преподавателей]', anchor=False, divider='red')
        # TODO: сделать раздел для студентов
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

    def __extract_text(self, file: str) -> str:
        path = f'GradeHubPlusApp/resources/text/{file}'
        
        with open(path, 'r', encoding='utf-8') as f:
            return ''.join(f.readlines())
