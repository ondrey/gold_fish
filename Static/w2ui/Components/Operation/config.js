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
        url: {
          get: '/operations/get_records'
        },
        method: 'POST',

        show: {
            toolbar: true,
            footer: true,
            toolbarDelete: true
        },

        toolbar: {
          tooltip: 'bottom',
          items: [
              { type: 'break' },
              //{ type: 'spacer' },     

              { type: 'menu', id: 'toggleAcc', caption: 'Новая операция', icon: 'fa fa-plus-square',
                selected: 'id3',
                tooltip: 'Операция - логически связывает несколько транзакций.',
                items: [
                  { id: 'id1', text: 'Простая', icon: 'fa fa-sticky-note-o', 
                    tooltip: 'Операция для групперовки логически связанных транзакций'
                  },
                  { id: 'id2', text: 'Перевод средств', icon: 'fa fa-exchange',
                    tooltip: 'Перевод средств между счетами'
                  },
                  { id: 'id3', text: 'Повторяющаяся операция', icon: 'fa fa-history',
                    tooltip: 'Повторяющаяся операция - ежедневно, ежемесячно, ежегодно...'
                  }
                ]
              },
              
              
          ],
          onClick: function (target, data) {
            console.log(target);      

            if (target == 'toggleAcc:id1') {
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
            }        


          }
        },     

        columns: [            
            { field: 'code_op', caption: 'Операция', size:"150"},
        ],

        multiSearch: true,
        records: [],
    }
