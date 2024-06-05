from GradeHubPlusApp.handlers.h_database import DatabaseH


class ProfileH(DatabaseH):

    def __init__(self):
        super().__init__()

    def get_reg_date(self, username: str):
        return self.db_users.fetch({'key': username}).items[0]['date']
