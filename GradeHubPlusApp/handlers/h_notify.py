import smtplib

from email_validate import validate
from email.mime.text import MIMEText
from GradeHubPlusApp.config.settings import (
    NOTIFY_EMAIL, NOTIFY_PW, NOTIFY_SERVER, NOTIFY_PORT
)
from GradeHubPlusApp.handlers.h_database import DatabaseH


class EmailNotification(DatabaseH):

    def __init__(self):
        super().__init__()

    def validate_email(self, email: str):
        return validate(
            email_address=email, 
            check_format=True, 
            check_blacklist=True, 
            check_dns=True, 
            dns_timeout=10, 
            check_smtp=False, 
            smtp_debug=False
        )
    
    def get_email(self): pass  # получить данные из БД
    def new_email(self): pass  # первое добавление почты в БД
    def change_email(self): pass  # изменение почты в БД

    def send_score_notify(self, 
        moder_username: str, 
        subject: str, 
        score: int, 
        users: list
    ):
        # TODO: сделать нужную валидацию | добавить возможность узнать 
        # сколько у пользователя баллов на данный момент по предмету

        msg = (
            f'Здравствуйте, [Full Name].\n\n' + 
            f'[Moderator] выставил Вам баллы: [Score]\n' + 
            f'по предмету: [Subject].\n' + 
            f'На данный момент по этому предмету у Вас [All Score] балл(ов).\n\n\n\n' + 
            'Вы сможете узнать баллы по остальным предметам на главной странице, ' + 
            'после авторизации на сайте:\nhttps://gradehu6plus-av.streamlit.app'
        )
        # FIXME: указать почту пользователя вместо 'Email'
        self.__send_email('Email', 'Уведомление от GradeHub+', msg)

    def __send_email(self, to_email: str, subject: str, body: str):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = NOTIFY_EMAIL
        msg['To'] = to_email

        try:
            with smtplib.SMTP(NOTIFY_SERVER, NOTIFY_PORT) as server:
                server.login(NOTIFY_EMAIL, NOTIFY_PW)
                server.sendmail(NOTIFY_EMAIL, to_email, msg.as_string())
        except smtplib.SMTPException as err:
            print('Не удалось отправить письмо!')

# возможность отправки уведомлений через телеграм-бота будет позже...
class TelegramNotification(DatabaseH): pass
