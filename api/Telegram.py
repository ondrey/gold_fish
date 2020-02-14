# -*- coding: utf-8 -*-
from ObjectAPI import ObjectAPI
from ObjectDb import ObjectDb
from Auth import isauth


class Auth(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    def check_new_chat(self):
        """
        Проверка новых пользователей подключившихся по ссылке, регистрация
        :return:
        """

    def send_message(self, text):
        """
        Отправить сообщение авторизованному пользователю
        :param text:
        :return:
        """