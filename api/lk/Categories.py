# -*- coding: utf-8 -*-


from json import loads

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..Auth import isauth


class Categories(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    @isauth
    def api_get_list_for_acc(self):
        req = loads(request.form['request'])
        rec_list = []

        if 'id_acc' in req:
            cur = self.connect.cursor()
            cur.execute(u"""
                select 
                    i.id_item,
                    i.is_vertual_item,
                    i.title_item,
                    i.discript_item,
                    i.is_cost,
                    u.name_user
                from Items as i 
                inner join Users u on u.id_user = i.id_user
                where i.id_acc = {0}        
            """.format(
                req['id_acc']
            ))
            for rec in cur.fetchall():
                rec_list.append({
                    'title_cat': rec[2],
                    'recid': rec[0],
                    'is_vertual_item': rec[1],
                    'discript_item': rec[3],
                    'is_cost': rec[4],
                    'name_user': rec[5]
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
            sql = u"""
            INSERT INTO Items (title_item, is_vertual_item, id_acc, discript_item, id_user, is_cost) 
            VALUES ('{0}', '{1}', {2}, {3}, {4}, {5})        
            """.format(
                req['record']['title_item'],
                req['record']['is_vertual_item'],
                req['selection'][0],
                u"'{0}'".format(req['record']['discript_item']) if req['record']['discript_item'] else u'NULL',
                session['client_sess']['id_user'],
                req['record']['is_cost']
            )
        else:
            sql = u"""
            UPDATE Items SET 
                title_item='{0}',
                is_vertual_item='{1}',
                discript_item={2},
                is_cost='{3}'
            WHERE 
                id_item={4} and id_user={5}
            """.format(
                req['record']['title_item'],
                req['record']['is_vertual_item'],
                u"'{0}'".format(req['record']['discript_item']) if req['record']['discript_item'] else u'NULL',
                req['record']['is_cost'],
                req['record']['id_item'],
                session['client_sess']['id_user']
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
