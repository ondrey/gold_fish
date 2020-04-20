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
            toolbarDelete: true
        },
        toolbar: {
          items: [
              { type: 'break' },
              //{ type: 'spacer' },     

              { type: 'menu', id: 'toggleAcc', caption: 'Новая операция', icon: 'fa fa-plus-square',
                selected: 'id3',
                items: [
                  { id: 'id1', text: 'Пустая', icon: 'fa fa-sticky-note-o' },
                  { id: 'id2', text: 'Перевод', icon: 'fa fa-exchange' },
                  { id: 'id3', text: 'Итерация', icon: 'fa fa-history' }
                ]
              },
              
              
          ],
          onClick: function (target, data) {
            console.log(target);              
          }
        },     

        columns: [
            
            { field: 'addate', caption: 'Время регистрации', size:"150"},
            { field: 'type_op', caption: 'Тип операции', size:"150"},
            { field: 'date_end', caption: 'Комментарий', size:"100%"},
            { field: 'guid_op', caption: 'Код', size:"120", info:true},
        ],

        multiSearch: true,
        records: [],

        onAdd: function(event) {

          w2popup.open({
              style:    "padding:8px;",
              title:'Новая операция',
              showClose: true,
              width:550,
              height: 450,
              body    : '<div id="newoper"></div>',
              onOpen  : function (event) {
                  event.onComplete = function () {      
                      $('#newoper').w2render('addOper');                        
                  };
              }
          });

       },     
      

    }
