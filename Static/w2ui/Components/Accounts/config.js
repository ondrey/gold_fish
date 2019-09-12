layout_account = {
  name: 'layout_account',
  padding: 0,
  //style: 'height: 100%; position: relative; width:100%;',
  panels: [
    { type: 'main', size: '30%',  content: 'main' },
    { type: 'preview', size:'70%', content: '7'}
  ]
}

config_accounts = {
        name: 'config_accounts',

        show: {
            toolbar: true,
            footer: false,
            toolbarAdd: true,
            toolbarDelete: true,
            toolbarSave: true,
            toolbarEdit: true,
            columnHeaders: false
        },
        columns: [
            { field: 'lname', caption: 'Last Name', size: '30%' },
            { field: 'fname', caption: 'First Name', size: '30%' },
            { field: 'email', caption: 'Email', size: '40%' },
            { field: 'sdate', caption: 'Start Date', size: '90px' }
        ],
        records: [
            { recid: 1, fname: 'John', lname: 'doe', email: 'jdoe@gmail.com', sdate: '4/3/2012', w2ui: { children: [] }},
            { recid: 2, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012',
                w2ui: {
                    children: [
                        { recid: 21, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 22, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012',
                            w2ui: {
                                children: [
                                    { recid: 221, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                                    { recid: 222, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012',
                                        w2ui: {
                                            children: [
                                                { recid: 2221, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                                                { recid: 2222, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                                                { recid: 2223, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                                                { recid: 2224, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' }
                                            ]
                                        }
                                    },
                                    { recid: 223, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                                    { recid: 224, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' }
                                ]
                            }
                        },
                        { recid: 23, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 24, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' }
                    ]
                }
            },
            { recid: 3, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012',
                w2ui: {
                    children: [
                        { recid: 11, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 12, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 13, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 14, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' }
                    ]
                }
            },
            { recid: 4, fname: 'Susan', lname: 'Ottie', email: 'jdoe@gmail.com', sdate: '4/3/2012', w2ui: { children: [] } },
            { recid: 5, fname: 'Kelly', lname: 'Silver', email: 'jdoe@gmail.com', sdate: '4/3/2012', w2ui: { children: [] } },
            { recid: 6, fname: 'Francis', lname: 'Gatos', email: 'jdoe@gmail.com', sdate: '4/3/2012',
                w2ui: {
                    children: [
                        { recid: 61, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 62, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 63, fname: 'Stuart', lname: 'Motzart', email: 'jdoe@gmail.com', sdate: '4/3/2012' },
                        { recid: 64, fname: 'Jin', lname: 'Franson', email: 'jdoe@gmail.com', sdate: '4/3/2012' }
                    ]
                }
            },
            { recid: 7, fname: 'Mark', lname: 'Welldo', email: 'jdoe@gmail.com', sdate: '4/3/2012', w2ui: { children: [] } },
            { recid: 8, fname: 'Thomas', lname: 'Bahh', email: 'jdoe@gmail.com', sdate: '4/3/2012', w2ui: { children: [] } }
        ]
    }
