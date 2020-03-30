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
            { field: 'account', caption: 'Счет', size: '120px' },
            { field: 'icon', caption: 'Иконка', size: '120px' },
            { field: 'discript', caption: 'Описание', size: '120px' }
        ],

        onAdd: function(event) {

            w2popup.open({
                style:    "padding:8px;",
                title:'Новая категория <i id="iconPreview" style="color: dimgray;"></i>',
                showClose: true,
                width:550,
                height: 310,
                body    : '<div id="addCat"></div>',
                onOpen  : function (event) {
                    event.onComplete = function () {
                        $('#addCat').w2render('addCategories');
                    };
                },
                onToggle: function (event) {
                    event.onComplete = function () {
                        $(w2ui.add_form_categories.box).show();
                        w2ui.foo.resize();
                    }
                }
            });
 
         } 

    }