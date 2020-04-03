layout_account = {
  name: 'layout_account',
  padding: 0,
  panels: [
    { type: 'main', size: '30%',  content: 'main', resizable: true },
    { type: 'preview', size:'70%', content: '7', resizable: true,
        tabs: {
            active: 'transact_grid',
            tabs: [
                { id: 'transact_grid', caption: 'Транзакции' },
                { id: 'config_categories', caption: 'Категории' },
                // { id: 'config_files', caption: 'Файлы' },
                //{ id: 'edit_account', caption: 'Настройки счета' }
            ],
            onClick: function (event) {
                if (w2ui.config_accounts.getSelection()) {
                    w2ui[event.target].postData['id_acc'] = w2ui.config_accounts.getSelection()[0];
                }
                
                this.owner.content('preview', w2ui[event.target]);
            }
        }
    }
  ]
}


config_accounts = {
        name: 'config_accounts',
        url  : {
            get    : '/acc/get_account_list',
            remove : '/acc/del_account'
        },
        method: 'POST',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarEdit: true,
            columnHeaders: true
        },
        columns: [
            { field: 'title_acc', caption: 'Наименование счета', size: '330px' },

            { field: 'in', caption: 'Входящий', size: '120px' },
            { field: 'income', caption: 'Приход', size: '120px' },
            { field: 'cost', caption: 'Расход', size: '120px' },
            { field: 'out', caption: 'Исходящий', size: '120px' },
            { field: 'discription_acc', caption: 'Комментарий', size: '120px', hidden: true},
            { field: 'name_user_owner', caption: 'Владелец', size: '100%'}
        ],
        onSelect: function(event) {
            if(w2ui.layout_account.get('preview').hidden) {
                w2ui.layout_account.show('preview');
            }
            
            //Назначить фильтр по идентификатору для выбранного счета
            let activ = w2ui.layout_account.get('preview').tabs.active;
            w2ui[activ].postData['id_acc'] = event.recid;
            w2ui[activ].reload();
        },

        onAdd: function(event) {

           w2popup.open({
               style:    "padding:8px;",
               title:'Новый счёт',
               showClose: true,
               width:550,
               height: 230,
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

        },


        onEdit: function(event) {

            w2popup.open({
                style:    "padding:8px;",
                title:'Редактировать счёт',
                showClose: true,
                width:550,
                height: 230,
                body    : '<div id="editAcc"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {
                        let curRec = w2ui.config_accounts.get(w2ui.config_accounts.getSelection()[0]); 
                        w2ui.editAccount.record = {
                            'title_acc': curRec['title_acc_clear'],
                            'id_acc': curRec['recid'],
                            'isPublic': Boolean(Number(curRec['is_public']))
                        };
                        $('#editAcc').w2render('editAccount');
                    };
                },
                onToggle: function (event) {
                    event.onComplete = function () {
                        $(w2ui.editAccount.box).show();
                        w2ui.foo.resize();
                    }
                }
            });
 
         } 


    }
