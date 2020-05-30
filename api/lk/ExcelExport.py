

from io import BytesIO
import xlsxwriter


from flask import session
from flask import send_file

from ..ObjectAPI import ObjectAPI
from ..ObjectDb import ObjectDb
from ..Auth import isauth


class ExcelExport(ObjectAPI, ObjectDb):
    def __init__(self):
        ObjectAPI.__init__(self)
        ObjectDb.__init__(self)

    def create_axcel_file(self):
        return ''

    def api_get_all_report(self):
        sql = u"""
        SELECT 
        /*Transaction*/
        t.addate_trans , t.date_plan , t.date_fact , t.comment_trans , t.ammount_trans/100.0 , t.count_trans , u.name_user ,
        /*Items*/
        i.title_item , i.unit_price_item, i.default_price_item , i.budget_month_item , i.discript_item ,
        case i.is_vertual_item when '1' then 'Виртуальная категория' else '' end,
        case i.is_cost when '1' then 'Расходная транзакция' else '' end,  
        iu.name_user ,
        /* Accounts */
        a.title_acc , case a.is_public when '1' then 'Общий счет' else '' end , owner.name_user,
        /*Operations*/
        op.code_op , op.amount_op , op.comment_op , opt.title_typeop , ou.name_user 
        from Users u 
            inner join Transactions t 
                on t.id_user = u.id_user 		
            inner join Items i 
                on i.id_acc = t.id_acc		
                inner join Users iu 
                    on i.id_user = iu.id_user 
            inner join Accounts a 
                on a.id_acc = t.id_acc or (a.is_public = '1' and a.id_user_owner = u.id_manager_user)		 
                inner join Users owner on owner.id_user = a.id_user_owner 
            left join Operations op 
                on op.id_op = t.id_op 
                left join Users ou 
                    on ou.id_user = op.id_owner_op 
                left join OpType opt 
                    on opt.alias_typeop = op.type_op 
            where u.id_user = {0}        
        """.format(session['client_sess']['id_user'])
        cur = self.connect.cursor()
        cur.execute(sql)

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        row_id = 0
        worksheet.write(row_id, 0, u'Дата регистрации')
        worksheet.write(row_id, 1, u'Плановая дата')
        worksheet.write(row_id, 2, u'Фактическая дата')
        worksheet.write(row_id, 3, u'Комментарий по транзакции')
        worksheet.write(row_id, 4, u'Стоимость транзакции')
        worksheet.write(row_id, 5, u'Количество')
        worksheet.write(row_id, 6, u'Редактор транзакции')

        worksheet.write(row_id, 7, u'Категория')
        worksheet.write(row_id, 8, u'Ед. измерения')
        worksheet.write(row_id, 9, u'Стоимость по умолчанию')
        worksheet.write(row_id, 10, u'Бюджет по категории')
        worksheet.write(row_id, 11, u'Описание категории')
        worksheet.write(row_id, 12, u'Виртуальность')
        worksheet.write(row_id, 13, u'Тип транзакции')
        worksheet.write(row_id, 14, u'Редактор категории')

        worksheet.write(row_id, 15, u'Счет')
        worksheet.write(row_id, 16, u'Доступ')
        worksheet.write(row_id, 17, u'Владелец счета')

        worksheet.write(row_id, 18, u'Код операции')
        worksheet.write(row_id, 19, u'Стартовая сумма')
        worksheet.write(row_id, 20, u'Комментарий операции')
        worksheet.write(row_id, 21, u'Тип операции')
        worksheet.write(row_id, 22, u'Редактор операции')

        for row in cur.fetchall():
            row_id += 1
            for col in range(0, len(row)):
                worksheet.write(row_id, col, row[col])

        workbook.close()
        output.seek(0)
        return send_file(output, attachment_filename="{}-транзакции.xlsx".format(session['client_sess']['name_user']), as_attachment=True)