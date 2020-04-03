editAccount = {
    name: 'editAccount',
    style: "height:100%",
    url      : '/acc/edit_account',
    fields: [
        
        { name: 'title_acc', type: 'text', required: true,
            html: { caption: 'Название счета', attr: 'size="40" maxlength="40"'}
        },   
        { field: 'isPublic', type: 'checkbox',
            html: { caption: 'В общем доступе', attr: 'style="width: auto;"' }
        },
    ],
    
    actions: {
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            this.save({
                'record': this.record, 
                'selection': w2ui.config_accounts.getSelection()
                }, 
                function(e){
                    w2ui.config_accounts.reload();                    
                    w2popup.close();
                    this.clear();                   
                });

            
        }
    }
}
