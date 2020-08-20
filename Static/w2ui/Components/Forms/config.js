config_forms = {
    name: 'config_forms',
    url  : {
        get    : '/forms/get_list',
        remove : '/forms/del_record'
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
        { field: 'title_form', caption: 'Наименование формы', size: '330px'},
        { field: 'id_icon_form', caption: 'Логотип', size: '120px' },
        { field: 'color_icon_form', caption: 'Цвет текста', size: '120px' },
        { field: 'color_back_form', caption: 'Цвет фона', size: '120px' },
        { field: 'link_form', caption: 'Секретная ссылка', size: '120px'}
    ],


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
                    $('#editAcc').w2render('editAccount');
                };
            },
            
        });

     } 

}