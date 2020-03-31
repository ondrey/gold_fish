addCategories = {
    name: 'addCategories',
    style: "height:100%",
    url      : '/categories/add_record',
    fields: [

        { name: 'title_item', type: 'text', required: true,
            html: { caption: 'Категория', attr: 'size="40" maxlength="40"'}
        },
        { field: 'is_vertual_item', type: 'checkbox',
            html: { caption: 'Виртуальная', attr: 'style="width: auto;"' }
        },
        { field: 'discript_item',   type: 'textarea',
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"' }
        },
        { field: 'id_icon', type: 'list',
            options: {
                url:"/categories/get_icon_list", 
                minLength:0
            },
            html: { 
                caption: 'Значёк', attr: 'style="width: 100%;"', 
                text: '<br/><i id="iconPreview"></i>'
            },            
        }        
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
                    w2ui.config_categories.reload();                    
                    this.clear();
                    w2popup.close();
                                      
                });
        }
    },
    onChange: function (event) {
        console.log(event);
        $('#iconPreview').removeClass();
        $('#iconPreview').addClass(event.value_new.icon);        
    }
}
