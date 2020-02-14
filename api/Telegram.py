# -*- coding: utf-8 -*-
from ObjectAPI import ObjectAPI
from ObjectDb import ObjectDb
from Auth import isauth


class Auth(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    @isauth
    def api_get_link_download(self):
        """
        Получить ссылку на скачивание бота для указанного пользователя
        Имеют доступ только авторизованные пользователи.
        :return:
        """
        pass

    @isauth
    def check_new_chat(self):
        """
        Проверка новых пользователей подключившихся по ссылке, регистрация
        :return:
        """

    @isauth
    def send_message(self, text):
        """
        Отправить сообщение авторизованному пользователю
        :param text:
        :return:
        """