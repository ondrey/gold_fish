layout_operation = {
  name: 'layout_operation',
  padding: 0,
  panels: [
    { type: 'top', size: '60%',  content: 'main' },
    { type: 'main', size:'40%', content: '7', resizable: true }
  ]
}

config_operation = {
        name: 'config_operation',
        url: {
          get: '/operations/get_records',
          remove: '/operations/del_record'
        },
        method: 'POST',
        autoLoad: false,
        
        limit: 50,
        show: {
            toolbar: true,
            footer: true,
            toolbarDelete: true
        },
        onSelect: function(event) {   
          w2ui.layout_operation.sizeTo('top', '60%');       
          w2ui.layout_operation.sizeTo('main', '40%');
          //Назначить фильтр по идентификатору для выбранной операции
          w2ui.transact_grid.postData['id_op'] = event.recid;
          w2ui.transact_grid.reload();
        },

        toolbar: {
          tooltip: 'bottom',
          items: [
              { type: 'break' },
              
              { type: 'button',  id: 'AA',  caption: 'Обычная', icon: 'fa fa-sticky-note-o',
                tooltip: 'Шаблон операции, который используется '+
                '<br/>для групперовки логически связанных транзакций.'
              },

              { type: 'button',  id: 'TF',  caption: 'Перевод', icon: 'fa fa-share-square-o',
                tooltip: 'Операция для перевода ДС между счетами. Создает транзакцию '+
                '<br/>расхода на одном счете и транзакцию дохода на другом.'
              },                            
              { type: 'button',  id: 'CT',  caption: 'Циклическая', icon: 'fa fa-history',
                tooltip: 'Создает повтаряющуюся транзакцию, с указанием '+
                '<br/>отрезка повторения - день, месяц, год.'
              },              
          ],
          onClick: function (target, data) {
            if (target == 'AA') {
              w2popup.open({
                style:    "padding:8px;",
                title:'Новая операция',
                showClose: true,
                width:550,
                height: 270,
                body    : '<div id="newoper"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {      
                        $('#newoper').w2render('addOper');                        
                    };
                }
              });
            }
            
            if (target == 'TF') {
              w2popup.open({
                style:    "padding:8px;",
                title:'Перевод',
                showClose: true,
                width:480,
                height: 320,
                body    : '<div id="newtransfer"  style="height:100%"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {   
                      w2ui.addLayoutTransfer.content('left', w2ui.config_accounts_selector);
                      w2ui.addLayoutTransfer.content('main', w2ui.addTransfer);

                      $('#newtransfer').w2render('addLayoutTransfer');
                    };
                }
              });
            }


            if (target == 'CT') {
              w2popup.open({
                style:    "padding:8px;",
                title:'Циклическая',
                showClose: true,
                width:480,
                height: 400,
                body    : '<div id="newtransfer"  style="height:100%"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {   
                      w2ui.addLayoutCicle.content('left', w2ui.config_accounts_selector);
                      w2ui.addLayoutCicle.content('main', w2ui.addCicle);

                      $('#newtransfer').w2render('addLayoutCicle');
                    };
                }
              });
            }            


          }
        },     

        columns: [
            { field: 'comment_op', caption: 'Коментарий', size:"150", info:true},  
            { field: 'amount_op', caption: 'Начальная стоимость', size:"88"},  
            { field: 'code_op', caption: 'Операция', size:"99", editable: { type: 'text' }},
            { field: 'icon_class_op', caption: 'Тип', size:"26"},
            { field: 'percent_complate_op', caption: 'Завершение', size:"50", style:"text-align:center"},
            { field: 'addate_op', caption: 'Дата', size:"150", hidden: true},
            { field: 'plan', caption: 'Сумма по транзакциям', size:"88", hidden: true},
            { field: 'fact', caption: 'Остаток', size:"88", hidden: true},
            { field: 'dstart_op', caption: 'Начало', size:"150", hidden: true},
            { field: 'dfinish_op', caption: 'Завершение', size:"150"},
        ],
        
        searches : [
          { field: 'code_op', caption: 'Код операции', type: 'text' },   
          { field: 'comment_op', caption: 'Коментарий', type: 'text' },       
        ],

        parser: function (responseText) {
            
          var data = $.parseJSON(responseText);
          if ('records'  in data) {

              // do other things
              for (let i = 0; i < data.records.length; i++) {
                  const rec = data.records[i];
                  data.records[i]['plan'] = (rec['amount_plan_op']/100).toLocaleString()
                  data.records[i]['fact'] = ((rec['amount_plan_op'] - rec['amount_fact_op'])/100).toLocaleString()

                  if(rec.count_plan != rec.count_fact) {
                    data.records[i]['w2ui'] = {'style': 'background-color:#7fda7f;'}
                  }
                  
                  
                  if (rec.count_plan>0) {
                    data.records[i]['percent_complate_op'] = Math.abs((rec.count_fact/rec.count_plan)*100) + '%'
                  }

                  data.records[i]['icon_class_op'] = '<i style="font-size: large" class="'+rec['icon_class_op']+'"></>'
              }
          }
          
          return data;
      }      
    }
