# -*- coding: utf-8 -*-

from hashlib import md5
from random import choice
from uuid import uuid4

from flask import jsonify
from flask import abort
from flask import request
from flask import session
from flask import redirect, url_for
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
                acc.id_type_acc,
                acct.title_type_acc,                
                acc.title_acc,                
                acc.id_user_owner,
                us.name_user,                
                acc.is_public,                								
                COALESCE(i.class_icon, acct.icon_type_acc) as class,                
                acc.color_acc,
                acc.discription_acc
                
                FROM 
                Accounts as acc
                left join Users as us 
                on us.id_user = acc.id_user_owner
                left join Icons as i 
                on i.id_icon = acc.id_icon
                left join AccountTypes as acct 
                on acct.id_type_acc = acc.id_type_acc
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
            w2ui = {'style': 'color:{0}'.format(i[10])}
            if len(ch) > 0:
                w2ui.update({'children': ch})

            records.append(dict(
                recid=i[0],
                parent_=i[1],
                addate_acc=i[2],
                id_type_acc=i[3],
                title_type_acc=i[4],
                title_acc=i[5],
                id_user_owner=i[6],
                name_user_owner=i[7],
                is_public=i[8],
                icon_class=i[9],
                discription_acc=i[11],
                #w2ui=w2ui
            ))

        return records

    @isauth
    def api_get_account_list(self):
        return jsonify(self.create_account_list())
