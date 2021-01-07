

def search2where(search=[], replase_field={}, logic=u'AND'):
    where = []
    logic = ' ' + logic + ' '
    for field in search:
        name = field['field']
        if name in replase_field:
            name = replase_field[name]

        if field['type'] == 'text':
            if field['operator'] == 'begins':
                where.append(u"{0} like('{1}%')".format(name, field['value']))
            elif field['operator'] == 'is':
                where.append(u"{0}='{1}'".format(name, field['value']))
            elif field['operator'] == 'contains':
                where.append(u"{0} like('%{1}%')".format(name, field['value']))
            elif field['operator'] == 'ends':
                where.append(u"{0} like('%{1}')".format(name, field['value']))

        if field['type'] == 'list':
            where.append(u'{0}={1}'.format(name, field['value']))

        if field['type'] == 'float':
            if field['operator'] == 'is':
                where.append(u'{0}={1}'.format(name, field['value']))
            elif field['operator'] == 'between':
                where.append(u'{0}>={1} and {0}<={2}'.format(name, field['value'][0], field['value'][1]))
            elif field['operator'] == 'less':
                where.append(u'{0}<={1}'.format(name, field['value']))
            elif field['operator'] == 'more':
                where.append(u'{0}>={1}'.format(name, field['value']))

        if field['type'] == 'date':
            if field['operator'] == 'is':
                where.append(u"{0}='{1}'".format(name, field['value']))
            elif field['operator'] == 'between':
                where.append(u"{0} between '{1}' and '{2}'".format(name, field['value'][0], field['value'][1]))

            elif field['operator'] == 'less':
                where.append(u"{0}<='{1}'".format(name, field['value']))
            elif field['operator'] == 'more':
                where.append(u"{0}<='{1}'".format(name, field['value']))

    if len(where) > 0:
        return u"({0})".format(logic.join(where))
    return u""
