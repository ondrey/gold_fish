# -*- coding: utf-8 -*-

from hashlib import md5
from json import dumps, loads
from random import choice

from flask import request
from flask import session
from flask import redirect, url_for
from flask import Response
from flask import current_app as app

from ObjectAPI import ObjectAPI
from ObjectDb import ObjectDb


def isauth(f):
    """
    Декоратор для проверки авторизации пользователя
    :param f:
    :return:
    """

    def wrapper(sl):
        if 'client_sess' in session and u'admin' in session['client_sess']['groups']:
            return f(sl)
        else:
            if 'app_key' in request.values and request.values['app_key'] == app.config.get('API_KEY'):
                return f(sl)
            else:
                return redirect(url_for('index'))

    return wrapper


class Auth(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.groups = {}

    def api_logout(self):
        """
        Удалить переменную сесии
        :return:
        """
        session.pop('client_sess', None)
        return Response(dumps(0), mimetype='application/json')

    def api_check(self):
        """
        Переопределить сессию авторизации
        :return:
        """
        form = loads(request.form['request'])

        if 'login' in form['record'] and 'password' in form['record']:

            sql = u"""
            SELECT ug.title_user_group, ug.id_user_group FROM user_groups_link gl 
                INNER JOIN users u ON u.id_user = gl.id_user
                INNER JOIN user_group ug ON ug.id_user_group = gl.id_group

                WHERE u.login_user = %s AND u.password_user = %s
                AND u.is_activ = 1 AND ug.is_activ = 1
            """
            cur = self.connect.cursor()
            cur.execute(sql, [form['record']['login'], self.__pas_digest(form['record']['password']), ])

            for row in cur.fetchall():
                session['client_sess'] = {}
                session['client_sess'] = {'groups': [row[0], ], 'login': form['record']['login']}
                self.get_child_group(row[1], cur)

                session['client_sess']['groups'] += self.groups.keys()

                return dumps({'status': 'success', 'message': session['client_sess']})

            return dumps({'status': 'error', 'message': u"Пользователь не найден"})
        else:
            return dumps({'status': 'error', 'message': u"Нет одного из параметров"})

    def __pas_digest(self, pas):
        md = md5()
        md.update(pas.encode('utf8'))
        return md.hexdigest()

    def get_child_group(self, id_parent, cur):

        cur.execute(u"""
            SELECT ug.title_user_group, ug.id_user_group FROM user_group ug                
                WHERE ug.id_parent_user_group = %s and ug.id_parent_user_group != ug.id_user_group 
                AND ug.is_activ = 1        
        """, id_parent)

        for row in cur.fetchall():
            self.groups[row[0]] = 1
            self.get_child_group(row[1], cur)

    def wassgen(self, length=6):
        """
        Генератор паролей
        :return:
        """
        pas = []
        for i in range(length):
            pas.append(choice('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-='))
        return ''.join(pas)