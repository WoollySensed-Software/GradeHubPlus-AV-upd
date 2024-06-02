from streamlit import secrets as ss
from GradeHubPlus.handlers.h_common import DtTools

# secret variables
DETA_KEY = ss['DATABASE']['KEY']
EMAIL = ss['NOTIFY']['EMAIL']
PW = ss['NOTIFY']['PW']
SERVER = ss['NOTIFY']['SERVER']
PORT = ss['NOTIFY']['PORT']

# (global upd).(major upd).(minor upd)
APP_VERSION = '2.2.0'
_dt = DtTools.dt_now()
SIDEBAR_INFO = (
    f'Версия: {APP_VERSION}\n\n' + 
    f'Патч от: {_dt:%d-%m-%Y} | {_dt:%H:%M}'
)