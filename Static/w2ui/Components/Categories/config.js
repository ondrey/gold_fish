config_categories = {
        name: 'config_categories',
        url: {
            get: '/categories/get_list_for_acc',
            remove: '/categories/del_record'
        },
        method: 'POST',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarEdit: true,
            toolbarDelete: true,
            columnHeaders: true
        },

        columns: [
            { field: 'title_cat', caption: 'Наименование категории', size: '330px', info:true},
            { field: 'amount_cat', caption: 'Сумма транзакций', size: '90px' },
            { field: 'bujet_cat_in_month', caption: 'Бюджет', size: '120px' },
            { field: 'default_price', caption: 'Стоимость по умолчанию', size: '90px', hidden: true},
            { field: 'unit_cat', caption: 'Ед.из.', size: '90px' , hidden: true},
            { field: 'name_user', caption: 'Владелец', size: '150px', hidden: true},
            { field: 'discript_item', caption: 'Описание', size: '100%'},
        ],


        parser: function (responseText) {
            
            var data = $.parseJSON(responseText);
            if ('records'  in data) {

                    // do other things
                for (let i = 0; i < data.records.length; i++) {
                    const rec = data.records[i];
                    let flags = ''
                    data.records[i]['title_cat_clear'] = data.records[i]['title_cat'];

                    if (Boolean(Number(rec['is_vertual_item']))) {
                        data.records[i]['w2ui'] = {'style':'color: grey;'};
                        data.records[i]['title_cat'] += ' (Вирт.)'
                    }
                    if (Boolean(Number(rec['is_cost']))) {
                        data.records[i]['title_cat']
                        = '<i class="fa fa-minus" style="font-size: larger;color: red;"></i> '
                        + data.records[i]['title_cat'];
                    } else {
                        data.records[i]['title_cat']
                        = '<i class="fa fa-plus" style="font-size: larger;color: green;"></i> '
                        + data.records[i]['title_cat'];
                    }                         
                }
            }
            
            return data;
        },

        onAdd: function(event) {
            if (w2ui.config_accounts.getSelection().length == 0) {
                w2ui.layout_account.message('preview', {
                    width: 300,
                    height: 150,
                    body: '<div class="w2ui-centered">Нужно выбрать счет</div>',
                    buttons: '<button class="w2ui-btn" onclick="w2ui.layout_account.message(\'preview\')">Хорошо</button>'
                })

            return
            };

            w2popup.open({
                style:    "padding:8px;",
                title:'Новая категория',
                showClose: true,
                width:550,
                height: 450,
                body    : '<div id="addCat"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {
                        w2ui.addCategories.clear();
                        $('#addCat').w2render('addCategories');
                    };
                },
                onToggle: function (event) {
                    event.onComplete = function () {
                        $(w2ui.addCategories.box).show();
                        w2ui.foo.resize();
                    }
                }
            });
 
        }, 
        onEdit: function(event) {
            w2popup.open({
                style:    "padding:8px;",
                title:'Редактировать категорию',
                showClose: true,
                width:550,
                height: 450,
                body    : '<div id="addCat"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {
                        let curRec = w2ui.config_categories.get(w2ui.config_categories.getSelection()[0]); 
                        w2ui.addCategories.record = {
                            'title_item': curRec['title_cat_clear'],
                            'discript_item': curRec['discript_item'],
                            'is_vertual_item': Boolean(Number(curRec['is_vertual_item'])),
                            'is_cost': Boolean(Number(curRec['is_cost'])),
                            'id_item': curRec['recid'],
                            'is_for_sub': Boolean(Number(curRec['is_for_sub'])),
                            'for_telegramm': Boolean(Number(curRec['for_telegramm'])),

                            'bujet_cat_in_month': curRec['bujet_cat_in_month'],
                            'default_price': curRec['default_price'],
                            'unit_cat': curRec['unit_cat']

                        };
                        
                        $('#addCat').w2render('addCategories');
                    };
                }
            });
 
         } 
    }