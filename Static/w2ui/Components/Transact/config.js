var transact_grid = {
        name: 'transact_grid',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarSave: true,
            toolbarEdit: true
        },
        method: 'GET', // need this to avoid 412 error on Safari
        columns: [
            { field: 'addate_transact', caption: 'Дата регистрации', size: '5%' },
            { field: 'date_transact', caption: 'Плановая дата', size: '5%' },
            { field: 'cost_item', caption: 'Статья расхода', size: '5%' },
            { field: 'amount_transact', caption: 'Сумма', size: '5%' },
            { field: 'fact_date', caption: 'Фактическая дата', size: '5%' },
            { field: 'account_title', caption: 'Cчет', size: '5%' },
            { field: 'account_num', caption: 'Номер счета', size: '5%' },
            { field: 'op_num', caption: 'Номер операции', size: '5%' },
            { field: 'op_type', caption: 'Тип операции', size: '5%' },
            { field: 'user', caption: 'Владелец счета', size: '5%' }
        ]
    }
