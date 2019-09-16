layout_account = {
  name: 'layout_account',
  padding: 0,
  //style: 'height: 100%; position: relative; width:100%;',
  panels: [
    { type: 'main', size: '30%',  content: 'main' },
    { type: 'preview', size:'70%', content: '7'}
  ]
}
config_accounts = {
        name: 'config_accounts',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarEdit: true,
            columnHeaders: true
        },
        columns: [
            { field: 'account', caption: 'Наименование счета/статьи', size: '60%' },
            { field: 'info', caption: '', size: '10%', style:'color:#688e39;font-size: large;'},
            { field: 'in', caption: 'Входящий', size: '10%' },
            { field: 'income', caption: 'Приход', size: '10%' },
            { field: 'cost', caption: 'Расход', size: '10%' },
            { field: 'out', caption: 'Исходящий', size: '10%' }
        ],
        multiSearch: true,
        searches: [
                    { field: 'recid', caption: 'Номер счета ', type: 'int' },
                    { field: 'period', caption: 'Период', type: 'date' }
                ],

        records: [
            { recid: 'SDFSDLFK23141K2L12KJL1', account: 'Alfa-bank', info: '<i class="fa fa-line-chart" aria-hidden="true"></i> <i class="fa fa-rocket" aria-hidden="true"></i> <i class="fa fa-check-square" aria-hidden="true"></i>'}]
    }
