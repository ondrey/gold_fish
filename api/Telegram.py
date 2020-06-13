from flask import current_app as app
from flask import request
from flask_mail import Mail
from api.ObjectAPI import ObjectAPI
from api.ObjectDb import ObjectDb
from flask import jsonify
import re
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
                    result.update({"text": "Подходит для создания транзакции", "reply_markup":{"inline_keyboard": [ [{"text":"отмена", "callback_data": "31221"}], ]}})
                elif 1!=1:
                    # Тут обработчик callback_data после выбора Счета
                    pass
                elif 1!=1:
                    # Тут обработчик callback_data после выбора Категории
                    pass                    
                else:
                    result.update({"text": "Не понял! Для получения справки введите команду /help"})
                    
                return result, 200

        return jsonify({"ok": True}), 200
        
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

    def cmd_restart_flask(self, params):
        if params['from']['id'] == 341694478:
            with open('/var/www/u1061027/data/www/kojima.su/tmp/restart.txt', 'a') as the_file:
                the_file.write('restart {0}\n'.format(params['date']))
                
            return {"text": "Сервер flask перезагружен."}
            
        return {"text": "У вас нет прав на совершение данной операции."}

    def cmd_report(self, params):
        sql = """
        select
        case 
            when (date(t.date_plan) < CURRENT_DATE()) then 'Просрочено'
            when (date(t.date_plan) = CURRENT_DATE()) then 'Сегодня'
            when (date(t.date_plan) = CURRENT_DATE() + INTERVAL 1 day) then 'Завтра'
            else '7 дней'
        end, 
        t.date_plan 	
        from Users u 
        inner join Transactions t 
            on t.id_user =u.id_user 
            and t.date_fact is null 
            and (t.date_plan < CURRENT_DATE()
            or (t.date_plan between CURRENT_DATE() and CURRENT_DATE() + INTERVAL 7 day))
        where u.telegram_chat_id = 341694478        
        """

        return {"text": "Вы ввели команду {0}".format(str(params))}

    def api_send_notyfy(self):
        pass
        
    def add_transaction(self, params):
        return {"text": "Вы ввели команду {0}".format(str(params))}
        
    def cmd_help(self, params):
        return {"parse_mode":"Markdown", 
        "text": """
*Регистрация транзакции*
    Для того чтобы зарегистировать расход или доход можно ввести следующую формулу:
    `<стоимость транзакции> <Красткое описание>`
    Например:
        `456.20 Купил булку со скидкой`
        `15.50 Бутылка кефира`
        `50 Носочек`
_После чего система предложит выбрать категорию к которой необходимо отнести транзакцию. 
Необходимо заранее указать в настройках категорий, какие из них, будут доступны в телеграмм._        

*Напоминания*
    Для того чтобы получать напоминания о приблежающимся платеже, необходимо активировать уведомления командой:
    /noty
    _Для того чтобы отключить напоминания, введите команду повторно_
        """}        
            
    def cmd_about(self, params):
        return {"parse_mode":"Markdown", 
        "text": """
*О программе*
Программа \"Kojima\" создана для ведения домашней бухгалтерии, по соображениям автора.         
Идея проекта заключается в воспитании дисциплины, касательно финансовых дел и хозяйственной
деятельности, для реализации долгосрочных проектов и целей.        
        """}       

    def cmd_webhookinfo(self, params):
        with urlopen("https://api.telegram.org/bot{0}/getWebhookInfo".format(self.key_api)) as conn:            
            return {"text": "{0}".format(conn.read()), "ok":True}
        return {"text": "не удалось прочесть ответ"}