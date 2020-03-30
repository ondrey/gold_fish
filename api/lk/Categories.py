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
                    ic.class_icon
                from Items as i inner join Icons ic 
                    on ic.id_icon = i.id_icon
                where i.id_acc = {0}        
            """.format(
                req['id_acc']
            ))
            for rec in cur.fetchall():
                rec_list.append(rec)

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



        pass

    @isauth
    def api_add_record(self):
        pass

    @isauth
    def api_edit_record(self):
        pass

    @isauth
    def api_del_record(self):
        pass