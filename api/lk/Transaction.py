# -*- coding: utf-8 -*-

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

                sqlInsertTransaction = u"""
                insert into Transactions(
                    id_acc
                    , id_item
                    , id_user
                    , date_plan
                    , date_fact
                    , ammount_trans
                    , comment_trans) 
                values ({0}, {1}, {2}, '{3}', {4}, {5}, '{6}')
                """.format(
                    id_acc,
                    req['record']['id_item']['id'],
                    session['client_sess']['id_user'],
                    date_plan, date_fact,
                    price,
                    req['record']['comments']
                )
                cur.execute(sqlInsertTransaction)
                result = {'status': 'success'}
                self.connect.commit()

        return jsonify(result)

    @isauth
    def api_del_record(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        status = 'error'
        if 'selected' in req:
            cur.execute(u"delete from Transactions where id_trans={0} and "
                        u"EXISTS (select * from kojima.Accounts a where a.id_user_owner = {1} and a.id_acc = id_acc )".format(
                req['selected'][0],
                session['client_sess']['id_user']
            ))
            self.connect.commit()
            status='success'

        return jsonify({
            'status': status,
            'records': req['selected']
        })

    @isauth
    def api_get_records(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        rec_list = []
        total = 0
        if 'id_acc' in req:

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
                    ts.id_trans
                FROM Transactions AS ts
                INNER JOIN Accounts AS ac ON ts.id_acc = ac.id_acc
                INNER JOIN Items AS it ON it.id_item = ts.id_item
                INNER JOIN Users AS us ON us.id_user = ts.id_user

                WHERE ts.date_plan <= current_date AND ts.id_acc = {0} AND ac.id_user_owner = {1} {4}
                ORDER BY ts.date_plan DESC, ts.date_fact
                LIMIT {2} OFFSET {3}        
            """.format(
                req['id_acc'],
                session['client_sess']['id_user'],
                req['limit'],
                req['offset'],
                search2where(req['search'], replase_field={
                    u'ammount_trans': u'ts.ammount_trans/100',
                    u'date_plan': u'ts.date_plan',
                    u'date_fact': u'ts.date_fact',
                    u'id_item': u'ts.id_item',
                    u'comment_trans': u'ts.comment_trans',
                    u'addate_trans': u'ts.addate_trans'
                }, logic=req['searchLogic']) if 'search' in req else ''
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
                    'recid': rec[9]
                })

            cur.execute(u"SELECT FOUND_ROWS()")
            total = cur.fetchone()

        return jsonify({
            'total': total,
            'records': rec_list
        })
