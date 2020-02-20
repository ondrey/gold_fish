layout_account = {
  name: 'layout_account',
  padding: 0,
  panels: [
    { type: 'main', size: '30%',  content: 'main', resizable: true },
    { type: 'preview', size:'70%', content: '7', resizable: true}
  ]
}

add_form_account = { 
    header: 'Edit Record',
    name: 'add_form_account',
    fields: [
        { name: 'recid', type: 'text', html: { caption: 'ID', attr: 'size="10" readonly' } },
        { name: 'fname', type: 'text', required: true, html: { caption: 'First Name', attr: 'size="40" maxlength="40"' } },
        { name: 'lname', type: 'text', required: true, html: { caption: 'Last Name', attr: 'size="40" maxlength="40"' } },
        { name: 'email', type: 'email', html: { caption: 'Email', attr: 'size="30"' } },
        { name: 'sdate', type: 'date', html: { caption: 'Date', attr: 'size="10"' } }
    ],
    actions: {
        Reset: function () {
            this.clear();
        },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;
            if (this.recid == 0) {
                w2ui.grid.add($.extend(true, { recid: w2ui.grid.records.length + 1 }, this.record));
                w2ui.grid.selectNone();
                this.clear();
            } else {
                w2ui.grid.set(this.recid, this.record);
                w2ui.grid.selectNone();
                this.clear();
            }
        }
    }
}

config_accounts = {
        name: 'config_accounts',
        url  : {
            get    : '/acc/get_account_list',
            remove : '',
            save   : '/acc/add_account'
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
        // items: [
        //     { id: 'add', type: 'button', caption: 'Add Record', icon: 'w2ui-icon-plus' }
        // ],

        columns: [
            { field: 'title_acc', caption: 'Наименование счета/статьи', size: '330px' },

            { field: 'in', caption: 'Входящий', size: '120px' },
            { field: 'income', caption: 'Приход', size: '120px' },
            { field: 'cost', caption: 'Расход', size: '120px' },
            { field: 'out', caption: 'Исходящий', size: '120px' },
            { field: 'name_user_owner', caption: 'Владелец', size: '100%'},
        ],
        
        onAdd: function(event) {
            console.log(event)

            w2popup.open({
                title   : 'Редактирование',
                width   : 900,
                height  : 600,
                showMax : true,
                body    : '<div id="smain" style="position: absolute; left: 5px; top: 5px; right: 5px; bottom: 5px;"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {
                        $('#smain').w2form(w2ui.add_form_account)
                    };
                },
                onToggle: function (event) { 
                    event.onComplete = function () {
                        w2ui.layout.resize();
                    }
                }
            });

        }  
    }
