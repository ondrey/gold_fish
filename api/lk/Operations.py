# -*- coding: utf-8 -*-

from json import loads
import datetime
import calendar

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..ObjectW2UI import search2where
from ..Auth import isauth


class Operations(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.user_id = None
        if 'client_sess' in session:
            self.user_id = session['client_sess']['id_user']

    @isauth
    def api_del_record(self):
        cur = self.connect.cursor()
        errors = []
        req = loads(request.form['request'])

        for id in req['selected']:
            cur.execute(u"delete from Operations where id_op={0} and id_owner_op={1}".format(id, self.user_id))

        self.connect.commit()

        return jsonify({
            'status': 'success',
            'message': u'Запись удалена'
        })

    def add_operation(self, amount_op, comment_op, type_op):
        """
        Регистрация операции
        :return:
        """
        cur = self.connect.cursor()
        cur.execute(u"insert into Operations (id_owner_op, amount_op, comment_op, type_op) "
                    u"values ({0}, {1}, '{2}', '{3}')".format(
            self.user_id,
            amount_op,
            comment_op,
            type_op
        ))
        self.connect.commit()
        cur.execute(u"SELECT LAST_INSERT_ID()")
        id_rec = cur.fetchone()[0]
        cur.execute(u"select count(*) from Operations where type_op='{0}' and id_owner_op={1}".format(
            type_op, self.user_id
        ))
        countOperations = cur.fetchone()[0]

        amount_type = 'E'
        amount_code = int(amount_op)
        if int(amount_op) / 1000 > 0:
            amount_type = 'K'
            amount_code = int(amount_op) / 1000
        if int(amount_op) / 1000000 > 0:
            amount_type = 'M'
            amount_code = int(amount_op) / 1000000

        code = u"{0}{1}{2}{3}".format(
            type_op,
            str(countOperations + 1).rjust(6, '0'),
            amount_type,
            str(amount_code).rjust(3, '0')
        )

        cur.execute(u"update Operations set code_op = '{0}' where id_op = {1}".format(
            code, id_rec
        ))
        self.connect.commit()

        return code, id_rec

    @isauth
    def api_add_operation(self):
        req = loads(request.form['request'])
        result = {}

        code, idrec = self.add_operation(req['record']['amount_op'], req['record']['comment_op'],
                                         req['record']['type_op'])

        return jsonify({'code': code, 'idrec': idrec, 'status': 'success'})

    @isauth
    def api_add_cicle_op(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        if 'id_exists' not in req:
            code, idrec = self.add_operation(req['record']['price_op'], req['record']['comment_transact'],
                                             req['record']['type_op'])
        else:
            idrec = req['id_exists']

        start = datetime.datetime.strptime(req['record']['date_start'], "%Y-%m-%d")
        stop = datetime.datetime.strptime(req['record']['date_finish'], "%Y-%m-%d")
        current = start
        current_week_day = start.isoweekday()
        transact_days = []
        while current < stop:
            if req['record']['unit']['id'] == 'day':
                count_day = (stop - start).days
                if count_day > 0:
                    price = req['record']['price_op']*100
                    if req['record']['price_for_unit'] == 1:
                        # Разделить стоимость по колву отрезков
                        price = req['record']['price_op']/count_day*100

                    cur.execute(u"""insert into Transactions
                        (id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans, id_op)
                        values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7})
                        """.format(req['acc'], req['record']['id_item']['id'], self.user_id, current, 'NULL',
                        0 - price if req['record']['id_item']['is_cost'] == '1' else price,
                        req['record']['comment_transact'], idrec))
                else:
                    return jsonify({'status': 'error', 'message': u"Указанный период меньше суток."})

            elif req['record']['unit']['id'] == 'week' and current.isoweekday() == current_week_day:
                count_day = (stop - start).days / 7
                if count_day > 0:
                    price = req['record']['price_op'] * 100
                    if req['record']['price_for_unit'] == 1:
                        # Разделить стоимость по колву отрезков
                        price = req['record']['price_op'] / count_day * 100

                    cur.execute(u"""insert into Transactions
                        (id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans, id_op)
                        values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7})
                        """.format(req['acc'], req['record']['id_item']['id'], self.user_id, current, 'NULL',
                                   0 - price if req['record']['id_item']['is_cost'] == '1' else price,
                                   req['record']['comment_transact'], idrec))
                else:
                    return jsonify({'status': 'error', 'message': u"Указанный период меньше 7 дней."})

            elif req['record']['unit']['id'] == 'month':
                date_transact = None
                if current.day == start.day and start.day != calendar.monthrange(start.year,start.month)[1]:
                    # Если текущий день равен стартовому дню и стартовый день не является последним в своем месяце
                    date_transact = datetime.date(current.year, current.month, current.day)

                elif start.day == calendar.monthrange(start.year,start.month)[1] \
                        and current.day == calendar.monthrange(current.year, current.month)[1]:
                    # если стартовый день это последний день месяца и текущий день равен последнему дню месяца
                    date_transact = datetime.date(
                        current.year, current.month, calendar.monthrange(current.year, current.month)[1]
                    )

                if date_transact:
                    transact_days.append(date_transact)

            current = current + datetime.timedelta(days=1)

        for date in transact_days:
            # Сохраним транзакции по месяцам если они есть

            price = req['record']['price_op'] * 100
            if req['record']['price_for_unit'] == 1:
                # Разделить стоимость по колву отрезков
                price = req['record']['price_op'] / len(transact_days) * 100

            cur.execute(u"""insert into Transactions
                (id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans, id_op)
                values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7})
                """.format(req['acc'], req['record']['id_item']['id'], self.user_id, date, 'NULL',
                           0 - price if req['record']['id_item']['is_cost'] == '1' else price,
                           req['record']['comment_transact'], idrec))

        self.connect.commit()

        return jsonify({'status': 'success'})

    @isauth
    def api_add_transfer_op(self):
        req = loads(request.form['request'])
        result = {}

        comment = req['record']['comment_transact']

        code, idrec = self.add_operation(
            req['record']['amount_op'],
            u"Перевод средств {0} в {1}".format(req['record']['acc_from'], req['record']['acc_to']),
            req['record']['type_op']
        )

        curDate = datetime.datetime.now()
        dateOp = datetime.datetime.strptime(req['record']['date_op'], '%Y-%m-%d')
        fact_date = u"'{0}'".format(req['record']['date_op'])
        if dateOp > curDate:
            fact_date = u"NULL"

        price = req['record']['amount_op'] * 100

        cur = self.connect.cursor()
        cur.execute(u"""insert into Transactions
                (id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans, id_op)
                values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7})
                """.format(req[u'acc_from'], -1, self.user_id, req['record']['date_op'], fact_date, 0 - price, comment,
                           idrec))

        cur.execute(u"""insert into Transactions
                (id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans, id_op)
                values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7})
                """.format(req[u'acc_to'], -2, self.user_id, req['record']['date_op'], fact_date, price, comment,
                           idrec))

        self.connect.commit()

        return jsonify({'status': 'success'})

    @isauth
    def api_get_records(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        sql = u"""
        select SQL_CALC_FOUND_ROWS * from
        (select
            op.id_op as id,
            op.addate_op as addate_op,
            op.id_owner_op as id_owner_op,
            op.amount_op as amount_op,
            op.code_op as code_op,
            op.comment_op as comment_op,
            op.type_op as type_op,
            ot.title_typeop as title_typeop,
            sum(CASE when tr.date_fact then tr.ammount_trans else 0 END) as fact_sum_op,
            coalesce(sum(tr.ammount_trans), 0) as plan_sum_op,
            min(tr.date_plan) as min_date_plan,
            max(tr.date_plan) as max_date_plan,
            count(tr.date_plan) as count_plan,
            count(tr.date_fact) as count_fact,
            ot.icon_class_op as icon
        from
            Operations op
        join OpType ot on
            ot.alias_typeop = op.type_op
        left join Transactions tr on
            tr.id_op = op.id_op
        where
            op.id_owner_op = {0}
        group by
            op.id_op,
            op.addate_op,
            op.id_owner_op,
            op.amount_op,
            op.code_op,
            op.comment_op,
            op.type_op,
            ot.title_typeop,
            ot.icon_class_op
        order by
            (count(tr.date_plan) - count(tr.date_fact)) DESC,
            op.addate_op DESC
        ) as oper
        where {3}
        LIMIT {1} OFFSET {2}
        """.format(self.user_id, req['limit'], req['offset'],
                   search2where(req['search'], replase_field={
                       u'code_op': u'oper.code_op',
                       u'comment_op': u'oper.comment_op'
                   }, logic=req['searchLogic']) if 'search' in req else u'1=1'
                   )

        cur.execute(sql)
        records = []
        for row in cur.fetchall():
            records.append({
                'recid': row[0]
                , 'addate_op': row[1].strftime("%d.%m.%Y %H:%M")
                , 'id_owner_op': row[2]
                , 'amount_op': row[3]
                , 'code_op': row[4]
                , 'comment_op': row[5]
                , 'type_op': row[6]
                , 'title_typeop': row[7]
                , 'amount_fact_op': int(row[8])
                , 'amount_plan_op': int(row[9])
                , 'dstart_op': row[10].strftime("%d.%m.%Y") if row[10] else None
                , 'dfinish_op': row[11].strftime("%d.%m.%Y") if row[11] else None
                , 'count_plan': row[12]
                , 'count_fact': row[13]
                , 'icon_class_op': row[14]
            })

        cur.execute(u"SELECT FOUND_ROWS()")
        total = cur.fetchone()

        return jsonify({
            'total': total,
            'records': records
        })
