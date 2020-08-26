"""
Расчет входящего остатка
"""
from config import DevelopmentTemplateConfig as config
import pymysql
import sys
import datetime

if __name__ == '__main__':
    param = sys.argv
    start_date = datetime.datetime.now().date()
    if len(param) == 2:
        start_date = datetime.datetime.strptime(param[1], "%d.%m.%Y").date()

    connect = pymysql.connect(**config.DB_CONNECT)
    cur = connect.cursor()

    while start_date <= datetime.datetime.now().date():
        cur.execute("select sum(t.ammount_trans), t.id_acc from `Transactions` t "
                    "where t.date_fact is not null and t.id_acc is not null and t.date_fact < %s "
                    "group by t.id_acc", (start_date,))

        for row in cur.fetchall():
            cur.execute("insert into `TotalDayReport` (sum_total, id_acc, date_total) values (%s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE date_total=date_total", (*row, start_date))
        connect.commit()

        start_date += datetime.timedelta(days=1)
