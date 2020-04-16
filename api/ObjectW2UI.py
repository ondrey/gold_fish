# -*- coding: utf-8 -*-


def __search2where(search=[], replase_field={}):
    where = u'1=1 '

    for field in search:
        name = field['field']
        if name in replase_field:
            name = replase_field[name]

        if field['type'] == 'list':
            where += u'and {0}={1} '.format(name, field['value'])
        if field['type'] == 'float':
            if field['operator'] == 'is':
                where += u'and {0}={1} '.format(name, field['value'])
            elif field['operator'] == 'between':
                where += u'and {0}>={1} and {0}<={2} '.format(name, field['value'][0], field['value'][1])
        pass

    return where