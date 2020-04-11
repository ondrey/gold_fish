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
            toolbarDelete: true
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
           
            { field: 'addate_trans', caption: 'Дата регистрации', size: '120px' },
            { field: 'date_plan', caption: 'Плановая дата', size: '120px' },
            { field: 'date_fact', caption: 'Фактическая дата', size: '120px',  render: 'date',
                editable: { type: 'date', options: {btn_now: true} } 
            },

            { field: 'title_item', caption: 'Категория', size: '50%' },
            { field: 'ammount_trans', caption: 'Сумма', size: '80px'}, 
            
            { field: 'comment_trans', caption: 'Комментарий', size: '100%'},
            { field: 'name_user', caption: 'Редактор', size: '120px'},
        ],

    }
