addLayoutCicle = {
    name: 'addLayoutCicle',
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
                    w2ui.addLayoutCicle.hide('left');
                    w2ui.addLayoutCicle.show('main');
                }
                if (event.target=='item5') {
                    let sel = w2ui.config_accounts_selector.getSelection()
                    if (sel.length == 1) {
                        let rec = w2ui.config_accounts_selector.get(sel[0]);

                        w2ui.addCicle.postData[w2ui.addCicle.curSelect] = sel[0];
                        
                        let id_item = w2ui.addCicle.get('id_item');
                        w2ui.addCicle.record.id_item = {};
                        id_item.options.postData.id_acc = sel[0];
                        w2ui.addCicle.set('id_item', { options: id_item.options }); 
                        
                        w2ui.addCicle.record[w2ui.addCicle.curSelect] = rec.title_acc_clear;

                        w2ui.addLayoutCicle.hide('left');
                        w2ui.addLayoutCicle.show('main');             
                        w2ui.addCicle.refresh();

                    } else {
                        w2ui.addLayoutCicle.message('left', {
                            width: 300,
                            height: 150,
                            body: '<div class="w2ui-centered">Необходимо выбрать счет</div>',
                            buttons: '<button class="w2ui-btn" onclick="w2ui.addLayoutCicle.message(\'left\')">Ok</button>'
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
                { type: 'button',  id: 'item5',  caption: 'Создать транзакции', icon: 'fa fa-check-circle-o', style: "color:green;"}
            ],
            onClick(event){
                if(event.target=='item4') {
                    w2ui.addCicle.clear();
                }

                if(event.target=='item5') {
                    let err = w2ui.addCicle.validate(false);
                    if (err.length > 0) {
                        w2ui.addLayoutCicle.message('main', {width: 300, height: 150, body: '<div class="w2ui-centered">Нужно заполнить поля</div>', buttons: '<button class="w2ui-btn" onclick="w2ui.addLayoutTransfer.message(\'main\')">Ok</button>'})
                    } else {
                        w2ui.addCicle.record['type_op'] = 'CT'

                        let selected_op = w2ui.config_operation.getSelection();
                        let finish = function(e){
                            w2ui.config_operation.reload();
                            w2ui.addCicle.clear();
                            w2popup.close();
                        }

                        if(selected_op.length == 0) {
                            w2ui.addCicle.save({}, finish);
                        } else {
                            let selop = w2ui.config_operation.get(selected_op[0])
                            w2confirm('Добавить транзакции в выбранную операцию ('+selop.code_op+')?', 
                            function btn(answer) {
                                if(answer == 'Yes') {
                                    w2ui.addCicle.save({'id_exists':selop.recid}, finish);
                                } else {
                                    w2ui.addCicle.save({}, finish);
                                }
                            });
                        }

                        
                    }

                }
            }
        },
    }
    ],
    // onRender: function(event) {
    //     w2ui.addCicle.clear();
    //     w2ui.addLayoutCicle.hide('left');
    //     w2ui.addLayoutCicle.show('main');
    //     let cur = new Date();
    //     w2ui.addCicle.record['date_op'] = cur.toISOString().split('T')[0];

    // }
}


addCicle = {
    name: 'addCicle',
    style: "height:100%",
    url      : '/operations/add_cicle_op', 
        
    fields: [
        {   field: 'acc', 
            required: true, 
            type: 'text', 
            html: { 
                caption: 'Счет', 
                text:' <a id=\'acc\' href="#" onClick="w2ui.addCicle.selectAccount(this.id)"> <i class="fa fa-crosshairs"></i> Выбрать</a>',
                attr: 'disabled style="width:200px;"'
            } 
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
                renderDrop: renderDropCategories,    
            }
        },
        { field: 'date_start',   type: 'date',  
            html: { caption: 'Начало', attr: 'size="40" maxlength="40"'}, required: true, 
        },
        { field: 'date_finish',   type: 'date',  
            html: { caption: 'Завершение', attr: 'size="40" maxlength="40"'}, required: true, 
        },        
        { field: 'unit', type: 'list', required: true, 
          html: { caption: 'Повтор', attr: 'size="40" maxlength="40"'},
          options: { 
              items: [{id:'day',text:'Каждый день'}, {id:'week',text:'Неделю'}, {id:'month',text:'Месяц'}] 
            } 
        },

        { field: 'price_op',   type: 'float',  
            html: { caption: 'Стоимость', attr: 'size="40" maxlength="40"'}, 
            required: true, options:{autoFormat: false, currencyPrecision:2, groupSymbol:' '}
        },
        { field: 'price_for_unit', type: 'checkbox',  
            html: { caption: 'Разделить стоимость', attr: 'style="text-align:left;"'} 
        },
        
        { field: 'comment_transact',   type: 'textarea',
            html: { caption: 'Комментарий', attr: 'style="height: 50px; width:273px;"' }
        }, 
    ],
    curSelect: null,
    selectAccount: function(field){
        this.curSelect = field;
        w2ui.addLayoutCicle.show('left');
        w2ui.addLayoutCicle.hide('main');
    },
}