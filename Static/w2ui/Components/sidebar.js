sidebar_config = {
        name: 'sidebar',
        flatButton: true,
        nodes: [
          { id: 'tools', text: 'Инструменты', img: 'icon-folder', expanded: true, group: true,
            nodes: [
              { id: 'trash', text: 'Не сортированные', icon: 'fa fa-trash-o', count: 5,
                comment:"Транзакции зарегистрированы через мобильную форму, имеют не заполненные поля."},

              { id: 'future', text: 'Скоро', icon: 'fa fa-calendar-check-o', count: 1
                ,comment:"Не подтвержденные транзакции, дата выполнения которых запланирована на ближайшие 7 дней."},

              { id: 'confirm', text: 'Подтверждение', icon: 'fa fa-check-square', count: 256
                ,comment:"Не подтвержденные транзакции у которых дата выполнения уже прошла."}
            ]
          },

          { id: 'balance', text: 'Справочники', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'account', text: 'Счета', icon: 'fa fa-cc-visa' },
                       { id: 'operation', text: 'Операции', icon: 'fa fa-tasks' },
                      ]
          },

          { id: 'report', text: 'Отчеты', img: 'icon-folder', expanded: true, group: true,
            nodes: [ 
              { id: 'graphRent', text: 'Эффективность', icon: 'fa fa-line-chart' },
            ]}
          ],

        onFlat: function (event) {
              if (event.goFlat) {
                w2ui.base_layout.get('left').size = 40;
              } else {
                w2ui.base_layout.get('left').size = 230;
              }
              w2ui.base_layout.resize();
            },

        onRender: function(event) {
                this.click('account');
                this.select('account');                
        },

        onClick: function(event) {

            // Отображаем меню
            if (event.target == 'account') {
              w2ui.base_layout.content('main', w2ui.layout_account);
              w2ui.layout_account.content('top', w2ui.config_accounts);
              w2ui.layout_account.content('main', w2ui.transact_grid);

            } else if (event.target == 'trash') {
              w2ui.base_layout.content('main', w2ui.transact_grid);

            } else if (event.target == 'future') {
              w2ui.base_layout.content('main', w2ui.transact_grid);

            } else if (event.target == 'confirm') {
              w2ui.base_layout.content('main', w2ui.transact_grid);

            } else if (event.target == 'operation') {
              w2ui.base_layout.content('main', w2ui.layout_operation);
                w2ui.layout_operation.content('main', w2ui.config_operation);
                w2ui.layout_operation.content('preview', w2ui.transact_grid);
            }

            // Действия совершаемые при каждой смене или обновлении текущего пункта меню.
              // Прячим дочернии справочники счетов
              w2ui.layout_account.sizeTo('top', '100%');

        }
    }
