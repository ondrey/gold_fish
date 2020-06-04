


from json import loads
import datetime

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
                    acc.date_last_sum,
                    /*Баланс на текущий момент*/
                    sum(case when (date(t.date_fact) <= CURRENT_DATE()) then t.ammount_trans else 0 end) as "balance",
                    /*Расходы с начала месяца*/
                    sum(case when (
                                date(t.date_fact) <= CURRENT_DATE() 
                                and date(t.date_fact) >= DATE_SUB(CURRENT_DATE(),INTERVAL DAYOFMONTH(CURRENT_DATE())-1 DAY)
                                and t.ammount_trans < 0
                            ) then t.ammount_trans else 0 end) as "costs_month",
                    /*Расходы за сегодня*/
                    sum(case when (date(t.date_fact) = CURRENT_DATE() and t.ammount_trans < 0) then t.ammount_trans else 0 end) as "costs_day",
                    /*Доходы с начала месяца*/
                    sum(case when (
                                date(t.date_fact) <= CURRENT_DATE() 
                                and date(t.date_fact) >= DATE_SUB(CURRENT_DATE(),INTERVAL DAYOFMONTH(CURRENT_DATE())-1 DAY)
                                and t.ammount_trans > 0
                            ) then t.ammount_trans else 0 end) as "income_month",
                    /*Доходы за сегодня*/
                    sum(case when (date(t.date_fact) = CURRENT_DATE() and t.ammount_trans > 0) then t.ammount_trans else 0 end) as "income_day"      
               FROM 
                Accounts as acc
                left join Transactions t on 
                    t.id_acc = acc.id_acc
                left join Items i 
                    on i.id_item = t.id_item 
                inner join Users as us 
                    on us.id_user = acc.id_user_owner
            WHERE 
            (acc.id_user_owner = {0} or {2}) {1}        
            group by                     
                acc.id_acc,
                acc.id_par_acc,
                acc.addate_acc,                          
                acc.title_acc,                
                acc.id_user_owner,
                us.name_user,                
                acc.is_public,
                acc.sum_month_acc,
                acc.date_last_sum               
            """.format(
                session['client_sess']['id_user'],
                u"and acc.id_par_acc = {0}".format(id_parent) if id_parent else u'and acc.id_par_acc is NULL',
                u"(acc.id_user_owner = {0} and acc.is_public='1')".format(
                    session['client_sess']['id_manager_user']
                ) if session['client_sess']['id_manager_user'] else u'1!=1'
            )

        cur.execute(sql)
        records = []
        balance_ch = dict(balance=0, cost_month=0, cost_day=0, income_month=0, income_day=0)
        for i in cur.fetchall():
            ch, b = self.create_account_list(i[0])
            w2ui = {}

            balance = float(round(i[9] / 100, 2))
            cost_month = float(round(i[10] / 100, 2))
            cost_day = float(round(i[11] / 100, 2))
            income_month = float(round(i[12] / 100, 2))
            income_day = float(round(i[13] / 100, 2))

            if len(ch) > 0:
                w2ui.update({'children': ch})
                # Добавим дочернии суммы если они есть
                balance += b['balance']
                cost_month += b['cost_month']
                cost_day += b['cost_day']
                income_month += b['income_month']
                income_day += b['income_day']

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
                'balance': '{:,}'.format(round(balance, 2)).replace(',', ' '),
                'cost_month': '{:,}'.format(round(cost_month, 2)).replace(',', ' '),
                'cost_day': '{:,}'.format(round(cost_day, 2)).replace(',', ' '),
                'income_month': '{:,}'.format(round(income_month, 2)).replace(',', ' '),
                'income_day': '{:,}'.format(round(income_day, 2)).replace(',', ' ')
            })
            balance_ch['balance'] += balance
            balance_ch['cost_month'] += cost_month
            balance_ch['cost_day'] += cost_day
            balance_ch['income_month'] += income_month
            balance_ch['income_day'] += income_day

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
