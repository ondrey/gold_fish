# -*- coding: utf-8 -*-


from json import loads

from flask import jsonify
from flask import request
from flask import session
from flask import current_app as app
from flask_mail import Mail

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..Auth import isauth


class Account(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.groups = {}

    def create_account_list(self, id_parent=None):
        cur = self.connect.cursor()
        sql = u"""
                select 
                acc.id_acc,
                acc.id_par_acc,
                acc.addate_acc,                          
                acc.title_acc,                
                acc.id_user_owner,
                us.name_user,                
                acc.is_public,                								
                i.class_icon,                
                acc.color_acc,
                acc.discription_acc
                
                FROM 
                Accounts as acc
                left join Users as us 
                on us.id_user = acc.id_user_owner
                left join Icons as i 
                on i.id_icon = acc.id_icon

            WHERE 
            
            (acc.id_user_owner = {0} or {2}) {1}
            """.format(
                session['client_sess']['id_user'],
                u"and acc.id_par_acc = {0}".format(id_parent) if id_parent else u'and acc.id_par_acc is NULL',
                u"(acc.id_user_owner = {0} and acc.is_public='1')".format(
                    session['client_sess']['id_manager_user']
                ) if session['client_sess']['id_manager_user'] else u'1!=1'
            )

        cur.execute(sql)
        records = []
        for i in cur.fetchall():
            ch = self.create_account_list(i[0])
            w2ui = {}

            if len(ch) > 0:
                w2ui.update({'children': ch})

            records.append(dict(
                recid=i[0],
                id_par_acc=i[1],
                addate_acc=i[2],                          
                title_acc=u"{0} {1}".format(
                    i[3],
                    '<i class="fa fa-wifi iconaccount" aria-hidden="true"></i>' if i[6] == "1" else ''),
                id_user_owner=i[4],
                name_user_owner=i[5],
                is_public=i[6],                								
                class_icon=i[7],
                color_acc=i[8],
                discription_acc=i[9],
                w2ui=w2ui
            ))

        return records

    @isauth
    def api_get_account_list(self):
        res = self.create_account_list()
        return jsonify({
            'total': len(res),
            'records': res
        })

    @isauth
    def api_del_account(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        for idrec in req['selected']:
            cur.execute(u"delete from Accounts where id_acc = {0}".format(idrec))

        self.connect.commit()

        return jsonify({
            'status': 'success',
            'records': req['selected']
        })

    @isauth
    def api_add_account(self):

        req = loads(request.form['request'])

        isRoot = False
        if req['record']['isRoot'] == 1:
            isRoot = True
        elif len(req['selection']) > 0:
            isRoot = False
        else:
            isRoot = True

        sql = u"INSERT INTO Accounts(id_par_acc, title_acc, id_user_owner, is_public, discription_acc) VALUES (" \
              u" {0}, '{1}', {2}, '{3}', '{4}')".format(
            req['selection'][0] if not isRoot else u"NULL",
            req['record']['title_acc'],
            session['client_sess']['id_user'],
            req['record']['isPublic'],
            req['record']['discription_acc']
        )

        cur = self.connect.cursor()
        cur.execute(sql)
        self.connect.commit()

        return jsonify({
            'status': 'success',
            'records': loads(request.form['request'])
        })