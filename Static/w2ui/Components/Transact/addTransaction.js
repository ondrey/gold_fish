addTransaction = {
    name: 'addTransaction',
    style: "height:100%",
    url      : '/transaction/add_transaction',
    fields: [
        { field: 'id_item',   type: 'list',             
            html: { caption: 'Категория', attr: 'size="40" maxlength="40"' },
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
                compare(e,r){
                    let virt = w2ui.addTransaction_toolbar.get('virt');
                    let plus = w2ui.addTransaction_toolbar.get('plus');
                    let res = false;
                    if (plus.checked) {
                        if (e.is_cost != "1") res = e;
                    } else {
                        if (e.is_cost == "1") res = e;
                    }
                    
                    if (virt.checked) {
                        if (e.is_vertual_item != "1") res = false;
                    }

                    return res
                },
                renderDrop: renderDropCategories,    
            }
        },
         
        { name: 'ammount_trans', type: 'float', required: true,
            html: { caption: 'Сумма', attr: 'size="40" maxlength="40"'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}

        },
        { field: 'comments',   type: 'textarea', 
            html: { caption: 'Комментарий', attr: 'style="height: 90px" cols="40"'  } 
        },

        { name: 'date_plan', type: 'date', hidden: true,
            html: { caption: 'Плановая дата', attr: 'size="40" maxlength="40"'}
        },
        { name: 'date_fact', type: 'date', 
            html: { caption: 'Факт. дата', attr: 'size="40" maxlength="40"'}
        },   
    ],
    toolbar: {
        items: [

            { type: 'check',  id: 'virt',  text: 'Виртуальная', icon: 'fa fa-low-vision'},
            { id: 'breakv', type: 'break' },
            { type: 'radio',  id: 'plus',  group: '1', text: 'Доход', icon: 'fa fa-plus', checked: true},
            { type: 'radio',  id: 'minus',  group: '1', text: 'Расход', icon: 'fa fa-minus'},
            
            { id: 'bt3', type: 'spacer' },
            { id: 'plan', type: 'radio', group: '2', text:'Планируется', icon: 'fa fa-calendar-check-o'},
            { id: 'fact', type: 'radio', group: '2', text:'Выполнено', icon: 'fa fa-calendar-check-o', checked: true}
        ],
        onClick: function (event) {
            let cur = new Date();
            if (event.item.id=='fact') {                
                w2ui.addTransaction.record['date_fact'] = cur.toISOString().split('T')[0];
                w2ui.addTransaction.record['date_plan'] = cur.toISOString().split('T')[0];
                
                w2ui.addTransaction.set('date_fact',{hidden: false}); 
                w2ui.addTransaction.set('date_plan',{hidden: true});                
            }
            if (event.item.id=='plan') {
                
                w2ui.addTransaction.record['date_plan'] = cur.toISOString().split('T')[0];
                w2ui.addTransaction.record['date_fact'] = '';

                w2ui.addTransaction.set('date_fact',{hidden: true}); 
                w2ui.addTransaction.set('date_plan',{hidden: false});  
                
            }


            if (event.item.id != 'plan' && event.item.id != 'fact'){
                w2ui.addTransaction.record.id_item  = {};
                w2ui.addTransaction.refresh();
            }
        }
    },
    
    // onChange: function (event) {
    //     if(event.target == 'date_plan') {
    //         w2ui.addTransaction.record['date_fact'] = event.value_new;
    //         w2ui.addTransaction.record['date_plan'] = event.value_new;
    //         w2ui.addTransaction.refresh();
    //     }
    // },
    onError: function(event) {
        console.log(event, 'error');
    },

    actions: {        
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            let id_acc = w2ui.config_accounts.getSelection();
            this.save({
                'record': this.record, 
                'id_acc': id_acc[0]
                }, 
                function(e){
                    w2confirm('Добавить еще запись?', '',
                        function(e){
                            if(e=='No') {
                                w2ui.transact_grid.reload();
                                w2ui.addTransaction.clear();
                                w2popup.close();
                            } else {
                                w2ui.addTransaction.clear();
                            }
                        }
                    )                    
                });

            
        }
    }
}
