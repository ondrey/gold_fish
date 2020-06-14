

from json import loads
import datetime

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..ObjectW2UI import search2where
from ..Auth import isauth


class Transaction(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    @isauth
    def api_edit_transaction(self):
        req = loads(request.form['request'])
        id_tran = req['id_tran']
        cur = self.connect.cursor()

        cur.execute(u"select date_fact, id_user from Transactions where id_trans={0}".format(id_tran))
        count_rec = cur.fetchone()
        sql = None
        if len(count_rec) != 0:
            if count_rec[0]:
                result = {'status': 'error', 'message': u"Ошибка. Транзакция уже завершена."}
            elif count_rec[1] != session['client_sess']['id_user']:
                result = {'status': 'error', 'message': u"Ошибка. Транзакция не пренадлежит Вам."}
            else:

                sql = u"update Transactions set {0} comment_trans = '{1}', ammount_trans={3}*100, date_plan='{4}', " \
                      u"id_item={5} " \
                      u"where id_trans={2}".format(

                        u"date_fact = '"+req['record']['date_fact']+u"', " if req['record']['date_fact'] else u'',
                        req['record']['comments'],
                        id_tran,
                        req['record']['ammount_trans'],
                        req['record']['date_plan'],
                        req['record']['id_item']['id']

                )
                result = {'status': 'success'}
        else:
            result = {'status': 'error', 'message': u"Ошибка. Записи не существует."}

        if sql:
            cur.execute(sql)
            self.connect.commit()

        return jsonify(result)

    @isauth
    def api_add_transaction(self):
        req = loads(request.form['request'])
        id_acc = req['id_acc']
        result = {}

        sqlCheckPerm = u"""
            select count(*) from Accounts a 
            where a.id_acc = {0} and (a.id_user_owner = {1} or a.is_public = '1') 
        """.format(id_acc, session['client_sess']['id_user'])

        cur = self.connect.cursor()
        cur.execute(sqlCheckPerm)
        for row in cur.fetchall():
            if row[0] == 0:
                result = {
                    'status': 'error',
                    'message': u'Счет не существует, или он НЕ является публичным.'
                }
            else:

                if not req['record']['date_fact']:
                    date_plan = req['record']['date_plan']
                    date_fact = u"NULL"
                else:
                    date_plan = req['record']['date_fact']
                    date_fact = u"'{0}'".format(req['record']['date_fact'])

                price = req['record']['ammount_trans'] * 100
                if req['record']['id_item']['is_cost'] == '1':
                    price = 0 - price

                if req['record']['counts']:
                    price = price * int(req['record']['counts'])

                comment_split = req['record']['comments'].split('\n')
                check_list = []
                for check in comment_split:
                    check = check.split('=')
                    if len(check) == 2:
                        try:
                            p = int(float(check[1].replace(',', '.')) * 100)
                            if req['record']['id_item']['is_cost'] == '1':
                                p = 0 - p
                            check_list.append({'text': check[0], 'price': p})
                        except:
                            pass

                if len(check_list) == 0:
                    sqlInsertTransaction = u"""
                    insert into Transactions(id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans
                        , id_op, count_trans) values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7}, {8})
                    """.format(id_acc, req['record']['id_item']['id'], session['client_sess']['id_user'], date_plan,
                               date_fact, price, req['record']['comments'], req['id_op'] if 'id_op' in req else 'NULL',
                               req['record']['counts'] if req['record']['counts'] else 1
                    )
                    cur.execute(sqlInsertTransaction)
                else:
                    for ch in check_list:
                        sqlInsertTransaction = u"""
                        insert into Transactions(id_acc, id_item, id_user, date_plan, date_fact, ammount_trans, comment_trans
                            , id_op, count_trans) values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}', {7}, {8})
                        """.format(id_acc, req['record']['id_item']['id'], session['client_sess']['id_user'], date_plan,
                                   date_fact, ch['price'], ch['text'],
                                   req['id_op'] if 'id_op' in req else 'NULL',
                                   req['record']['counts'] if req['record']['counts'] else 1
                                   )
                        cur.execute(sqlInsertTransaction)

                result = {'status': 'success'}
                self.connect.commit()

        return jsonify(result)

    @isauth
    def api_del_record(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        result = {}
        if 'selected' in req:
            for recid in req['selected']:
                select = u"select acc.id_user_owner, tr.date_fact, it.is_vertual_item " \
                         u"from Transactions tr " \
                         u"inner join Accounts acc on acc.id_acc = tr.id_acc " \
                         u"inner join Items AS it ON it.id_item = tr.id_item " \
                         u"where tr.id_trans={0}".format(recid)

                cur.execute(select)
                trans = cur.fetchone()
                if trans[0] != session['client_sess']['id_user']:
                    result = {'status': 'error', 'message': u'Ошибка. Вы не можете удалять транзакции в чужих счетах, '
                                                            u'обратитесь к владельцу счета.'}
                else:
                    cur.execute(u"delete from Transactions where id_trans = {0}".format(recid))
                    result = {'status': 'success'}

        self.connect.commit()

        return jsonify(result)

    @isauth
    def api_get_records(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        rec_list = []
        id_acc = u""
        hot_filter = u""
        if 'id_acc' in req:
            id_acc = u"ts.id_acc = {0} AND ".format(req['id_acc'])
        if 'id_op' in req:
            id_acc = u"ts.id_op = {0} AND ".format(req['id_op'])

        if 'is_hot_filter' in req and req['is_hot_filter']:
            hot_filter = u"((ts.date_fact is null and ts.date_plan <= CURRENT_DATE()) or " \
                         u"ts.date_plan between current_date() and CURRENT_DATE() + INTERVAL 7 day) AND "

        sql = u"""
            SELECT 
                SQL_CALC_FOUND_ROWS
                 
                it.title_item, it.is_vertual_item, it.is_cost,
                ts.addate_trans,
                ts.date_plan,
                ts.date_fact,
                ts.ammount_trans,
                ts.comment_trans,
                us.name_user,
                ts.id_trans,
                ac.title_acc,
                op.code_op,
                ts.count_trans,
                it.id_item
            FROM Transactions AS ts
            INNER JOIN Accounts AS ac ON ts.id_acc = ac.id_acc
            INNER JOIN Items AS it ON it.id_item = ts.id_item
            INNER JOIN Users AS us ON us.id_user = ts.id_user
            LEFT JOIN Operations AS op on op.id_op = ts.id_op

            WHERE {0} {5} ac.id_user_owner = {1} and {4}
            ORDER BY ts.date_fact, ts.date_plan DESC
            LIMIT {2} OFFSET {3}        
        """.format(
            id_acc,
            session['client_sess']['id_user'],
            req['limit'],
            req['offset'],
            search2where(req['search'], replase_field={
                u'ammount_trans': u'ts.ammount_trans/100',
                u'date_plan': u'ts.date_plan',
                u'date_fact': u'ts.date_fact',
                u'id_item': u'ts.id_item',
                u'comment_trans': u'ts.comment_trans',
                u'addate_trans': u'ts.addate_trans',
                u'title_item': u'it.title_item',
                u'title_acc': u'ac.title_acc',
                u'code_op': u'op.code_op',
                u'counts': u'ts.count_trans'
            }, logic=req['searchLogic']) if 'search' in req else u'1=1',
            hot_filter
        )

        cur.execute(sql)
        for rec in cur.fetchall():
            rec_list.append({
                'title_item': rec[0],
                'is_vertual_item':rec[1],
                'is_cost': rec[2],
                'addate_trans': rec[3].strftime("%Y-%m-%d %H:%M"),
                'date_plan': rec[4].strftime("%Y-%m-%d") if rec[4] else None,
                'date_fact': rec[5].strftime("%Y-%m-%d") if rec[5] else None,
                'ammount_trans': round(float(rec[6])/100.0, 2),
                'comment_trans': rec[7],
                'name_user': rec[8],
                'recid': rec[9],
                'title_acc': rec[10],
                'code_op': rec[11],
                'count_trans': rec[12],
                'id_item': rec[13],
                'title_item_clear': rec[0]
            })

        cur.execute(u"SELECT FOUND_ROWS()")
        total = cur.fetchone()

        return jsonify({
            'total': total,
            'records': rec_list
        })

    @isauth
    def api_paste_in_account(self):
        req = loads(request.form['data'])

        if 'id_trans' in req and 'id_new_acc' in req:
            cur = self.connect.cursor()

            for id in req['id_trans']:
                cur.execute("update Transactions set id_acc = {0} where id_trans = {1} and id_user={2}".format(
                    req['id_new_acc'], id, session['client_sess']['id_user']
                ))
            self.connect.commit()

        return jsonify({
            'total': len(req['id_trans']),
            'ok': True
        })
