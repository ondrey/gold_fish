"""
Отчет для графика по категориям - ежедневная проверка зарегистрированных транзакций по категории.
"""
from config import DevelopmentTemplateConfig as config
import pymysql

if __name__ == '__main__':
    connect = pymysql.connect(**config.DB_CONNECT)
    cur = connect.cursor()
    cur.execute("""
    Select date(t.date_fact), t.id_acc, t.id_item, sum(t.ammount_trans) from `Transactions` t 		
    where t.date_fact is not null and t.id_acc is not null
    and (t.date_fact > 
        (
            select max(tr.date_report) from `TransactionReport` tr where tr.id_acc = t.id_acc and tr.id_item = t.id_item) 
        or (
            select max(tr.date_report) 
            from `TransactionReport` tr where tr.id_acc = t.id_acc and tr.id_item = t.id_item) is Null
        )
    group by date(t.date_fact), t.id_acc, t.id_item
    """)
    for row in cur.fetchall():
        sql_inser = "insert into `TransactionReport` (date_report, id_acc, id_item, sum_report) values (%s, %s, %s, %s)"
        cur.execute(sql_inser, row)
        print(row)
    connect.commit()