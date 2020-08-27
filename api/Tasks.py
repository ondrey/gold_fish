from flask import current_app as app
from flask import request
from flask_mail import Mail
from api.ObjectAPI import ObjectAPI
from api.ObjectDb import ObjectDb
from flask import jsonify
import re
import json
import datetime
import pathlib
from urllib.request import urlopen


class Tasks(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.key_api = app.config.get('TASKS_KEY')

    def api_total_day_input(self):
        if request.values['key'] == self.key_api:

            start_date = datetime.datetime.now().date()
            if 'date' in request.values:
                start_date = datetime.datetime.strptime(request.values['date'], "%d.%m.%Y").date()

            date_list = []
            while start_date <= datetime.datetime.now().date():
                cur = self.connect.cursor()
                cur.execute("select sum(t.ammount_trans), t.id_acc from `Transactions` t "
                            "where t.date_fact is not null and t.id_acc is not null and t.date_fact < %s "
                            "group by t.id_acc", (start_date,))

                cnt = 0
                for row in cur.fetchall():
                    cur.execute("insert into `TotalDayReport` (sum_total, id_acc, date_total) values (%s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE date_total=date_total", (row[0], row[1], start_date))
                    cnt += 1
                date_list.append({'count_acc': cnt, 'date': start_date.strftime('%Y.%m.%d')})
                start_date += datetime.timedelta(days=1)

            self.connect.commit()

            return jsonify({
                'status': 'success', 'report': date_list
            })

        else:
            return jsonify({
                'status': 'error',
                'records': 'Not valid key!'
            })
