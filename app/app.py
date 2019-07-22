from .bin.database import Database_mysql
from .bin.settings import Settings

class App():
    database_obj = Database_mysql()
    settings_obj = Settings()

    def process_cf(self):
        pass