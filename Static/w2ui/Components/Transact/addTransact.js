addTransact = {
    name: 'addTransact',
    style: "height:100%",
    url      : '/acc/add_transaction',
    fields: [
        
        { name: 'date_plan', type: 'date', required: true,
            html: { caption: 'Плановая дата', attr: 'size="40" maxlength="40"'}
        },
        { name: 'date_fact', type: 'date', 
            html: { caption: 'Факт. дата', attr: 'size="40" maxlength="40"'}
        },   
        { name: 'ammount_trans', type: 'float', required: true,
            html: { caption: 'Сумма', attr: 'size="40" maxlength="40"'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}

        },
        { field: 'comments',   type: 'textarea', 
            html: { caption: 'Комментарий', attr: 'style="height: 90px" cols="40"'  } 
        },
    ],
    onChange: function (event) {
        if(event.target == 'date_plan') {
            w2ui.addTransact.record['date_fact'] = event.value_new;
            w2ui.addTransact.record['date_plan'] = event.value_new;
            w2ui.addTransact.refresh();
        }
    },

    actions: {        
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            let acc = w2ui.config_accounts.getSelection();
            let cat = w2ui.config_accounts.getSelection();
            

            this.save({
                'record': this.record, 
                'selection_acc': acc,
                'selection_cat': cat
                }, 
                function(e){
                    w2ui.config_accounts.reload();                    
                    w2ui.addTransact.clear();
                    w2popup.close();
                                     
                });

            
        }
    }
}
