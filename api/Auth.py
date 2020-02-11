# -*- coding: utf-8 -*-

from hashlib import md5
from json import dumps, loads
from random import choice
from uuid import uuid4


from flask import request
from flask import session
from flask import redirect, url_for
from flask import Response
from flask import render_template
from flask import current_app as app
from flask_mail import Mail

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

    def api_page_login(self):
        return render_template('auth/login.html')

    def api_page_newuser(self):
        return render_template('auth/newuser.html')

    def api_page_repass(self):
        return render_template('auth/repassword.html')

    def api_logout(self):
        """
        Удалить переменную сесии
        :return:
        """
        session.pop('client_sess', None)
        return Response(dumps(0), mimetype='application/json')

    def wassgen(self, length=6):
        """
        Генератор паролей
        :return:
        """
        pas = []
        for i in range(length):
            pas.append(choice('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-='))
        return ''.join(pas)

    def api_activ_user(self):
        code = request.query_string
        cur = self.connect.cursor()
        cur.execute(u"UPDATE Users SET code_activ_user = '' WHERE code_activ_user = %s ", (code,))
        self.connect.commit()
        return render_template('login.html', mess=u"Пользователь активирован, попробуйте авторизоваться!")

    def api_re_access(self):
        if 'user_mail' in request.form:
            cur = self.connect.cursor()
            cur.execute(u"select id_user from Users where email_user = %s", (request.form['user_mail'], ))
            for i in cur.fetchall():
                mail = Mail(app)
                session['repass_code'] = uuid4().hex
                session['repass_email'] = request.form['user_mail']

                mail.send_message("Востановление доступа - Kojima", recipients=[request.form['user_mail'], ],
                                  html=render_template('email_tmp/reaccess.html',
                                                       host=request.host, code=session['repass_code']))

                return render_template('auth/repassword.html', mess=u"На указанный email отправленна ссылка для "
                                                               u"востановления доступа. Проверьте почтовый ящик.")

            return render_template('auth/repassword.html', mess=u"Пользователь с такими данными не зарегистрирован в базе.")

    def api_re_pass(self):
        if 'code_mail' in request.values:
            return render_template('auth/repassword2.html', code=request.values['code_mail'])
        elif 'code' in request.form:
            if request.form['pass'] == request.form['repass']:
                if 'repass_code' in session and 'repass_email' in session:
                    cur = self.connect.cursor()
                    cur.execute(u"update Users set password_user=%s where email_user=%s", (request.form['repass'], session['repass_email']))
                    self.connect.commit()
                    redirect(url_for('/auth/page_login'))
                else:
                    return render_template('auth/repassword.html', mess=u"Срок действия кода востановления истёк.")
            else:
                return render_template('auth/repassword2.html', code=request.values['code'], mess=u"Пароли не совпадают")
        else:
            return render_template('auth/repassword.html')

    def api_create_user(self):
        error = []
        mail = Mail(app)

        if len(request.form) == 6:
            if len(request.form['user_password1']) < 6:
                error.append(u"Пароль менее шести символов - слишком слабый.")
            else:
                if request.form['user_password1'] != request.form['user_password2']:
                    error.append(u"Пароли не совпадают.")
                else:
                    cur = self.connect.cursor()
                    cur.execute(u"select * from Users where email_user=%s", (request.form['user_mail']))

                    for row in cur.fetchall():
                        error.append(u"Пользователь с таким email уже зарегистрирован.")

        else:
            error.append(u"Не хватает параметров.")

        id_ref_user = None

        if request.form['ref']:
            curef = self.connect.cursor()
            curef.execute(u"select id_user from Users where guid_user=%s", (request.form['ref']))

            for row in curef.fetchall():
                id_ref_user = row[0]

        if len(error) > 0:
            return render_template('newuser.html', errors=error)
        else:
            sql = u"INSERT INTO Users(password_user, email_user, code_activ_user, name_user, guid_user, id_manager_user) " \
                  u"VALUES (%s, %s, %s, %s, %s, %s)"
            code = uuid4().hex

            cur.execute(sql, (
                md5(request.form['user_password1']).hexdigest()
                , request.form['user_mail']
                , code
                , request.form['name'],
                uuid4().hex,
                id_ref_user
            ))

            html = u"<p>Пройдите по ссылке, для подтверждения регистрации <a href=\"http://"+request.host+u"/auth/activ_user?"+code+u"\"> активация </a> </p>"
            mail.send_message("Подтверждение регистрации", recipients=["spark-mag@yandex.ru"], html=html)

            return render_template('newuser.html', errors = [], finish = u"Пользователь зарегистрирован в базе. Инструкция по активации выслана на указанный email.")