# -*- coding: utf-8 -*-
from datetime import timedelta


class Config(object):
    NAME_PROGECT = u"APIrator"
    DEBUG = False
    SECRET_KEY = '\x00\xf1\x00Bv\x990\\1\x04\xe1\xe3g'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1000)
    ADMIN_ACCOUNT = {}
    TASKS_KEY = "1U6iWrABx0qBBOjwG5xrFyaASig6N0xpn9BP"
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class ProductionConfig(Config):
    DEBUG = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)


class DevelopmentConfig(Config):

    DEBUG = True
    SECRET_KEY = '\x00\xf1\x00Bv\x97\x97K\x11w\xd0vJ\xcfL\xf2\xcf\x90\\1\x04\xe1\xe3g'
    ADMIN_ACCOUNT = {
        "login": "admin",
        "password": "911",
        "email": "mag.ondrei@gmail.com"
    }


class TestingConfig(Config):
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
    DEBUG = False


class DevelopmentTemplateConfig(Config):

    DEBUG = True
    SECRET_KEY = '\x00\xf1\x00Bv\x97\x97K\x11w\xd0vJ\xcfL\xf2\xcf\x90\\1\x04\xe1\xe3g'

    DB_CONNECT = dict(db='kojima', user='prokat', passwd='prokatmysql', host='89.108.99.136', port=3306, charset='cp1251')

    ADMINS = ['square.wind@yandex.ru', ]
    ERROR_COMMENT = u"При возникновении сложностей, свяжитесь с администратором по телефону: +7 (967) 667 67 91."
    TELEGRAM = "407030035:AAErYfnXpoVydKj3LGdH-gQuh91q7g-"
    SAVE_FILE_PATH = 'C:\\Users\\andrey\\Файлы апиратора'
    API_KEY = '1U6iWrABx0qBBOjwG5xrFyaASig6N0xpn9BP'

    # email server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
#    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'mag.ondrei@gmail.com'
    MAIL_PASSWORD = 'bdabilpfrtwnoijx'
    MAIL_DEFAULT_SENDER = (u'Макрушин Андрей', 'mag.ondrei@gmail.com')