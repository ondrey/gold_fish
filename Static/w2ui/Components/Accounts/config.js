layout_account = {
  name: 'layout_account',
  padding: 0,
  panels: [
    { type: 'main', size: '30%',  content: 'main', resizable: true },
    { type: 'preview', size:'70%', content: '7', resizable: true,
        tabs: {
            active: 'tab1',
            tabs: [
                { id: 'transact_grid', caption: 'Транзакции' },
                { id: 'config_categories', caption: 'Категории' },
                { id: 'edit_account', caption: 'Настройки' }
            ],
            onClick: function (event) {
                this.owner.content('preview', w2ui[event.target]);
            }
        }
    }
  ]
}


config_accounts = {
        name: 'config_accounts',
        url  : {
            get    : '/acc/get_account_list'
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
            { field: 'title_acc', caption: 'Наименование счета', size: '330px' },

            { field: 'in', caption: 'Входящий', size: '120px' },
            { field: 'income', caption: 'Приход', size: '120px' },
            { field: 'cost', caption: 'Расход', size: '120px' },
            { field: 'out', caption: 'Исходящий', size: '120px' },
            { field: 'discription_acc', caption: 'Комментарий', size: '120px', hidden: true},
            { field: 'name_user_owner', caption: 'Владелец', size: '100%'},
            { field: 'virtual', caption: 'Виртуальный', size: '100%'},
        ],
        onSelect: function(event) {
            //Назначить фильтр по идентификатору для выбранного счета
            console.log(w2ui.layout_account.get('preview').tabs.active);

        },

        onAdd: function(event) {
            console.log(event)

            w2popup.open({
                title   : 'Редактирование',               
                showMax : true,
                height  :330,
                body    : '<div id="smain"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {                        
                        $('#smain').w2render('addAccount');
                    };
                },
                onToggle: function (event) { 
                    event.onComplete = function () {
                        $(w2ui.add_form_account.box).show();
                        w2ui.foo.resize();
                    }
                }
            });

        }  
    }
