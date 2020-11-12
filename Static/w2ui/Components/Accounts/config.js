layout_account = {
  name: 'layout_account',
  padding: 0,
  panels: [
    { type: 'top', size: '50%',  content: '', resizable: true },
    { type: 'main', size:'50%', content: '', resizable: true, 
        tabs: {
            active: 'transact_grid',
            tabs: [
                { id: 'transact_grid', caption: 'Транзакции' },
                { id: 'config_categories', caption: 'Категории' },
                // { id: 'config_files', caption: 'Файлы' },
                //{ id: 'edit_account', caption: 'Настройки счета' }
            ],
            onClick: function (event) {
                w2ui.config_categories.toolbar.disable('addTrans');
                
                if (w2ui.config_accounts.getSelection()) {
                    w2ui[event.target].postData['id_acc'] = w2ui.config_accounts.getSelection()[0];
                }
                
                this.owner.content('main', w2ui[event.target]);
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
        onLoad: function(event) {
            event.onComplete = function(ev){                
                w2ui.config_accounts.records.forEach(el => {                    
                    if ('children' in el.w2ui) {      
                        w2ui.config_accounts.expand(el.recid);
                    }
                });
            }
            w2ui.transact_grid_toolbar.set('menu_transact', { disabled: false});
        },
        
        postData: {
            'filter': 'item2:month'
        },

        toolbar: {
            items: [
                { type: 'spacer' },
                
                { type: 'menu-radio', id: 'item2', icon: 'fa fa-balance-scale',
                text: function (item) {
                    var text = item.selected;
                    var el   = this.get('item2:' + item.selected);
                    return 'Остаток: ' + el.text;
                },
                selected: 'month',
                items: [
                    { id: 'day', text: 'Сегодня'},
                    { id: 'month', text: 'Месяц' }
                ]
            },
            ],
            onClick: function (target, data) {
                console.log(target);
                w2ui.config_accounts.postData["filter"] = target

                if (target == 'item2:day' || target == 'item2:month') {
                    w2ui.config_accounts.reload();
                }
                
            }
        },        

        columns: [
            { field: 'title_acc', caption: 'Наименование счета', size: '330px'},
            
            { field: 'input', caption: 'Входящий остаток', size: '120px' },
            
            { field: 'cost', caption: 'Расход', size: '120px' },
            { field: 'income', caption: 'Приход', size: '120px' },
            { field: 'balance', caption: 'Баланс', size: '120px' },
            { field: 'start_dt', caption: 'От', size: '120px', hidden: true },

            
            { field: 'discription_acc', caption: 'Комментарий', size: '120px', hidden: true},
            { field: 'name_user_owner', caption: 'Владелец', size: '100%', hidden: true}
        ],


        onSelect: function(event) {
            w2ui.layout_account.sizeTo('top', '50%');
            //Назначить фильтр по идентификатору для выбранного счета
            let activ = w2ui.layout_account.get('main').tabs.active;
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


config_accounts_selector = {
        name: 'config_accounts_selector',
        url  : {
            get    : '/acc/get_account_list',
        },
        method: 'POST',
        multiSearch: false,
        show : {
            toolbar: false,
            footer: false,
            
            toolbarReload   : false,
            toolbarColumns  : false,
            toolbarSearch   : false,
            columnHeaders   : false,
        },        
        columns: [
            { field: 'title_acc', caption: 'Наименование счета', size: '330px' }
        ],
    }
