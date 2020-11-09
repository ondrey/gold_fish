# -*- coding: utf-8 -*-

from json import loads
import datetime

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..Auth import isauth


# class Acc:
#     def __init__(self, sqlres):
#         self.id_acc = sqlres[0],
#         self.id_par_acc = sqlres[1],
#         self.addate_acc = sqlres[2],
#         self.title_acc = sqlres[3],
#         self.id_user_owner = sqlres[4],
#         self.owner_name = sqlres[5],
#         self.is_public = sqlres[6],
#         self.is_all_transact = sqlres[7],
#         self.is_mod_transact = sqlres[8],
#         self.notify_mod = sqlres[9]

class Account(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.groups = {}

    def my_accounts(self, parent_id=None):
        cur = self.connect.cursor()
        cur.execute(
            """
            SELECT 
                ac.id_acc, 
                ac.id_par_acc, 
                ac.addate_acc, 
                ac.title_acc,
                ac.id_user_owner,
                us.name_user AS owner_name
            FROM kojima.Accounts ac 
            INNER JOIN kojima.Users us ON ac.id_user_owner = us.id_user
            WHERE ac.id_user_owner = %(id_user_owner)s AND ac.id_par_acc {0}        
            """.format(
                ' = ' + str(parent_id) if parent_id else ' is NULL'
            ), {'id_user_owner': session['client_sess']['id_user']})

        return cur.fetchall()

    def get_balanse(self, date_start, id_acc):
        cur = self.connect.cursor()
        cur.execute("""
        SELECT 
            SUM(tr.ammount_trans) AS balance,
            SUM(case when (tr.ammount_trans < 0) then tr.ammount_trans ELSE 0 END) AS cost,
            SUM(case when (tr.ammount_trans > 0) then tr.ammount_trans ELSE 0 END) AS income
            from kojima.Transactions tr 
            WHERE tr.id_acc = %s AND date(tr.date_fact) >= %s
        """, (id_acc, date_start))


    def create_account_list(self, id_parent=None):
        records, balance_ch = [], {}

        req = loads(request.form['request'])

        date_start = datetime.datetime.now().date()
        if req['filter'] == 'item2:month':
            date_start = datetime.date(date_start.year, date_start.month, 1)

        for acc in self.my_accounts(id_parent):

            children = self.create_account_list(acc[0])

            records.append({
                'recid': acc[0],
                'id_par_acc': acc[1],
                'addate_acc': acc[2],
                'title_acc': acc[3],
                'id_user_owner': acc[4],
                'name_user_owner': acc[5],
                'w2ui': {'children': children[0]},
                'title_acc_clear': acc[3],
            })

        return records, balance_ch

    @isauth
    def api_get_account_list(self):
        res = self.create_account_list()
        return jsonify({
            'total': len(res[0]),
            'records': res[0]
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

        if req['record']['isRoot'] == 1:
            isRoot = True
        elif len(req['selection']) > 0:
            isRoot = False
        else:
            isRoot = True

        sql = u"INSERT INTO Accounts(id_par_acc, title_acc, id_user_owner, is_public) VALUES (" \
              u" {0}, '{1}', {2}, '{3}')".format(
            req['selection'][0] if not isRoot else u"NULL",
            req['record']['title_acc'],
            session['client_sess']['id_user'],
            req['record']['isPublic']
        )

        cur = self.connect.cursor()
        cur.execute(sql)

        if isRoot:
            cur.execute(u"update Accounts set id_acc_root = id_acc where id_acc = (SELECT LAST_INSERT_ID())")
        else:
            cur.execute(u"select par.id_acc_root, cur.id_acc from Accounts cur "
                        u"inner join Accounts par on par.id_acc = cur.id_par_acc "
                        u"where cur.id_acc = (SELECT LAST_INSERT_ID())")
            row = cur.fetchone()

            cur.execute(u"update Accounts set id_acc_root = {0} where id_acc = {1}".format(
                row[0], row[1]
            ))

        self.connect.commit()

        return jsonify({
            'status': 'success',
            'records': loads(request.form['request'])
        })

    @isauth
    def api_edit_account(self):
        req = loads(request.form['request'])
        cur = self.connect.cursor()
        sql = u"""
        update Accounts set title_acc = '{0}', is_public='{1}' 
        where id_acc={2} and id_user_owner={3}
        """.format(
            req['record']['title_acc'],
            req['record']['isPublic'],
            req['record']['id_acc'],
            session['client_sess']['id_user']
        )
        cur.execute(sql)
        self.connect.commit()

        return jsonify({
            'status': 'success',
            'records': loads(request.form['request'])
        })
