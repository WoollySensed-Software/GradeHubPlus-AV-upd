import streamlit as st

from streamlit_option_menu import option_menu

from GradeHubPlusApp.config.settings import SIDEBAR_INFO
from GradeHubPlusApp.handlers.common.API import logout
from GradeHubPlusApp.handlers.common.cache import Menippe
from GradeHubPlusApp.ui.Authorization import AuthorizationAUI
from GradeHubPlusApp.ui.Home import HomeUI
from GradeHubPlusApp.ui.Profile import ProfileUI

# --- состояние сессии
if 'Auth-Status' not in st.session_state:
    st.session_state['Auth-Status'] = False
if 'Fullname' not in st.session_state:
    st.session_state['Fullname'] = None
if 'Username' not in st.session_state:
    st.session_state['Username'] = None
if 'Role' not in st.session_state:
    st.session_state['Role'] = None
if 'Selector-Menu' not in st.session_state:
    st.session_state['Selector-Menu'] = (
        'Авторизация', 'Информация'
    )
if 'Selector-Icons' not in st.session_state:
    st.session_state['Selector-Icons'] = (
        'person-fill-lock', 'info-circle-fill'
    )
if 'Cache-settings-vault_size' not in st.session_state:
    st.session_state['Cache-settings-vault_size'] = 10
if 'Cache-settings-optimization' not in st.session_state:
    st.session_state['Cache-settings-optimization'] = True

# --- параметры страницы ---
st.set_page_config(
    page_title='GradeHub+', 
    page_icon='./GradeHubPlusApp/resources/media/ghp_icon.png', 
    layout='wide'
)

# --- боковая панель ---
st.logo('./GradeHubPlusApp/resources/media/GHP_full_logo.png')
with st.sidebar:
    st.markdown(SIDEBAR_INFO)
    st.write('---')
    selector_mode = option_menu(
        menu_title='Страницы:',
        menu_icon='list-nested',  
        icons=st.session_state['Selector-Icons'], 
        options=st.session_state['Selector-Menu'], 
        styles=None
    )

# --- для неавторизованного пользователя
if not st.session_state['Auth-Status']:
    if selector_mode == 'Авторизация':
        authorization_ui = AuthorizationAUI()
        authorization_ui.setupUI()
    elif selector_mode == 'Информация':
        # about_ui = AboutUI()
        # about_ui.setupUI()
        ...
# --- для авторизованного пользователя
elif st.session_state['Auth-Status']:
    # настройка параметров кэширования
    menippe = Menippe()
    menippe.settings(
        optimization=st.session_state['Cache-settings-optimization'], 
        vault_size=st.session_state['Cache-settings-vault_size']
    )

    st.sidebar.button('Выйти из аккаунта', on_click=logout)
    st.sidebar.write('---')

    if selector_mode == 'Главная':
        home_ui = HomeUI(
            st.session_state['Username'], 
            st.session_state['Fullname'], 
            st.session_state['Role']
        )
        home_ui.setupUI()
    elif selector_mode == 'Профиль':
        profile_ui = ProfileUI(
            st.session_state['Username'], 
            st.session_state['Fullname'], 
            st.session_state['Role']
        )
        profile_ui.setupUI()
    elif selector_mode == 'Информация':
        # about_ui = AboutUI()
        # about_ui.setupUI()
        ...
