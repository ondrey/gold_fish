transact_grid = {
        name: 'transact_grid',
        show: {
            toolbar: true,
            footer: true,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarSave: true,
            toolbarEdit: true
        },
        method: 'GET', // need this to avoid 412 error on Safari
        columns: [
            { field: 'fname', caption: 'First Name', size: '30%' },
            { field: 'lname', caption: 'Last Name', size: '30%' },
            { field: 'email', caption: 'Email', size: '40%' },
            { field: 'sdate', caption: 'Start Date', size: '120px' }
        ]
    }
