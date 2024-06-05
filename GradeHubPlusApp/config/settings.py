from streamlit import secrets as ss
from GradeHubPlusApp.handlers.h_common import DtTools

# база данных
KEY_DETA = ss['database']['KEY']

# уведомления
NOTIFY_EMAIL = ss['notify']['EMAIL']
NOTIFY_PW = ss['notify']['PASSWORD']
NOTIFY_SERVER = ss['notify']['SERVER']
NOTIFY_PORT = ss['notify']['PORT']

# (global upd).(major upd).(minor upd)
APP_VERSION = '2.2.4'
_dt = DtTools.dt_now()
SIDEBAR_INFO = (
    f'Версия: {APP_VERSION}\n\n' + 
    f'Патч от: {_dt:%d-%m-%Y} | {_dt:%H:%M}'
)
