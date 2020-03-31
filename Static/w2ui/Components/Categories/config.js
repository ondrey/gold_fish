config_categories = {
        name: 'config_categories',
        url: {
            get: '/categories/get_list_for_acc'
        },
        method: 'POST',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            columnHeaders: true
        },
        columns: [
            { field: 'title_cat', caption: 'Наименование категории', size: '330px' },
            { field: 'is_vertual_item', caption: 'Виртуальный', size: '120px', 
                editable: { type: 'checkbox', style: 'text-align: center' } 
            },
            { field: 'discript_item', caption: 'Описание', size: '120px'}
        ],

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
 
         } 

    }