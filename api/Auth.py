

from hashlib import md5
from random import choice
from uuid import uuid4

from flask import jsonify
from flask import abort
from flask import request
from flask import session
from flask import redirect, url_for
from flask import current_app as app
from flask_mail import Mail


from api.ObjectAPI import render_tmp
from api.ObjectDb import ObjectDb
from api.ObjectAPI import ObjectAPI


def isauth(f):
    """
    Декоратор для проверки авторизации пользователя
    :param f:
    :return:
    """
    def wrapper(sl):
        if 'client_sess' in session:
            return f(sl)
        else:
            abort(404)

    return wrapper


class Auth(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.groups = {}

    def api_page_login(self):
        return render_tmp('auth/login.html')

    def api_page_newuser(self):
        return render_tmp('auth/newuser.html')

    def api_page_repass(self):
        return render_tmp('auth/repassword.html')

    @isauth
    def api_userinfo(self):
        if 'user_name' in request.form:
            cur = self.connect.cursor()
            sql = u"update Users set name_user='{0}' where id_user={1}".format(
                request.form['user_name'],
                str((session['client_sess']['id_user'])))
            cur.execute(sql)
            session['client_sess']['name_user'] = request.form['user_name']
            self.connect.commit()

        return render_tmp('auth/userinfo.html', code_emploey=session['client_sess']['guid_user'])

    def api_login(self):

        if 'user_mail' in request.form and 'user_password' in request.form:
            password = request.form['user_password']
            try:
                password = md5(password.encode()).hexdigest()
            except:
                return render_tmp('auth/login.html', mess=u"Пароль может состоять из символов латинского алфавита, цифр и знаков. Проверте раскладку!")

            cur = self.connect.cursor()
            cur.execute(u"""
                select us.id_user, us.email_user, us.name_user, us.id_manager_user, us.guid_user
                from Users us where us.email_user = '{0}' and us.password_user = '{1}' and us.code_activ_user is NULL        
            """.format(request.form['user_mail'], password))

            for row in cur.fetchall():
                session['client_sess'] = {}
                session['client_sess']['id_user'] = row[0]
                session['client_sess']['email_user'] = row[1]
                session['client_sess']['name_user'] = row[2]
                session['client_sess']['id_manager_user'] = row[3]
                session['client_sess']['guid_user'] = row[4]

                return redirect("/app")

            return render_tmp('auth/login.html', mess=u"Ошибка! Такого сочетания логина и пароля, не зарегистрированно.")
        else:
            return render_tmp('auth/login.html', mess=u"Не передан один из параметров")

    def api_logout(self):
        """
        Удалить переменную сесии
        :return:
        """
        session.pop('client_sess', None)
        return redirect(url_for('index'))

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
        cur.execute(u"UPDATE Users SET code_activ_user = NULL WHERE code_activ_user = %s ", (code,))
        self.connect.commit()
        return render_tmp('auth/login.html', mess=u"Пользователь активирован, попробуйте авторизоваться!")

    def api_re_access(self):
        if 'user_mail' in request.form:
            cur = self.connect.cursor()
            cur.execute(u"select id_user from Users where email_user = %s", (request.form['user_mail'], ))
            for i in cur.fetchall():
                mail = Mail(app)
                session['repass_code'] = uuid4().hex
                session['repass_email'] = request.form['user_mail']

                mail.send_message("Востановление доступа - Kojima", recipients=[request.form['user_mail'], ],
                                  html=render_tmp('email_tmp/reaccess.html',
                                                       host=request.host, code=session['repass_code']))

                return render_tmp('auth/repassword.html', mess=u"На указанный email отправленна ссылка для "
                                                               u"востановления доступа. Проверьте почтовый ящик.")

            return render_tmp('auth/repassword.html', mess=u"Пользователь с такими данными не зарегистрирован в базе.")

    def api_re_pass(self):
        if 'code_mail' in request.values:
            return render_tmp('auth/repassword2.html', code=request.values['code_mail'])
        elif 'code' in request.form:
            if request.form['pass'] == request.form['repass']:
                if 'repass_code' in session and 'repass_email' in session:

                    try:
                        md5(request.form['repass'].encode()).hexdigest()
                    except:
                        return render_tmp('auth/repassword2.html', code=request.values['code'],
                                          mess=u"Пароль может содержать только латинские буквы, символы и цыфры.")

                    cur = self.connect.cursor()
                    cur.execute(u"update Users set password_user=%s where email_user=%s", (
                        md5(request.form['repass'].encode()).hexdigest(), session['repass_email']))
                    self.connect.commit()
                    return render_tmp('auth/login.html', mess=u"Вы успешно сменили пароль. Попробуйте войти теперь.")
                else:
                    return render_tmp('auth/repassword.html', mess=u"Срок действия кода востановления истёк.")
            else:
                return render_tmp('auth/repassword2.html', code=request.values['code'], mess=u"Пароли не совпадают")
        else:
            return render_tmp('auth/repassword.html')

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

                    md5(request.form['user_password1'].encode()).hexdigest()

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

            if not(id_ref_user):
                error.append(u"Такой код проекта отсутствует.")

        if len(error) > 0:
            return render_tmp('auth/newuser.html', errors=error)
        else:
            sql = u"INSERT INTO Users(password_user, email_user, code_activ_user, name_user, guid_user, id_manager_user) " \
                  u"VALUES (%s, %s, %s, %s, %s, %s)"
            code = uuid4().hex

            cur.execute(sql, (
                md5(request.form['user_password1'].encode()).hexdigest()
                , request.form['user_mail']
                , code
                , request.form['name'],
                uuid4().hex,
                id_ref_user
            ))

            html = render_tmp('email_tmp/activate.html', host=request.host, code=code)
            mail.send_message("Подтверждение регистрации", recipients=[request.form['user_mail'],], html=html)

            return render_tmp('auth/newuser.html', errors = [], finish = u"Пользователь зарегистрирован в базе. Инструкция по активации выслана на указанный email.")