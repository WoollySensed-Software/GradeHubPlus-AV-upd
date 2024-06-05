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
        moder_full_name: str, 
        subject: str, 
        work_type: str, 
        score: int, 
        students: list
    ):
        
        for student in students:
            full_name, _dir, course = student.split(' - ')
            notidy_data = self.db_notify.fetch({'isEnable': 'Yes'}).items

            if notidy_data != []:
                for i in notidy_data:
                    if i['fullName'] == full_name:
                        data = self.db_scores.fetch({
                            'moder': moder_username, 
                            'student': student
                        }).items[0]
                        msg = (
                            f'Здравствуйте, {full_name}.\n\n' + 
                            f'{moder_full_name} выставил Вам {score} балла(ов)\n' + 
                            f'по предмету: {subject}, за {work_type.lower()}.\n' + 
                            f'На данный момент по этому предмету у Вас ' + 
                            f'{data['score']} балл(ов).\n\n\n\n' + 
                            'Вы сможете узнать баллы по остальным ' + 
                            'предметам на главной странице, ' + 
                            'после авторизации на сайте:\n' + 
                            'https://gradehu6plus-av.streamlit.app'
                        )
                        self.__send_notify(
                            i['link'], 'Уведомление от GradeHub+', msg
                        )
    # FIXME: не работает
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

    # отправка работает
    def __send_notify(self, to_email: str, subject: str, message: str):
        # Кодировка письма
        charset = 'Content-Type: text/plain; charset=utf-8'
        mime = 'MIME-Version: 1.0'

        # Формирование тела письма
        body = '\r\n'.join((
            f'From: {NOTIFY_EMAIL}',
            f'To: {to_email}',
            f'Subject: {subject}',
            mime, charset, '', message
        ))

        try:
            # Подключение к почтовому сервису
            smtp = smtplib.SMTP(NOTIFY_SERVER, NOTIFY_PORT)
            smtp.starttls()
            smtp.ehlo()
            # Вход в почтовый сервер
            smtp.login(NOTIFY_EMAIL, NOTIFY_PW)
            # Отправка письма
            smtp.sendmail(NOTIFY_EMAIL, to_email, body.encode('utf-8'))
        except smtplib.SMTPException as error:
            print('Не удалось отправить письмо...')
            raise error
        finally: smtp.quit()

# возможность отправки уведомлений через телеграм-бота будет позже...
class TelegramNotificationH(DatabaseH): pass
