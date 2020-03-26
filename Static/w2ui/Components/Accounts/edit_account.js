edit_account = {
        name   : 'edit_account',
        fields : [
            { name: 'first_name', type: 'text', required: true },
            { name: 'last_name',  type: 'text', required: true },
            { name: 'comments',   type: 'text'}
        ],
        actions: {
            reset: function () {
                this.clear();
            },
            save: function () {
                this.save();
            }
        }
    }