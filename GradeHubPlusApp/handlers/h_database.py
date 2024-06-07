from deta import Deta
from GradeHubPlusApp.config.settings import KEY_DETA


class DatabaseH:
    """
    Класс для работы с базой данных.
    """

    def __init__(self):
        self.db = Deta(KEY_DETA)
        self.db_keys = self.db.Base('keys')
        self.db_notify = self.db.Base('notify')
        self.db_users = self.db.Base('users')
        self.db_students = self.db.Base('students')
        self.db_subjects = self.db.Base('subjects')
        self.db_scores = self.db.Base('scores')
