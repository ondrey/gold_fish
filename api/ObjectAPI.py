# -*- coding: utf-8 -*-
from flask import abort
from json import dumps


class ErrorAPI(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(ErrorAPI, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class ObjectAPI:
    """
    Если мы захотим реализовать стандарт работы АПИ, лучше делать это в этом классе.
    А пока тут запускатор методов по имени
    """
    def __init__(self):
        pass

    def run_api_method(self, name_method):
        """
        Запустить метод обработчик если он объявлен в экземпляре класса с префиксом api_.
        :return: Результат работы
        """
        fnm = 'api_{0}'.format(name_method)
        if hasattr(self, fnm):
            api_function = getattr(self, fnm)
            try:
                return api_function()
            except ErrorAPI, ex:
                return dumps(dict(user_mess=ex.message, type_mess=ex.errors), ensure_ascii=True)

        abort(404)
