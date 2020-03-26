edit_account = {
        name   : 'edit_account',
        fields : [
            { name: 'Наименование', type: 'text', required: true, column: 1},
            { name: 'Описание',  type: 'text', required: true, column: 1},
            { name: 'Общедоступный',   type: 'text'},
            { name: 'Уведомления на почту',   type: 'text'},
            { name: 'Реквизиты',   type: 'text'},
            { name: 'Владелец',   type: 'text'},
            { name: 'Дата создания',   type: 'text'}
        ],
        toolbar: {
            items: [
                { id: 'bt1', type: 'button', caption: 'Файлы', img: 'icon-folder' },
                { id: 'bt3', type: 'spacer' },

                { id: 'bt5', type: 'button', caption: 'Сохранить', icon: 'fa-star'}
            ],
            onClick: function (event) {
                if (event.target == 'bt4') w2ui.form.clear();
                if (event.target == 'bt5') w2ui.form.save();
            }
        }

    }