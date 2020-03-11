layout_account = {
  name: 'layout_account',
  padding: 0,
  panels: [
    { type: 'main', size: '30%',  content: 'main', resizable: true },
    { type: 'preview', size:'70%', content: '7', resizable: true}
  ]
}

add_form_account = { 
    name: 'add_form_account',
    url      : '/acc/add_account',
    fields: [
        { name: 'title_acc', type: 'text', required: true, 
            html: { caption: 'Название счета', attr: 'size="40" maxlength="40"' } 
        },
        { field: 'discription_acc',   type: 'textarea', 
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"' } 
        },
        { name: 'account_color', type: 'color', 
            html: { caption: 'Цвет счета', attr: 'size="40" maxlength="40"' } 
        },        
        { field: 'is_public', type: 'checkbox',  
            html: { caption: 'В общем доступе', attr: 'style="width: auto;"' } 
        },
    ],
    actions: {
        Reset: function () {
            this.clear();
        },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            
            if (this.recid == 0) {
                this.save(this.record);
                this.clear();
            } else {
                w2ui.config_accounts.set(this.recid, this.record);
                w2ui.config_accounts.selectNone();
                this.clear();
            }
        }
    }
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
            toolbarEdit: true,
            columnHeaders: true
        },
        columns: [
            { field: 'title_acc', caption: 'Наименование счета', size: '330px' },

            { field: 'in', caption: 'Входящий', size: '120px', info: true },
            { field: 'income', caption: 'Приход', size: '120px' },
            { field: 'cost', caption: 'Расход', size: '120px' },
            { field: 'out', caption: 'Исходящий', size: '120px' },
            { field: 'discription_acc', caption: 'Комментарий', size: '120px', hidden: true},
            { field: 'name_user_owner', caption: 'Владелец', size: '100%'},
        ],
        
        onAdd: function(event) {
            console.log(event)

            w2popup.open({
                title   : 'Редактирование',               
                showMax : true,
                height  :330,
                body    : '<div id="smain"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {                        
                        $('#smain').w2render('add_form_account');
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
