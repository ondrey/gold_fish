var renderDropCategories = function(event) {
    let icon = '<i class="fa fa fa-plus" style="font-size: larger;color: green;"></i>';
    if (event.is_cost == "1")
        icon = '<i class="fa fa fa-minus" style="font-size: larger;color: red;"></i>';
    let style = ""
    if (event.is_vertual_item == "1")
        style = "color: grey;";
    
    return '<span style="'+style+'">' + icon + ' ' + event.text + '</span>'
}


var transact_grid = {
        name: 'transact_grid',
        url  : {
            get    : '/transaction/get_records',
            remove : '/transaction/del_record'
        },
        method: 'POST', 
        autoLoad: false,
        markSearch: true,
        show: {
            toolbar: true,
            footer: true,
            toolbarDelete: true,
            toolbarAdd: true,
            toolbarEdit: true
        },
        onRequest(event){            
            let filter = w2ui.transact_grid_toolbar.get("item1");
            event.postData['is_hot_filter'] = filter.checked;   
            return event
        },
        
        toolbar: {
            items: [
                //{ type: 'break' },
                //{ id: 'finish', type: 'button', caption: 'Завершить сейчас', icon: 'fa fa-bolt' },
                
                { type: 'spacer' },
                
                { type: 'menu',   id: 'menu_transact', caption: 'Действия', 
                    items: [
                        { id: 'cut', text: 'Вырезать', icon: 'fa fa-scissors' }, 
                        { id: 'paste', text: 'Вставить', icon: 'fa fa-clipboard', count: 0, cut: [] }
                    ]
                },
                
                { 
                    type: 'check',  id: 'item1', caption: 'Тёплые', 
                    icon: 'redicon fa fa-free-code-camp', checked: true,
                    tooltip: "Отображать транзакции за сегодня + неделя планируемых."
                },
                


                // { type: 'button', id: 'toggleAcc', caption: '', icon: 'fa fa-chevron-up' },
                
                
            ],
            onClick: function (target, data) {

                if (target=='toggleAcc') {
                    if (w2ui.layout_operation.box) {
                        w2ui.layout_operation.toggle('top');
                    } else {
                        w2ui.layout_account.toggle('top');
                    }
                    
                } else if (target=='item1') {
                    data.onComplete = function(){
                        w2ui.transact_grid.reload();
                    }
                } else if (target=='finish') {
                   
                } else if (target=='menu_transact') {
                                        
                    if (w2ui.transact_grid.getSelection().length) {
                        w2ui.transact_grid_toolbar.set('menu_transact:cut', { disabled: false})
                    } else {
                        w2ui.transact_grid_toolbar.set('menu_transact:cut', { disabled: true})
                    }
                    let paste = w2ui.transact_grid_toolbar.get('menu_transact:paste')
                    if (paste.count>0) {
                        w2ui.transact_grid_toolbar.set('menu_transact:paste', { disabled: false})
                    } else {
                        w2ui.transact_grid_toolbar.set('menu_transact:paste', { disabled: true})
                    }
                    
                } else if (target=='menu_transact:cut') {
                    w2ui.transact_grid_toolbar.set('menu_transact:paste', {
                        disabled: false, 
                        cut: w2ui.transact_grid.getSelection(),
                        count: w2ui.transact_grid.getSelection().length
                    })
                } else if (target=='menu_transact:paste') {
                    let paste = w2ui.transact_grid_toolbar.get('menu_transact:paste')
                    let id_new_acc = w2ui.config_accounts.getSelection()

                    if (id_new_acc.length) {
                        $.post("/transaction/paste_in_account", {
                            data: JSON.stringify({id_trans: paste.cut, id_new_acc: id_new_acc[0]})
                        }, function(result){
                            if(result['ok']) {
                                w2ui.transact_grid.reload()
                            }                            
                          });
                    }

                    w2ui.transact_grid_toolbar.set('menu_transact:paste', {
                        disabled: true, 
                        cut: [],
                        count: 0
                    })
                }
                
            }
        },        

        parser: function (responseText) {
            
            var data = $.parseJSON(responseText);
            if ('records'  in data) {

                    // do other things
                for (let i = 0; i < data.records.length; i++) {
                    const rec = data.records[i];
                    let flags = ''
                    data.records[i]['title_item_clear'] = data.records[i]['title_item'];
                    let style_rec = []
                    if (Boolean(Number(rec['is_vertual_item']))) {
                        style_rec.push('color: grey');
                        
                        data.records[i]['title_item'] += ' (Вирт.)'
                    }

                    if (Boolean(Number(rec['is_cost']))) {
                        data.records[i]['title_item']
                        = '<i class="fa fa-minus" style="font-size: larger;color: red;"></i> '
                        + data.records[i]['title_item'];
                    } else {
                        data.records[i]['title_item']
                        = '<i class="fa fa-plus" style="font-size: larger;color: green;"></i> '
                        + data.records[i]['title_item'];
                    }  
                    
                    // Разукрасим просроченные
                    
                    if (new Date(rec.date_plan) < new Date(new Date().toDateString()) && !rec.date_fact) {
                        data.records[i]['info'] = '<i class="fa fa-bolt" style="margin-left: 5px;color: #ff5e00;"></i>';
                        style_rec.push('background-color:#ffdfcc');
                    } 
                    
                    data.records[i]['w2ui'] = {'style': style_rec.join(';')};
                }
            }
            
            return data;
        },       

        columns: [
            { field: 'info', caption: '', size: '40px', info: true},
            { field: 'comment_trans', caption: 'Комментарий', size: '460px'},
            
            { field: 'ammount_trans', caption: 'Сумма', size: '80px', searchable: true}, 
            { field: 'count_trans', caption: 'Кол-во', size: '40px', hidden: true}, 
            { field: 'title_item', caption: 'Категория', size: '185px'},
            { field: 'date_fact', caption: 'Фактическая дата', size: '120px'},

            { field: 'date_plan', caption: 'Плановая дата', size: '120px', searchable: true},
            { field: 'addate_trans', caption: 'Дата регистрации', size: '120px', hidden: true},
            { field: 'name_user', caption: 'Редактор', size: '120px', hidden: true},
            { field: 'title_acc', caption: 'Счет', size: '120px'},
            { field: 'code_op', caption: 'Операция', size: '120px', hidden: true}
        ],        

        searches: [
            { field: 'ammount_trans', caption: 'Сумма', type: 'float', options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '} },
            { field: 'date_plan', caption: 'Плановая дата', type: 'date' },
            { field: 'title_item', caption: 'Категория', type:'text'},
            { field: 'title_acc', caption: 'Счет', type:'text'},
            { field: 'comment_trans', caption: 'Комментарий', type:'text'},
            { field: 'code_op', caption: 'Операция', type:'text'},

        ],

        onAdd: function(event) {
            let width = 750
            if ('id_acc' in this.postData) {
                width = 550
                w2ui.addLayoutTransaction.hide('left')
            } else {
                // переопределим селект для компонента выбора счета
                w2ui.addLayoutTransaction.show('left')
                w2ui.config_accounts_selector.onSelect = function(event) {
                    
                    //Назначить фильтр по идентификатору для выбранного счета
                    
                    w2ui.transact_grid.postData['id_acc'] = event.recid;                    
                    w2ui.addTransaction.record.id_item = {}
                    w2ui.addTransaction.refresh()

                }

            }
            
            w2popup.open({
                style:    "padding:8px;",
                title:'Новая транзакция',
                showClose: true,
                width: width,
                height: 450,
                body    : '<div id="newtrans" style="height:100%"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {

                        let cur = new Date();
                        w2ui.addTransaction.record['date_fact'] = cur.toISOString().split('T')[0];
                        w2ui.addTransaction.record['date_plan'] = cur.toISOString().split('T')[0];
                        
                        w2ui.addLayoutTransaction.content('left', w2ui.config_accounts_selector);
                        w2ui.addLayoutTransaction.content('main', w2ui.addTransaction);

                        $('#newtrans').w2render('addLayoutTransaction');
                    };
                },
                onClose: function(event){
                    w2ui.addTransaction.clear();
                    if (width == 750) w2ui.transact_grid.postData = {};
                }
            });
 
        },        
        onDelete(event){
            
            let recid = w2ui.transact_grid.getSelection();
            let record = w2ui.transact_grid.get(recid[0]);
            // console.log(record);
            // if (record.date_fact && record.is_vertual_item != '1') {
            //     event.preventDefault();
            //     w2ui.layout_account.message('main', {
            //         width: 300,
            //         height: 150,
            //         body: '<div class="w2ui-centered">Нельзя удалить подтвержденную транзакцию.</div>',
            //         buttons: '<button class="w2ui-btn" onclick="w2ui.layout_account.message(\'main\')">Ясно</button>'
            //     });
            // }
        },
        onEdit(event){

            let selection = w2ui.transact_grid.getSelection()[0];
            let record = w2ui.transact_grid.get(selection);
            

            if (record.date_fact) {
                event.preventDefault();
                w2ui.layout_account.message('main', {
                    width: 300,
                    height: 150,
                    body: '<div class="w2ui-centered">Нельзя редактировать подтвержденную транзакцию.</div>',
                    buttons: '<button class="w2ui-btn" onclick="w2ui.layout_account.message(\'main\')">Ясно</button>'
                });
            } else {
                w2popup.open({
                    style:    "padding:8px;",
                    title:'Редактировать транзакцию',
                    showClose: true,
                    width:550,
                    height: 400,
                    body    : '<div id="editrans"></div>',
                    onOpen  : function (event) {
                        event.onComplete = function (event) {
                            w2ui.editTransaction.record['comments'] = record.comment_trans;
                            w2ui.editTransaction.record['date_plan'] = record.date_plan;
                            w2ui.editTransaction.record['ammount_trans'] = record.ammount_trans; 
                            w2ui.editTransaction.record['id_item'] = {id: record.id_item, text: record.title_item_clear};
                            $('#editrans').w2render('editTransaction');
                        };
                    }
                });                  
            }                 

            
          
            
         } 
    }
