# -*- coding: utf-8 -*-

from json import loads

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..Auth import isauth


class Transaction(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    @isauth
    def api_del_record(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        status = 'error'
        if 'selected' in req:
            cur.execute(u"delete from Transactions where id_trans={0} and id_user={1}".format(
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
            sqlCount = u"""
                SELECT 
                    count(*)
                FROM Transactions AS ts
                INNER JOIN Accounts AS ac ON ts.id_acc = ac.id_acc
                WHERE ts.id_acc = {0} AND ac.id_user_owner = {1}
            """.format(req['id_acc'], session['client_sess']['id_user'])
            cur.execute(sqlCount)
            for r in cur.fetchall():
                total = r[0]

            sql = u"""
                SELECT 
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

                WHERE ts.id_acc = {0} AND ac.id_user_owner = {1}
                ORDER BY ts.date_plan DESC, ts.date_fact
                LIMIT {2} OFFSET {3}        
            """.format(
                req['id_acc'],
                session['client_sess']['id_user'],
                req['limit'],
                req['offset']
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
                    'ammount_trans': rec[6],
                    'comment_trans': rec[7],
                    'name_user': rec[8],
                    'recid': rec[9]
                })

        return jsonify({
            'total': total,
            'records': rec_list
        })
