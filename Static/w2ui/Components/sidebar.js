sidebar_config = {
        name: 'sidebar',
        nodes: [
            { id: 'level-1', text: 'Групперовки', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'level-1-1', text: 'Статьи', icon: 'fa-home' },
                       { id: 'level-1-2', text: 'Счета', icon: 'fa-star' },
                       { id: 'level-1-3', text: 'Операции', icon: 'fa-star-empty' }
                     ]
            },
            { id: 'level-2', text: 'Дополнительно', img: 'icon-folder', expanded: true, group: true,
              nodes: [ { id: 'level-2-1', text: 'Справочники', img: 'icon-folder', count: 3,
                           nodes: [
                           { id: 'level-2-1-1', text: 'Счета', icon: 'fa-star-empty' },
                           { id: 'level-2-1-2', text: 'Статьи расхода', icon: 'fa-star-empty'},
                           { id: 'level-2-1-3', text: 'Пользователи', icon: 'fa-star-empty' },
                           { id: 'level-2-1-4', text: 'Подписка', icon: 'fa-star-empty' }
                       ]},
                       { id: 'level-2-2', text: 'Настройки', icon: 'fa-star-empty' },
                       { id: 'level-2-3', text: 'О программе', icon: 'fa-star-empty' }
                     ]
            }
        ]
    }
