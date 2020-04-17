# -*- coding: utf-8 -*-


def search2where(search=[], replase_field={}, logic=u'AND'):
    where = u''

    for field in search:
        name = field['field']
        if name in replase_field:
            name = replase_field[name]

        if field['type'] == 'text':
            if field['operator'] == 'begins':
                where += u"and {0} like('{1}%') ".format(name, field['value'])
            elif field['operator'] == 'is':
                where += u"and {0}='{1}' ".format(name, field['value'])
            elif field['operator'] == 'contains':
                where += u"and {0} like('%{1}%') ".format(name, field['value'])
            elif field['operator'] == 'ends':
                where += u"and {0} like('%{1}') ".format(name, field['value'])

        if field['type'] == 'list' and logic == u'AND':
            where += u'and {0}={1} '.format(name, field['value'])

        if field['type'] == 'float' and logic == u'AND':
            if field['operator'] == 'is':
                where += u'and {0}={1} '.format(name, field['value'])
            elif field['operator'] == 'between':
                where += u'and {0}>={1} and {0}<={2} '.format(name, field['value'][0], field['value'][1])
            elif field['operator'] == 'less':
                where += u'and {0}<={1} '.format(name, field['value'])
            elif field['operator'] == 'more':
                where += u'and {0}>={1} '.format(name, field['value'])

        if field['type'] == 'date' and logic == u'AND':
            if field['operator'] == 'is':
                where += u"and {0}='{1}' ".format(name, field['value'])
            elif field['operator'] == 'between':
                where += u"and {0} between '{1}' and '{2}' ".format(name, field['value'][0], field['value'][1])

            elif field['operator'] == 'less':
                where += u"and {0}<='{1}' ".format(name, field['value'])
            elif field['operator'] == 'more':
                where += u"and {0}<='{1}' ".format(name, field['value'])

    return where