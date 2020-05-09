addCategories = {
    name: 'addCategories',
    style: "height:100%",
    url      : '/categories/add_record',
    fields: [

        { name: 'title_item', type: 'text', required: true,
            html: { caption: 'Категория', attr: 'size="40" maxlength="40"'}
        },
        { field: 'is_vertual_item', type: 'checkbox',
            html: { caption: ' ', attr: 'style="width: auto;"', text:' Не суммируется (Виртуальная)' }
        },
        { field: 'is_cost', type: 'checkbox',
            html: { caption: ' ', attr: 'style="width: auto;"', text:' Статья расхода' }
        },
        { field: 'is_for_sub', type: 'checkbox',
            html: { caption: ' ', attr: 'style="width: auto;"', text:' Общий для дочерних счетов' }
        },
        { field: 'discript_item',   type: 'textarea',
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"' }
        }, 
        { name: 'bujet_cat_in_month', type: 'float',
            html: {caption: ' ', attr: 'size="16" maxlength="40"', text:' Бюджет на месяц'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}
        },
        { name: 'default_price', type: 'float',
            html: {caption: ' ', attr: 'size="16" maxlength="40"', text:' Стоимость по умолчанию'},
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}
        },
        { name: 'unit_cat', type: 'text',
            html: {caption: 'Ед.из.', attr: 'size="16" maxlength="40"', text:' Наименование'},            
        },
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
                    w2ui.addCategories.clear();
                    w2popup.close();
                    
                });
        }
    }
}
