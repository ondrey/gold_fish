
import pymysql
from flask import current_app as app


class ObjectDb:
    def __init__(self):
        self.connect = pymysql.connect(**app.config.get('DB_CONNECT'))

    def __del__(self):
        self.connect.commit()
        self.connect.close()
