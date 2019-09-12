sidebar_config = {
        name: 'sidebar',
        bottomHTML : '<div style="background-color: #eee; padding: 10px 5px; border-top: 1px solid silver">Куджима</div>',
        nodes: [
            { id: 'notify', text: 'Уведомления', icon: 'fa fa-bell', count: 15 },
            { id: 'trash', text: 'Не сортированные', icon: 'fa fa-trash-o', count: 5 },
            { id: 'balance', text: 'Инструменты', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'cost_item', text: 'Статьи', icon: 'fa fa-shopping-cart' },
                       { id: 'account', text: 'Счета', icon: 'fa fa-cc-visa' },
                       { id: 'operation', text: 'Операции', icon: 'fa fa-tasks' }
                     ]
            },
            { id: 'level-2', text: 'Дополнительно', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'level-2-1', text: 'Справочники', img: 'icon-folder',
                           nodes: [
                           { id: 'level-2-1-1', text: 'Счета', icon: 'fa fa-bars' }, //С возможностью выбора владельца
                           { id: 'level-2-1-2', text: 'Статьи расхода', icon: 'fa fa-bars'},
                           { id: 'level-2-1-3', text: 'Мои пользователи', icon: 'fa fa-bars' },
                       ]},
                       { id: 'subscribe', text: 'Подписка', icon: 'fa fa-check-square-o' }, //Пользователи, счета, статьи, операции
                       { id: 'settings', text: 'Настройки', icon: 'fa fa-cogs' },
                     ]
            }
        ],
        onClick: function(event) {

            // Отображаем меню

            if (event.target == 'account') {
              w2ui.base_layout.content('main', w2ui.layout_account);
                w2ui.layout_account.content('main', w2ui.config_accounts);
                w2ui.layout_account.content('preview', w2ui.transact_grid);
            }

            if (event.target == 'notify') {
              w2ui.base_layout.content('main', w2ui.notification_layout);
            }

        }
    }
