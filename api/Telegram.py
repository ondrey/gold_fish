from flask import current_app as app
from flask import request
from flask_mail import Mail
from api.ObjectAPI import ObjectAPI
from api.ObjectDb import ObjectDb
from flask import jsonify
import re


class Telegram(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    def api_qwerty(self):
        if request.method == "POST":

            # mail = Mail(app)
            # mail.send_message("Сообщение от бота Ответ от кнопки", recipients=['mag.ondrei@gmail.com', ],
            #                   html=str(request.json))

            if 'entities' in request.json['message']:
                command = None
                for ent in request.json['message']['entities']:
                    if ent['type'] == 'bot_command':
                        command = request.json['message']['text'][ent['offset']+1: ent['length']]

                if command:
                    cmd = "cmd_{0}".format(command)
                    if hasattr(self, cmd):
                        api_function = getattr(self, cmd)
                        result = {"method": "sendMessage", "chat_id": request.json['message']['chat']['id'],}
                        try:
                            result.update(api_function(request.json['message']))
                        except Exception as ex:
                            result.update({"text": "Не удалось выполнить команду. Ошибка на сервере."})
                        return result

        return jsonify({})

    def cmd_start(self, params):
        code = ''.join(re.findall(r'\d', params['text']))
        cur = self.connect.cursor()
        cur.execute("select id, name_user from Users where telegram_add_code={0}".format(code))
        first = cur.fetchone()
        if first:
            cur.execute("update Users telegram_chat_id={0} where telegram_add_code={1}".format(
                params['chat']['id'],
                code,
            ))
            self.connect.commit()
            return {"text": "Добро пожаловать ув. {0}.".format(first[1])}
        else:
            return {"text": "Добро пожаловать. Для того чтобы начать пользоваться ботом, привяжите аккаунт. "
                            "Для этого необходимо авторизоваться на сайте kojima.su, затем в разделе настройки "
                            "пользователя скопировать команду и отправить этому боту."}

    def cmd_restart_flask(self, params):
        return {"text": "Вы ввели команду РЕСТАРТ"}

    def cmd_echo(self, params):
        return {"text": "Вы ввели команду {0}".format(str(params))}

    def botton_save_categories(self):
        pass