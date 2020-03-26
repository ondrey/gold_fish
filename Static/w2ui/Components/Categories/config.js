config_categories = {
        name: 'config_categories',
        method: 'POST',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            columnHeaders: true
        },
        columns: [
            { field: 'title_cat', caption: 'Наименование категории', size: '330px' },
            { field: 'account', caption: 'Счет', size: '120px' },
            { field: 'vertual', caption: 'Вертуальная категория', size: '120px' },
            { field: 'ammount', caption: 'Стоимость', size: '120px' }
        ],
    }