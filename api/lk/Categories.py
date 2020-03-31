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
                    ic.class_icon,
                    i.discript_item
                from Items as i left join Icons ic 
                    on ic.id_icon = i.id_icon
                where i.id_acc = {0}        
            """.format(
                req['id_acc']
            ))
            for rec in cur.fetchall():
                rec_list.append({
                    'title_cat': u"<i class='fa {1} iconaccount'></i> {0}".format(rec[2], rec[3]),
                    'recid': rec[0],
                    'is_vertual_item': rec[1],
                    'discript_item': rec[4]
                })

        return jsonify({
            'total': len(rec_list),
            'records': rec_list,
            'req': req
        })

    @isauth
    def api_get_icon_list(self):
        rec_list = []

        cur = self.connect.cursor()
        cur.execute(u'select id_icon, class_icon from Icons')
        for rec in cur.fetchall():
            rec_list.append({'id': rec[0], 'text': rec[1], 'icon': 'fa '+rec[1], 'img': rec[1]})

        return jsonify({
            'items': rec_list,
            'status': 'success',
        })

    @isauth
    def api_add_record(self):
        cur = self.connect.cursor()
        req = loads(request.form['request'])
        sql = u"""
        INSERT INTO Items (title_item, is_vertual_item, id_acc, id_icon, discript_item, id_user) 
        VALUES ('{0}', '{1}', {2}, {3}, {4}, {5})        
        """.format(
            req['record']['title_item'],
            req['record']['is_vertual_item'],
            req['selection'][0],
            req['record']['id_icon'][u'id'],
            u"'{0}'".format(req['record']['discript_item']) if req['record']['discript_item'] else u'NULL',
            session['client_sess']['id_user']
        )
        cur.execute(sql)
        self.connect.commit()
        return jsonify({
            'status': 'success',
        })

    @isauth
    def api_edit_record(self):
        pass

    @isauth
    def api_del_record(self):
        pass