from flask import current_app as app
from flask import request
from flask_mail import Mail
from api.ObjectAPI import ObjectAPI
from api.ObjectDb import ObjectDb
from flask import jsonify
import re
import json

import pathlib
from urllib.request import urlopen



class Telegram(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.key_api = app.config.get('TELEGRAM')

    def api_qwerty(self):
        if request.method == "POST":

            mail = Mail(app)
            mail.send_message("Сообщение от бота Ответ от кнопки", recipients=['mag.ondrei@gmail.com', ],
                               html=str(request.json))

            if 'message' in request.json:
                result = {"method": "sendMessage", "chat_id": request.json['message']['chat']['id'],}
                is_transact = re.fullmatch(r"^(\d+[.,]?\d*)[\s]+(.*)$", request.json['message']['text'])
                
                if 'entities' in request.json['message']:
                    command = None
                    for ent in request.json['message']['entities']:
                        if ent['type'] == 'bot_command':
                            command = request.json['message']['text'][ent['offset']+1: ent['length']]

                    if command:
                        cmd = "cmd_{0}".format(command)
                        if hasattr(self, cmd):
                            api_function = getattr(self, cmd)                            
                            try:
                                result.update(api_function(request.json['message']))
                            except Exception as ex:
                                result.update({"text": "Не удалось выполнить команду. Ошибка на сервере."})
                        else:
                            result.update({"text": "Такой команды не существует."})                    

                elif bool(is_transact):
                    trinfo = is_transact.groups()
                    inline_keyboard = self.get_items_telegramm(request.json['message'], trinfo = is_transact.groups())
                    inline_keyboard.append([{"text":"Отмена", "callback_data": "-1"}])

                    result.update({"text": "Добавить транзакцию ?\n{0} {1}".format(trinfo[0], trinfo[1]),
                                   "reply_markup": {"inline_keyboard": inline_keyboard}
                                   })
                else:
                    result.update({"text": "Не понял! Для получения справки введите команду /help"})
                    
                return result, 200
            elif 'callback_query' in request.json:
                # Нажали кнопку


                if (request.json['callback_query']['data'] == '-1'):
                    result = {"method": "editMessageText",
                              "chat_id": request.json['callback_query']['message']['chat']['id'],
                              "message_id": request.json['callback_query']['message']['message_id'], "text": "Отмена."}
                else:
                    result = {"method": "editMessageText",
                              "chat_id": request.json['callback_query']['message']['chat']['id'],
                              "message_id": request.json['callback_query']['message']['message_id'],
                              "text": self.add_transaction(request.json['callback_query']['data'],
                                                           request.json['callback_query']['message']['text'])
                              }

                return jsonify(result), 200

        return jsonify({"ok": True}), 200

    def get_items_telegramm(self, params, trinfo=None):
        #Возвращает список категорий доступных из телеграмм.
        cur = self.connect.cursor()
        sql = """
        select i.id_item , i.title_item, i.is_cost, a.id_acc, u.id_user from Users u 
        inner join Accounts a on a.id_user_owner = u.id_user 
        inner join Items i on i.id_acc = a.id_acc and i.for_telegramm = '1'
        where u.telegram_chat_id = {0}""".format(params['chat']['id'])
        cur.execute(sql)
        items = []
        for row in cur.fetchall():

            data = "{0}::{1}::{2}::{3}::{4}::{5}".format(
                trinfo[0], '0', row[0], row[2], row[3], row[4]
            )
            items.append([{'text': row[1], 'callback_data': data}])
        return items

    def add_transaction(self, data, message):
        data = data.split('::')
        mess = re.fullmatch(r"^Добавить транзакцию \?\n(\d+[.,]?\d*)[\s]+(.*)$", message)
        amount = float(data[0].replace(',','.')) * 100
        amount = 0 - int(amount) if data[3] == '1' else int(amount)

        comment = mess.groups()

        id_acc = int(data[4])
        id_item = int(data[2])
        id_user = int(data[5])

        sql = """
        INSERT INTO Transactions (id_acc,id_item,id_user,date_plan,date_fact,ammount_trans,comment_trans) VALUES
        ({0}, {1}, {2}, current_date(), NULL, {3}, '{4}')
        """.format(id_acc, id_item, id_user, amount, comment[1])
        try:
            cur = self.connect.cursor()
            cur.execute(sql)
            self.connect.commit()
            return "Сохранено! {0} - {1}".format(amount/100, comment[1])
        except:
            return "Ошибка базы данных. Обратитесь к администратору. "
        
    def cmd_start(self, params):
        code = ''.join(re.findall(r'\d', params['text']))
        first = None
        if code:
            cur = self.connect.cursor()
            cur.execute("select id_user, name_user from Users where telegram_add_code={0}".format(code))
            first = cur.fetchone()
            
            if first:
                cur.execute("update Users set telegram_chat_id={0} where telegram_add_code={1}".format(
                    params['chat']['id'],
                    code,
                ))
                self.connect.commit()
                return {"text": "Добро пожаловать ув. {0}.".format(first[1])}

        
        return {"parse_mode":"Markdown", "text": """
        *Добро пожаловать!* 
        
        Этот бот является частью системы ведения домашней бухгалтерии "Kojima". 
        Для того чтобы начать пользоваться ботом, необходимо привязать ваш аккаунт. Для этого требуется авторизоваться на сайте [Kojima.su](https://kojima.su/),
        после чего зайти в раздел настройки пользовательских данных и пройти по ссылке активации бота.
        """}

    def cmd_reset(self, params):
        if params['from']['id'] == 341694478:
            with open('/var/www/u1061027/data/www/kojima.su/tmp/restart.txt', 'a') as the_file:
                the_file.write('restart {0}\n'.format(params['date']))
                
            return {"text": "Сервер flask перезагружен."}
            
        return {"text": "У вас нет прав на совершение данной операции."}

    def cmd_status(self, params):
        sql = """
        select
        case 
            when (date(t.date_plan) < CURRENT_DATE()) then 'Просрочено'
            when (date(t.date_plan) = CURRENT_DATE()) then 'Сегодня'
            when (date(t.date_plan) = CURRENT_DATE() + INTERVAL 1 day) then 'Завтра'
            else '7 дней'
        end, 
        t.date_plan,
        t.ammount_trans/100,
        t.comment_trans,
        i.title_item, 
        a.title_acc 
        from Users u 
        inner join Transactions t 
            on t.id_user =u.id_user 
            and t.date_fact is null 
            and (t.date_plan < CURRENT_DATE()
            or (t.date_plan between CURRENT_DATE() and CURRENT_DATE() + INTERVAL 7 day))
        inner join Items i on i.id_item = t.id_item 
        inner join Accounts a on a.id_acc = t.id_acc 
        where u.telegram_chat_id = {0}
        order by t.date_plan         
        """.format(params['chat']['id'])
        cur = self.connect.cursor()
        cur.execute(sql)
        text = "*Список ближайших платежей:* \n"
        transact_list = []
        for row in cur.fetchall():
            transact_list.append("""
{0} *{1}*
`{2}`
_Цена:{3} ({4} - {5})_
            """.format(
                row[1].strftime("%Y-%m-%d"), row[0],
                row[3],
                round(float(row[2]), 2), row[5], row[4]
            ))

        text += "\n".join(transact_list)

        return {"parse_mode":"Markdown", "text": text}

    def cmd_help(self, params):
        return {"parse_mode":"Markdown", 
        "text": """
    *Напоминания*
Для того чтобы получить список предстоящих дел и платежей воспользуйтесь командой /status

_Данная команда вернет список всех транзакций у которых просрочена плановая дата, либо транзакции которые состоятся в ближайшие дни._
        
    *Регистрация транзакций из телеграмма*
Для того чтобы быстро добавить транзакцию необходимо ввести команду вида:
`<стоимость> <Краткое описание>`
Например:
    45.5 Кефир
    15 Пол батона
    ...

_После ввода подобной комбинации, вам будет предложено выбрать категорию в которую требуется добавить транзакцию._
Список категорий определяется зарание, из интерфейса на сайте [kojima.su](https://kojima.su).  

    *О программе*
Программа \"Kojima\" создана для ведения домашней бухгалтерии.         
Идея проекта заключается в воспитании дисциплины, касательно финансовых дел и хозяйственной
деятельности, для реализации долгосрочных проектов и целей.
    [Сайт kojima.su](https://kojima.su) 
    **   
        """}

    def cmd_webhookinfo(self, params):
        with urlopen("https://api.telegram.org/bot{0}/getWebhookInfo".format(self.key_api)) as conn:            
            return {"text": "{0}".format(conn.read()), "ok":True}
        return {"text": "не удалось прочесть ответ"}