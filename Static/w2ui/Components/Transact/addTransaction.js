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
                renderDrop(event){
                    let icon = '<i class="fa fa fa-plus" style="font-size: larger;color: green;"></i>';
                    if (event.is_cost == "1")
                        icon = '<i class="fa fa fa-minus" style="font-size: larger;color: red;"></i>';
                    let style = ""
                    if (event.is_vertual_item == "1")
                        style = "color: grey;";
                    
                    return '<span style="'+style+'">' + icon + ' ' + event.text + '</span>'
                }            
            }
        },
         
        { name: 'ammount_trans', type: 'float', required: true,
            html: { caption: 'Сумма', attr: 'size="40" maxlength="40"'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}

        },
        { field: 'comments',   type: 'textarea', 
            html: { caption: 'Комментарий', attr: 'style="height: 90px" cols="40"'  } 
        },

        { name: 'date_plan', type: 'date', hidden:true,
            html: { caption: 'Плановая дата', attr: 'size="40" maxlength="40"'}
        },
        { name: 'date_fact', type: 'date', hidden:true,
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
            { id: 'date', type: 'check', text:'Сегодня', icon: 'fa fa-calendar-check-o', checked: true}
        ],
        onClick: function (event) {
            if (event.item.id=='date') {
                w2ui.addTransaction.set('date_plan',{hidden:!event.item.checked});
                w2ui.addTransaction.set('date_fact',{hidden:!event.item.checked});
            }
            if (event.item.id != 'date'){
                w2ui.addTransaction.record.id_item  = {};
                w2ui.addTransaction.refresh();
            }

            
        }
    },
    
    onChange: function (event) {
        if(event.target == 'date_plan') {
            w2ui.addTransaction.record['date_fact'] = event.value_new;
            w2ui.addTransaction.record['date_plan'] = event.value_new;
            w2ui.addTransaction.refresh();
        }
    },

    actions: {        
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            this.save({
                'record': this.record, 
                }, 
                function(e){
                    w2ui.config_accounts.reload();                    
                    w2ui.addTransaction.clear();
                    w2popup.close();
                                     
                });

            
        }
    }
}
