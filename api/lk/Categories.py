# -*- coding: utf-8 -*-


from json import loads

from flask import jsonify
from flask import request
from flask import session
import datetime

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..Auth import isauth


class Categories(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    def get_items(self, id_acc):
        rec_list = []
        cur = self.connect.cursor()
        cur.execute(u"""
            select 
                i.id_item,
                i.is_vertual_item,
                i.title_item,
                i.discript_item,
                i.is_cost,
                u.name_user,
                i.default_price_item / 100.0,
                i.is_for_sub
            from Items as i 
            inner join Users u on u.id_user = i.id_user
            inner join Accounts a on a.id_acc = i.id_acc
            where i.id_acc = {0} 
        """.format(id_acc))

        for rec in cur.fetchall():
            rec_list.append({
                'text': rec[2],
                'id': rec[0],
                'is_vertual_item': rec[1],
                'is_cost': rec[4],
                'default_price': float(rec[6]) if rec[6] else None
            })

        cur.execute(u"""
            select 
                i.id_item,
                i.is_vertual_item,
                i.title_item,
                i.discript_item,
                i.is_cost,
                u.name_user,
                i.default_price_item / 100.0,
                i.is_for_sub
            from Accounts a
            inner join Items i on i.id_acc_root = a.id_acc_root and i.is_for_sub = '1'
            inner join Users u on u.id_user = i.id_user
            where a.id_acc = {0}
        """.format(id_acc))

        for rec in cur.fetchall():
            rec_list.append({
                'text': rec[2],
                'id': rec[0],
                'is_vertual_item': rec[1],
                'is_cost': rec[4],
                'default_price': float(rec[6]) if rec[6] else None
            })


        return rec_list

    @isauth
    def api_get_list_transaction(self):
        req = loads(request.values['request'])
        rec_list = []

        if 'id_acc' in req:
            rec_list = self.get_items(req['id_acc'])

        return jsonify({
            "status": "success",
            "items": rec_list
        })

    @isauth
    def api_get_list_for_acc(self):
        req = loads(request.form['request'])
        rec_list = []
        cur_date = datetime.datetime.now().replace(day=1)

        if 'id_acc' in req:
            cur = self.connect.cursor()
            sql = u"""
                select 
                    i.id_item,
                    i.is_vertual_item,
                    i.title_item,
                    i.discript_item,
                    i.is_cost,
                    u.name_user,
                    /**/
                    i.budget_month_item / 100.0,
                    i.default_price_item / 100.0,
                    i.unit_price_item, 
                    sum(ts.ammount_trans ) / 100.0,
                    i.is_for_sub
                from Items as i 
                inner join Users u on u.id_user = i.id_user
                left join Transactions ts on ts.id_item = i.id_item and ts.date_fact >= '{1}'
                where i.id_acc = {0}
                group by i.id_item, i.is_vertual_item, i.title_item, i.discript_item, i.is_cost, 
                u.name_user, i.budget_month_item, i.default_price_item, i.unit_price_item, i.is_for_sub      
            """.format(
                req['id_acc'],
                cur_date.strftime("%Y-%m-%d")
            )
            cur.execute(sql)
            for rec in cur.fetchall():
                rec_list.append({
                    'title_cat': rec[2],
                    'recid': rec[0],
                    'is_vertual_item': rec[1],
                    'discript_item': rec[3],
                    'is_cost': rec[4],
                    'name_user': rec[5],
                    'bujet_cat_in_month': float(rec[6]) if rec[6] else 0,
                    'default_price': float(rec[7]) if rec[7] else 0,
                    'unit_cat': rec[8],
                    'amount_cat': float(rec[9]) if rec[9] else 0,
                    'is_for_sub': rec[10]
                })

        return jsonify({
            'total': len(rec_list),
            'records': rec_list,
            'req': req
        })

    @isauth
    def api_add_record(self):
        errors = []
        cur = self.connect.cursor()
        req = loads(request.form['request'])



        if not 'id_item' in req['record']:
            cur.execute(u"select id_acc_root from Accounts where id_acc={0}".format(req['selection'][0]))
            row = cur.fetchone()

            sql = u"""
            INSERT INTO Items (title_item, is_vertual_item, id_acc, discript_item, id_user, is_cost, 
            budget_month_item, default_price_item, unit_price_item, is_for_sub, id_acc_root) 
            VALUES ('{0}', '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})        
            """.format(
                req['record']['title_item'],
                req['record']['is_vertual_item'],
                req['selection'][0],
                u"'{0}'".format(req['record']['discript_item']) if req['record']['discript_item'] else u'NULL',
                session['client_sess']['id_user'],
                req['record']['is_cost'],
                req['record']['bujet_cat_in_month']*100 if req['record']['bujet_cat_in_month'] else u'NULL',
                req['record']['default_price']*100 if req['record']['default_price'] else u'NULL',
                u"'{0}'".format(req['record']['unit_cat']) if req['record']['unit_cat'] else u'NULL',
                req['record']['is_for_sub'],
                row[0]
            )
        else:
            sql = u"""
            UPDATE Items SET 
                title_item='{0}',
                is_vertual_item='{1}',
                discript_item={2},
                is_cost='{3}',
                budget_month_item={6}, 
                default_price_item={7}, 
                unit_price_item={8},
                is_for_sub={9}
            WHERE 
                id_item={4} and id_user={5}
            """.format(
                req['record']['title_item'],
                req['record']['is_vertual_item'],
                u"'{0}'".format(req['record']['discript_item']) if req['record']['discript_item'] else u'NULL',
                req['record']['is_cost'],
                req['record']['id_item'],
                session['client_sess']['id_user'],
                req['record']['bujet_cat_in_month']*100 if req['record']['bujet_cat_in_month'] else u'NULL',
                req['record']['default_price']*100 if req['record']['default_price'] else u'NULL',
                u"'{0}'".format(req['record']['unit_cat']) if req['record']['unit_cat'] else u'NULL',
                req['record']['is_for_sub']
            )

        cur.execute(sql)
        self.connect.commit()

        return jsonify({
            'status': 'success' if len(errors) == 0 else 'error',
            'error': errors
        })

    @isauth
    def api_del_record(self):
        cur = self.connect.cursor()
        errors = []
        req = loads(request.form['request'])

        cur.execute(u"delete from Items where id_item = {0} and id_user={1}".format(
            req['selected'][0], session['client_sess']['id_user']
        ))

        self.connect.commit()

        return jsonify({
            'status': 'success' if len(errors) == 0 else 'error',
            'error': errors
        })
