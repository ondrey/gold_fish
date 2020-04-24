addOper = {
    name: 'addOper',
    style: "height:100%",
    url  : '/operations/add_operation',
    fields: [
        { field: 'amount_op',   type: 'text', requared: true,
            html: { caption: 'сумма', attr: 'style="width: 300px;"', page: 0 }
        }, 
        { field: 'comment_op',   type: 'textarea',
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"', page: 0 }
        },
        { field: 'type_op',   type: 'text', requared: true,
            html: { caption: 'Тип', attr: 'style="width: 300px;"', page: 0 }
        }, 
    ],    

    actions: {
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            let clear = this.clear;
            this.save({
                'record': this.record
                }, 
                function(e){
                    w2ui.config_operation.reload();                                        
                    w2ui.addOper.clear();
                    w2popup.close();
                    
                });
        }
    }
}
