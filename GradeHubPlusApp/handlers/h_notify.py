import smtplib

from email_validate import validate
from email.mime.text import MIMEText
from GradeHubPlusApp.config.settings import (
    NOTIFY_EMAIL, NOTIFY_PW, NOTIFY_SERVER, NOTIFY_PORT
)
from GradeHubPlusApp.handlers.h_database import DatabaseH
from GradeHubPlusApp.handlers.h_common import (
    AddEmailOutputMsg, ChangeEmailOutputMsg, 
    AddEmailStates, ChangeEmailStates
)


class EmailNotificationH(DatabaseH):

    def __init__(self):
        super().__init__()
    
    def get_notify_status(self, username: str) -> str:
        return self.db_notify.fetch({'key': username}).items[0]['isEnable']

    def change_notify_status(self, username: str) -> None:
        notify_status = self.get_notify_status(username)
        value = 'Yes' if notify_status == 'No' else 'No'
        self.db_notify.update({'isEnable': value}, username)

    def get_notify_mode(self, username: str) -> str:
        return self.db_notify.fetch({'key': username}).items[0]['mode']

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
    
    def get_link(self, username: str) -> str:
        return self.db_notify.fetch({'key': username}).items[0]['link']

    def add_email(self, username: str, link: str) -> AddEmailOutputMsg:
        if self.get_notify_status(username) == 'No':
            self.db_notify.update({
                'mode': 'Email', 
                'link': link
            }, username)
            output_msg = {
                'state': AddEmailStates.SUCCESS, 
                'msg': 'Данный метод успешно добавлен в БД.'
            }
        else: output_msg = {
            'state': AddEmailStates.FAIL, 
            'msg': 'Не удалось добавить почту в БД.'
        }
        
        return output_msg

    def change_email(self, 
        username: str, 
        old_link: str, 
        new_link: str
    ) -> ChangeEmailOutputMsg:
        if self.get_link(username) == old_link:
            self.db_notify.update({'link': new_link}, username)
            output_msg = {
                'state': ChangeEmailStates.SUCCESS, 
                'msg': 'Почта успешно изменена.'
            }
        else: output_msg = {
            'state': ChangeEmailStates.FAIL, 
            'msg': 'Не удалось изменить почту.'
        }
        
        return output_msg


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
class TelegramNotificationH(DatabaseH): pass
