layout_account = {
  name: 'layout_account',
  padding: 0,
  panels: [
    { type: 'main', size: '30%',  content: 'main', resizable: true },
    { type: 'preview', size:'70%', content: '7', resizable: true}
  ]
}
config_accounts = {
        name: 'config_accounts',
        url  : {
            get    : '/acc/get_account_list',
            remove : '',
            save   : ''
        },
        method: 'POST',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarEdit: true,
            columnHeaders: true
        },
        selectType : 'row',
        columns: [
            { field: 'title_acc', caption: 'Наименование счета/статьи', size: '60%' },

            { field: 'in', caption: 'Входящий', size: '10%' },
            { field: 'income', caption: 'Приход', size: '10%' },
            { field: 'cost', caption: 'Расход', size: '10%' },
            { field: 'out', caption: 'Исходящий', size: '10%' },
            { field: 'name_user_owner', caption: 'Владелец', size: '10%'},
        ]
    }
