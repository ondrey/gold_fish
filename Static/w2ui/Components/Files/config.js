config_files = {
    name: 'config_files',
    // url: {
    //   get: '/operations/get_records',
    //   remove: '/operations/del_record'
    // },
    method: 'POST',
    autoLoad: false,
    
    limit: 50,
    show: {
        toolbar: true,
        footer: true,
        toolbarDelete: true,
        toolbarAdd: true
    },  

    columns: [
        { field: 'name_file', caption: 'Наименование файла', size:"150"},  
        { field: 'link_file', caption: 'Ссылка на файл', size:"150"},  
        { field: 'date_file', caption: 'Дата регистрации', size:"90"},  
        { field: 'access_file', caption: 'Открытый доступ', size:"90"}
    ],   
    
    onAdd: function(event) {
        // if (w2ui.config_accounts.getSelection().length == 0) {
        //     w2ui.layout_account.message('preview', {
        //         width: 300,
        //         height: 150,
        //         body: '<div class="w2ui-centered">Нужно выбрать счет</div>',
        //         buttons: '<button class="w2ui-btn" onclick="w2ui.layout_account.message(\'preview\')">Хорошо</button>'
        //     })

        // return
        // };

        w2popup.open({
            style:    "padding:8px;",
            title:'Добавить файлы',
            showClose: true,
            width:500,
            height: 235,
            body    : '<div id="addFile"></div>',
            onOpen  : function (event) {
                event.onComplete = function () {
                    w2ui.addFileForm.clear();
                    $('#addFile').w2render('addFileForm');
                };
            },
            onToggle: function (event) {
                event.onComplete = function () {
                    $(w2ui.addFileForm.box).show();
                    w2ui.foo.resize();
                }
            }
        });

    },     
}

addFileForm = {
    name: 'addFileForm',
    style: "height:100%",
    url  : '/files/add',
    fields: [
        { name: 'files', type: 'file',
            html: { caption: 'Загрузка файла', attr: 'style="width:300px"'}
        },
        { name: 'name', type: 'text',
            html: {caption: 'Наименование', attr: 'size="45" maxlength="40"'},            
        },
        { name: 'public', type: 'checkbox',
            html: {caption: 'Доступен из вне'},            
        },                

    ],    

    actions: {
        Reset: function () { this.clear(); },
        Save: function () {
            // var errors = this.validate();
            // if (errors.length > 0) return;
            // let clear = this.clear;

            // this.record['type_op'] = 'AA'
            // this.record['amount_op'] = 0

            // this.save({
            //     'record': this.record
            //     }, 
            //     function(e){
            //         w2ui.config_operation.reload();                                        
            //         w2ui.addOper.clear();
            //         w2popup.close();
                    
            //     });
        }
    }
}
