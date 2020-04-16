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

        show: {
            toolbar: true,
            footer: true,
            toolbarDelete: true,
            toolbarAdd: true
        },

        toolbar: {
            items: [
                //{ type: 'break' },
                { type: 'spacer' },                
                { type: 'button', id: 'toggleAcc', caption: '', icon: 'fa fa-chevron-up' }
            ],
            onClick: function (target, data) {
                
                if (target=='toggleAcc') {
                    w2ui.layout_account.toggle('top');
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

                    if (Boolean(Number(rec['is_vertual_item']))) {
                        data.records[i]['w2ui'] = {'style':'color: grey;'};
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
                }
            }
            
            return data;
        },


        columns: [
            { field: 'comment_trans', caption: 'Комментарий', size: '200px'},
            
            { field: 'ammount_trans', caption: 'Сумма', size: '80px', searchable: true}, 
            { field: 'title_item', caption: 'Категория', size: '185px'},
            { field: 'date_fact', caption: 'Фактическая дата', size: '120px', searchable: true},

            { field: 'date_plan', caption: 'Плановая дата', size: '120px', searchable: true},
            { field: 'addate_trans', caption: 'Дата регистрации', size: '120px', searchable: true},
            { field: 'name_user', caption: 'Редактор', size: '120px'},
        ],        

        searches: [
            { field: 'ammount_trans', caption: 'Сумма', type: 'float', options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '} },
            { field: 'id_item',   type: 'list', caption: 'Категория',  
              options: {
                url: '/categories/get_list_transaction',
                minLength: 0,
                match: 'contains',    
                postData: {
                    id_acc: -1
                },
                onRequest(event){
                    let sel = w2ui.config_accounts.getSelection();
                    event.postData.id_acc=sel[0];
                    return event
                },
                renderDrop: renderDropCategories,
              }
            },

            { field: 'date_fact', caption: 'Фактическая дата', type: 'date' },
            { field: 'date_plan', caption: 'Плановая дата', type: 'date' },
            { field: 'addate_trans', caption: 'Дата регистрации', type: 'date' },

        ],

        onAdd: function(event) {

            w2popup.open({
                style:    "padding:8px;",
                title:'Новая транзакция',
                showClose: true,
                width:550,
                height: 450,
                body    : '<div id="newtrans"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {
                        let cur = new Date();
                        w2ui.addTransaction.record['date_fact'] = cur.toISOString().split('T')[0];
                        w2ui.addTransaction.record['date_plan'] = cur.toISOString().split('T')[0];
        
                        $('#newtrans').w2render('addTransaction');                        
                    };
                }
            });
 
         },        

    }
