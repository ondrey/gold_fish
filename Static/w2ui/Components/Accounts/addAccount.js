addAccount = {
    name: 'addAccount',
    url      : '/acc/add_account',
    fields: [
        { name: 'title_acc', type: 'text', required: true,
            html: { caption: 'Название счета', attr: 'size="40" maxlength="40"' }
        },
        { field: 'discription_acc',   type: 'textarea',
            html: { caption: 'Описание', attr: 'style="width: 300px; height: 90px"' }
        },
        { name: 'account_color', type: 'color',
            html: { caption: 'Цвет счета', attr: 'size="40" maxlength="40"' }
        },
        { field: 'is_public', type: 'checkbox',
            html: { caption: 'В общем доступе', attr: 'style="width: auto;"' }
        },
    ],
    actions: {
        Reset: function () {
            this.clear();
        },
        Save: function () {
            var errors = this.validate();
            if (errors.length > 0) return;

            if (this.recid == 0) {
                this.save(this.record);
                this.clear();
            } else {
                w2ui.config_accounts.set(this.recid, this.record);
                w2ui.config_accounts.selectNone();
                this.clear();
            }
        }
    }
}
