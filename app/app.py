from .bin.database import Database_mysql
from .bin.settings import *

class App():
    database_obj = Database_mysql(LOGIN_str, PASSWORD_str, HOST_str, SCHEMA_str)
    settings_obj = Settings()

    def process_cf(self):
        pass
