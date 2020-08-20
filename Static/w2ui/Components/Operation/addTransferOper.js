addLayoutTransfer = {
    name: 'addLayoutTransfer',
    padding: 0,
    panels: [
      { type: 'left', size: '100%', style: "height:100%",  content: '', hidden: true,
        toolbar: {
            items: [
                
                { type: 'button',  id: 'item4',  caption: 'Отмена', icon: 'fa fa-times-circle'},
                { type: 'spacer' },
                { type: 'button',  id: 'item5',  caption: 'Использовать', icon: 'fa fa-check-circle-o'}
            ],
            onClick: function (event) {                
                if (event.target=='item4') {
                    w2ui.addLayoutTransfer.hide('left');
                    w2ui.addLayoutTransfer.show('main');
                }
                if (event.target=='item5') {
                    let sel = w2ui.config_accounts_selector.getSelection()
                    if (sel.length == 1) {
                        let rec = w2ui.config_accounts_selector.get(sel[0]);

                        w2ui.addTransfer.postData[w2ui.addTransfer.curSelect] = sel[0];
                        w2ui.addTransfer.record[w2ui.addTransfer.curSelect] = rec.title_acc_clear;

                        w2ui.addLayoutTransfer.hide('left');
                        w2ui.addLayoutTransfer.show('main');             
                        w2ui.addTransfer.refresh();           

                    } else {
                        w2ui.addLayoutTransfer.message('left', {
                            width: 300,
                            height: 150,
                            body: '<div class="w2ui-centered">Необходимо выбрать счет</div>',
                            buttons: '<button class="w2ui-btn" onclick="w2ui.addLayoutTransfer.message(\'left\')">Ok</button>'
                        })                        
                    }
                }

            }
        }    
        
      },
      { type: 'main', size:'100%', content: '22',
        toolbar: {
        items: [            
            { type: 'button',  id: 'item4',  caption: 'Очистить', icon: 'fa fa-times-circle'},
            { type: 'spacer' },
            { type: 'button',  id: 'item5',  caption: 'Перевод', icon: 'fa fa-check-circle-o', style: "color:green;"}
        ],
        onClick: function (event) { 
            if(event.target=='item4') {
                w2ui.addTransfer.clear();
            }
            if(event.target=='item5') {
                let err = w2ui.addTransfer.validate(false);
                if (err.length > 0) {
                    w2ui.addLayoutTransfer.message('main', {width: 300, height: 150, body: '<div class="w2ui-centered">Нужно заполнить поля</div>', buttons: '<button class="w2ui-btn" onclick="w2ui.addLayoutTransfer.message(\'main\')">Ok</button>'})
                } else {
                    w2ui.addTransfer.record['type_op'] = 'TF'                    
                    w2ui.addTransfer.save({},
                        function(e){
                            w2ui.config_operation.reload();
                            w2ui.addTransfer.clear();
                            w2popup.close();
                    });
                }
            }
        }
            
        },
    }
    ],
    onRender: function(event) {
        w2ui.addTransfer.clear();
        w2ui.addLayoutTransfer.hide('left');
        w2ui.addLayoutTransfer.show('main');
        let cur = new Date();
        w2ui.addTransfer.record['date_op'] = cur.toISOString().split('T')[0];

    }
}


addTransfer = {
    name: 'addTransfer',
    style: "height:100%",
    url      : '/operations/add_transfer_op',   
        
    fields: [
        {   field: 'acc_from', 
            required: true, 
            type: 'text', 
            html: { 
                caption: 'Источник', 
                text:' <a id=\'acc_from\' href="#" onClick="w2ui.addTransfer.selectAccount(this.id)"> <i class="fa fa-crosshairs"></i> Выбрать</a>',
                attr: 'disabled'
            } 
        },

        {   field: 'acc_to', 
            required: true, 
            type: 'text', 
            html: { 
                caption: 'Получатель', 
                text:' <a id=\'acc_to\' href="#" onClick="w2ui.addTransfer.selectAccount(this.id)"> <i class="fa fa-crosshairs"></i> Выбрать</a>',
                attr: 'disabled'
            } 
        },
        
        { field: 'amount_op',   type: 'float',  
            html: { caption: 'Сумма', attr: 'size="33" maxlength="40"'}, 
            required: true, 
            options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}
        },

        { field: 'date_op',   type: 'date',  
            html: { caption: 'Дата', attr: 'size="33" maxlength="40"'}, required: true, 
        },

        { field: 'comment_transact',   type: 'textarea',
            html: { caption: 'Комментарий', attr: 'style="height: 90px; width:228px"' }
        } 

    ],
    curSelect: null,
    selectAccount: function(field){
        this.curSelect = field;
        w2ui.addLayoutTransfer.show('left');
        w2ui.addLayoutTransfer.hide('main');
    },
}