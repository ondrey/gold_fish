sidebar_config = {
        name: 'sidebar',
        flatButton: true,
        topHTML    : '<div style="height: 30px;"></div>',
        bottomHTML : '<div style="background-color: #eee; padding: 10px 5px; border-top: 1px solid silver">Куджима</div>',
        nodes: [
            { id: 'trash', text: 'Не сортированные', icon: 'fa fa-trash-o', count: 5 },
            { id: 'balance', text: 'Инструменты', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'account', text: 'Счета', icon: 'fa fa-cc-visa' },
                       { id: 'operation', text: 'Операции', icon: 'fa fa-tasks' }]
            }],
            onFlat: function (event) {
              if (event.goFlat) {
                w2ui.base_layout.get('left').size = 40;
              } else {
                w2ui.base_layout.get('left').size = 230;
              }
              w2ui.base_layout.resize();
            },


        onClick: function(event) {

            // Отображаем меню

            if (event.target == 'account') {
              w2ui.base_layout.content('main', w2ui.layout_account);
                w2ui.layout_account.content('main', w2ui.config_accounts);
                w2ui.layout_account.content('preview', w2ui.transact_grid);
            }

            if (event.target == 'trash') {
              w2ui.base_layout.content('main', w2ui.transact_grid);
            }

        }
    }
