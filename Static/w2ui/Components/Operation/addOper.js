addOper = {
    name: 'addOper',
    style: "height:100%",
    url      : '/operations/add_oper',
    fields: [
        { field: 'title_oper',   type: 'text', requared: true,
            html: { caption: 'Наименование', attr: 'style="width: 300px;"', page: 0 }
        }, 
        { field: 'discript_oper',   type: 'textarea',
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"', page: 0 }
        } 
    ],    
    tabs: [
        { id: 'empty', caption: 'Шаблон' },
        { id: 'transfer', caption: 'Перевод'},
        { id: 'return', caption: 'Повтор' }
    ],

    actions: {
        Reset: function () { this.clear(); },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            let clear = this.clear;
            this.save({
                'record': this.record, 
                'selection': w2ui.config_accounts.getSelection()
                }, 
                function(e){
                    w2ui.config_categories.reload();                                        
                    w2ui.addOper.clear();
                    w2popup.close();
                    
                });
        }
    }
}
