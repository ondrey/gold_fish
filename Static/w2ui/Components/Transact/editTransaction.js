editTransaction = {
    name: 'editTransaction',
    style: "height:100%",
    url      : '/transaction/edit_transaction',
    fields: [
        { field: 'comments',   type: 'textarea', 
            html: { caption: 'Комментарий', attr: 'style="height: 90px" cols="40"'  } 
        },

        { name: 'date_fact', type: 'date',
            html: { caption: 'Факт. дата', attr: 'size="40" maxlength="40"'}
        }, 
        { name: 'date_plan', type: 'date', required: true,
            html: { caption: 'Планируемая дата', attr: 'size="40" maxlength="40"'}
        },         
        { name: 'ammount_trans', type: 'float', required: true,
            html: { caption: 'Сумма', attr: 'size="40" maxlength="40"'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}

        }, 
        
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
                
                renderDrop: renderDropCategories,    
            }
        },        


    ],
    toolbar: {
        items: [
            //{ id: 'bt2', type: 'button', caption: 'Очистить', icon: 'fa fa-trash-o' },
            { id: 'bt3', type: 'spacer' },            
            { id: 'bt4', type: 'button', caption: 'Завершить сейчас', icon: 'fa fa-bolt' },
            //{ id: 'bt5', type: 'button', caption: 'Сохранить', icon: 'fa fa-floppy-o' },
        ],
        onClick: function (event) {
            if (event.target == 'bt4') {
                
                let id_tran = w2ui.transact_grid.getSelection();
                let cur = new Date();
                w2ui.editTransaction.record['date_fact'] = cur.toISOString().split('T')[0];
                
                w2ui.editTransaction.save({
                    'record': this.record,
                    'id_tran': id_tran[0]
                    },
                    function(e){
                        w2ui.transact_grid.reload();
                        w2ui.editTransaction.clear();
                        w2popup.close();               
                    });

            }
        }
    },


    actions: {        
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            let id_tran = w2ui.transact_grid.getSelection();
            this.save({
                'record': this.record,
                'id_tran': id_tran[0]
                },
                function(e){
                    w2ui.transact_grid.reload();
                    w2ui.editTransaction.clear();
                    w2popup.close();               
                });

            
        }
    }
}