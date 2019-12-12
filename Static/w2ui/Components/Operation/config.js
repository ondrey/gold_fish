layout_operation = {
  name: 'layout_operation',
  padding: 0,
  panels: [
    { type: 'main', size: '30%',  content: 'main' },
    { type: 'preview', size:'70%', content: '7'}
  ]
}

config_operation = {
        name: 'config_operation',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarEdit: true,
            columnHeaders: true
        },
        columns: [
            { field: 'recid', caption: 'id', size:"10%"},
            { field: 'guid_op', caption: 'Код', size:"10%"},
            { field: 'addate', caption: 'Время регистрации', size:"10%"},
            { field: 'date_start', caption: 'Начало', size:"10%"},
            { field: 'date_end', caption: 'Завершение', size:"10%"},
            { field: 'unit', caption: 'Еденица деления', size:"10%"},
            { field: 'amount', caption: 'Стоимость деления', size:"10%"}
        ],

        multiSearch: true,
        records: [],

        onAdd: function (event) {
          let text = "<p>Вы можете выбрать один из предложенных типов операции</p>";
          text += "<a href='#' style=\"margin-top: 29px;display: block;\">Разделение по счетам </br> <img src='/static/w2ui/Components/Operation/account.png' /></a> <br />";
          text += "<a href='#' style=\"margin-top: 29px;display: block;\">Разделение во времени </br><img src='/static/w2ui/Components/Operation/optype.png' /></a>";

          w2popup.open({
              body: '<div class="w2ui-centered">'+text+'</div>',
              color: '#3b798c',
              height: 400
           });

        },

    }
