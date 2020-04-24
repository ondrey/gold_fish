# -*- coding: utf-8 -*-

from json import loads
import datetime

from flask import jsonify
from flask import request
from flask import session

from ..ObjectAPI import ObjectAPI
from ..ObjectAPI import render_tmp
from ..ObjectDb import ObjectDb
from ..ObjectW2UI import search2where
from ..Auth import isauth


class Operations(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)
        self.user_id = None
        if 'client_sess' in session:
            self.user_id = session['client_sess']['id_user']

    def add_operation(self, amount_op, comment_op, type_op):
        """
        Регистрация операции
        :return:
        """
        cur = self.connect.cursor()
        cur.execute(u"insert into Operations (id_owner_op, amount_op, comment_op, type_op) "
                    u"values ({0}, {1}, '{2}', '{3}')".format(
            self.user_id,
            amount_op,
            comment_op,
            type_op
        ))
        self.connect.commit()
        cur.execute(u"SELECT LAST_INSERT_ID()")
        id_rec = cur.fetchone()[0]
        cur.execute(u"select count(*) from Operations where type_op='{0}' and id_owner_op={1}".format(
            type_op, self.user_id
        ))
        countOperations = cur.fetchone()[0]

        amount_type = 'E'
        amount_code = int(amount_op)
        if int(amount_op)/1000 > 0:
            amount_type = 'K'
            amount_code = int(amount_op)/1000
        if int(amount_op)/1000000 > 0:
            amount_type = 'M'
            amount_code = int(amount_op) / 1000000

        code = u"{0}{1}{2}{3}".format(
            type_op,
            str(countOperations+1).rjust(6, '0'),
            amount_type,
            str(amount_code).rjust(3,'0')
        )

        cur.execute(u"update Operations set code_op = '{0}' where id_op = {1}".format(
            code, id_rec
        ))
        self.connect.commit()

        return code, id_rec

    @isauth
    def api_add_operation(self):
        req = loads(request.form['request'])
        result = {}

        code, idrec = self.add_operation(req['record']['amount_op'], req['record']['comment_op'], req['record']['type_op'])

        return jsonify({'code': code, 'idrec': idrec, 'status': 'success'})

    @isauth
    def api_get_records(self):
        cur = self.connect.cursor()
        cur.execute(u"select SQL_CALC_FOUND_ROWS * from Operations where id_owner_op={0}".format(self.user_id))
        records = []
        for row in cur.fetchall():
            records.append({
                  'recid': row[0]
                , 'addate_op': row[1]
                , 'id_owner_op': row[2]
                , 'amount_op': row[3]
                , 'code_op': row[4]
                , 'comment_op': row[5]
                , 'type_op': row[6]
            })

        cur.execute(u"SELECT FOUND_ROWS()")
        total = cur.fetchone()

        return jsonify({
            'total': total,
            'records': records
        })
