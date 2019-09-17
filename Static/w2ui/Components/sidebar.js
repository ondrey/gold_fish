sidebar_config = {
        name: 'sidebar',
        flatButton: true,
        topHTML    : '<div style="height: 30px;" id="helpsidebar"></div>',
        bottomHTML : '<div style="background-color: #f7f7f7; padding: 8px; border-top: 1px solid #63acdd; color: #539ed7;"><i style="font-size: xx-large;float: inline-end;" class="fa fa-info-circle" aria-hidden="true"></i> <div id="bottomHTML"></div></div>',
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

          { id: 'balance', text: 'Группы', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'account', text: 'Счета', icon: 'fa fa-cc-visa' },
                       { id: 'operation', text: 'Операции', icon: 'fa fa-tasks' },
                       { id: 'cost_item', text: 'Статьи', icon: 'fa fa-pie-chart' },]
                     }
          ],
        onFlat: function (event) {
              if (event.goFlat) {
                w2ui.base_layout.get('left').size = 40;
              } else {
                w2ui.base_layout.get('left').size = 230;
              }
              w2ui.base_layout.resize();
            },

        onClick: function(event) {
          console.log(event);
            // Отображаем меню

            if (event.target == 'account') {
              w2ui.base_layout.content('main', w2ui.layout_account);
                w2ui.layout_account.content('main', w2ui.config_accounts);
                w2ui.layout_account.content('preview', w2ui.transact_grid);
            }

            if (event.target == 'trash') {
              w2ui.base_layout.content('main', w2ui.transact_grid);
            }

            if ('comment' in event.object)
              {$("#bottomHTML").html(event.object.comment) }
            else {$("#bottomHTML").html(event.object.text);}


        }
    }
