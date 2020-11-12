addLayoutTransaction = {
        name: 'addLayoutTransaction',
        padding: 0,
        panels: [
          { type: 'left', size: '200',  content: ''},
          { type: 'main', size:'550', content: ''}
        ]
}

addTransaction = {
    name: 'addTransaction',
    style: "height:100%",
    url      : '/transaction/add_transaction',    
    fields: [
        { field: 'id_item',   type: 'list', required: true,
            html: { caption: 'Категория', attr: 'size="40" maxlength="40"' },
            options: {
                url: '/categories/get_list_transaction',
                minLength: 0,
                match: 'contains',    
                postData: {
                    id_acc: -1
                },
                onRequest(event){                    
                    event.postData.id_acc=w2ui.transact_grid.postData.id_acc;
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
         
        { field: 'comments',   type: 'textarea', 
            html: { caption: 'Комментарий', attr: 'style="height: 90px" cols="40"'  } 
        },
        { name: 'ammount_trans', type: 'float', required: true,
            html: {caption: 'Стоимость', attr: 'size="40" maxlength="40"'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}

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
            { type: 'radio',  id: 'plus',  group: '1', text: 'Доход', icon: 'fa fa-plus'},
            { type: 'radio',  id: 'minus',  group: '1', text: 'Расход', icon: 'fa fa-minus', checked: true},
            
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
    actions: {
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            let fact = w2ui.addTransaction_toolbar.get('fact')
            if(!fact.checked) {
                w2ui.addTransaction.record['date_fact'] = '';                
            }
            record = {
                'record': this.record
            }
            
            if ('id_acc' in w2ui.transact_grid.postData) {
                record['id_acc'] = w2ui.transact_grid.postData.id_acc
            }
            
            if ('id_op' in w2ui.transact_grid.postData) {
                record['id_op'] = w2ui.transact_grid.postData.id_op
            }

            this.save(
                record, 

                function(e){
                    w2confirm('Добавить еще запись?', '',
                        function(e){
                            if(e=='No') {
                                w2ui.transact_grid.reload();
                                w2ui.addTransaction.clear();
                                w2popup.close();
                            } else {
                                w2ui.addTransaction.record.comments = "";
                                w2ui.addTransaction.record.ammount_trans = "";
                                w2ui.addTransaction.refresh();
                                //w2ui.addTransaction.clear();
                            }
                        }
                    )                    
                });

            
        }
    },
    onChange: function (event) {
        if(event.target == 'id_item') {
            if (event.value_new.default_price) {
                w2ui.addTransaction.record['ammount_trans'] = event.value_new.default_price;
                event.onComplete = function(){
                    w2ui.addTransaction.refresh();
                }
            }
        }
    }    
}
