# -*- coding: utf-8 -*-


from json import loads

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..Auth import isauth


class Account(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.groups = {}

    def get_sum_month(self, id_user):
        sql = u"""
        SELECT 
        a.id_acc,
        sum(t.ammount_trans),
        sum(case when (t.ammount_trans>0) then  t.ammount_trans else 0 end)
        from Transactions t 
            inner join Accounts a on t.id_acc = a.id_acc
            inner join Items i on i.id_item = t.id_item 
        where 
            a.id_user_owner = {0} 
            and t.date_fact is not null 
            and i.is_vertual_item != '1'
            and EXTRACT(year from t.date_fact) = EXTRACT(year from current_date())
            and EXTRACT(month from t.date_fact) = EXTRACT(month from current_date())
        group by a.id_acc
        """.format(id_user)
        cur = self.connect.cursor()
        cur.execute(sql)
        result = {}
        for row in cur.fetchall():
            if row[0] not in result:
                result[row[0]] = {'sum': row[1], 'plus': row[2], 'minus': row[1]-row[2]}

        return result

    def recalculate_sum_month(self):
        cur = self.connect.cursor()

        cur.execute(u"""
        SELECT t.id_acc, sum(t.ammount_trans) 
        from Transactions t 
        inner join Items i on i.id_item = t.id_item and i.is_vertual_item != '1'
        inner join Accounts a on a.id_acc = t.id_acc and a.id_user_owner = {0}
            where t.date_fact < DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01') 
            and (EXTRACT(month from a.date_last_sum) != EXTRACT(month from current_date()) or a.date_last_sum is NULL)
            group by t.id_acc
        """.format(session['client_sess']['id_user']))
        curup = self.connect.cursor()
        for row in cur.fetchall():
            curup.execute(u"update Accounts set date_last_sum = current_date(), sum_month_acc={0} where id_acc={1}".format(
                row[1], row[0]
            ))
        self.connect.commit()
        pass

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
                    acc.sum_month_acc,
                    acc.date_last_sum                    
               FROM 
                Accounts as acc
                left join Users as us 
                on us.id_user = acc.id_user_owner
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
        sum_month = self.get_sum_month(session['client_sess']['id_user'])

        for i in cur.fetchall():
            ch = self.create_account_list(i[0])
            w2ui = {}

            if len(ch) > 0:
                w2ui.update({'children': ch})

            income = round(float(sum_month[i[0]]['plus'])/100.0, 2) if i[0] in sum_month else 0
            cost = round(float(sum_month[i[0]]['minus'])/100.0, 2) if i[0] in sum_month else 0
            inp = round(float(i[7]) / 100.0, 2)
            out = round(inp + (income + cost), 2)

            outicon = ''
            if out > inp:
                outicon += '{0} <i class="fa fa fa-chevron-up" style="color:green;"></i>'.format(out)
            elif out < inp:
                outicon += '{0} <i class="fa fa-chevron-down" style="color:red;"></i>'.format(out)
            else:
                outicon += str(out)

            records.append({
                'recid': i[0],
                'id_par_acc': i[1],
                'addate_acc': i[2],
                'title_acc': u"{0} {1}".format(
                    i[3],
                    '<i class="fa fa-wifi iconaccount" aria-hidden="true"></i>' if i[6] == "1" else ''),
                'id_user_owner': i[4],
                'name_user_owner': i[5],
                'is_public': i[6],
                'w2ui': w2ui,
                'title_acc_clear': i[3],
                'income': income,
                'cost': cost,
                'in': inp,
                'out': outicon
            })

        return records

    @isauth
    def api_get_account_list(self):
        self.recalculate_sum_month()
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
