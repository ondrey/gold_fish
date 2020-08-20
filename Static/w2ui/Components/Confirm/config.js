layout_confirm = {
    name: 'layout_confirm',
    padding: 0,
    panels: [
      
      { type: 'main', size:'100%', content: '', resizable: true,    toolbar: {
        items: [
            { type: 'spacer' },
            { type: 'button',  id: 'item1', caption: 'Завершить транзакции', icon: 'fa fa-bolt', checked: true },]
        } },
      { type: 'top', size: 70, resizable: true, style:'text-align: center; padding: 25px;'}
    ],
    onRender(event){
        w2ui.transact_grid.show.selectColumn = true;
        w2ui.transact_grid_toolbar.hide("toggleAcc");
        w2ui.transact_grid.on('select', function(event){
                        
            let rec = w2ui.transact_grid.get(event.recid);
            w2ui.layout_confirm.content('top', rec.comment_trans);
        });
    }
  }