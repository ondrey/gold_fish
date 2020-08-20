sidebar_config = {
        name: 'sidebar',
        flatButton: true,
        nodes: [
          // { id: 'tools', text: 'Инструменты', img: 'icon-folder', expanded: true, group: true,
          //   nodes: [
          //     { id: 'trash', text: 'Не сортированные', icon: 'fa fa-trash-o', count: 5,
          //       comment:"Транзакции зарегистрированы через мобильную форму, имеют не заполненные поля."},

          //     { id: 'future', text: 'Скоро', icon: 'fa fa-calendar-check-o', count: 1
          //       ,comment:"Не подтвержденные транзакции, дата выполнения которых запланирована на ближайшие 7 дней."},

          //     { id: 'confirm', text: 'Подтверждение', icon: 'fa fa-check-square', count: 256
          //       ,comment:"Не подтвержденные транзакции у которых дата выполнения уже прошла."}
          //   ]
          // },

          { id: 'balance', text: 'Справочники', img: 'icon-folder', expanded: true, group: true,
              nodes: [ 
                { id: 'account', text: 'Счета', icon: 'fa fa-cc-visa' },
                { id: 'operation', text: 'Операции', icon: 'fa fa-tasks' },
                { id: 'transactions', text: 'Транзакции', icon: 'fa fa-puzzle-piece' },
              ]
          },

          { id: 'report', text: 'Отчеты', img: 'icon-folder', expanded: true, group: true,
            nodes: [ 
              { id: 'xlsx', text: 'Экспортировать в xlsx', icon: 'fa fa-file-excel-o' },
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
            
            } else if (event.target == 'operation') {
              w2ui.base_layout.content('main', w2ui.layout_operation);
                w2ui.layout_operation.content('top', w2ui.config_operation);
                w2ui.layout_operation.content('main', w2ui.transact_grid);
            } else if (event.target == 'transactions') {
              w2ui.base_layout.content('main', w2ui.transact_grid);                
            }
            else if (event.target == 'xlsx') {
              w2ui.base_layout.content('main', '<a href="/xlsx/get_all_report" style="display: block;margin: 150px auto;background-color: #8ab54c;width: 239px;text-align: center;padding: 15px;border-radius: 6px;color: aliceblue;">Скачать файл <i class="fa fa-file-excel-o" aria-hidden="true"></i></a>');
              
            } 
            // Действия совершаемые при каждой смене или обновлении текущего пункта меню.
              // Прячим дочернии справочники счетов
              w2ui.layout_account.sizeTo('top', '100%');
              w2ui.layout_operation.sizeTo('top', '100%');
              w2ui.transact_grid.postData = {};
              w2ui.transact_grid.searchReset();
              w2ui.transact_grid.show.toolbar = true;
              w2ui.transact_grid.show.selectColumn = false;  
              w2ui.transact_grid_toolbar.set('menu_transact', { disabled: true});

        }
    }
