addOper = {
    name: 'addOper',
    style: "height:100%",
    url  : '/operations/add_operation',
    fields: [
        { field: 'comment_op',   type: 'textarea',
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"', page: 0 }
        }
    ],    

    actions: {
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            let clear = this.clear;

            this.record['type_op'] = 'AA'
            this.record['amount_op'] = 0

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
