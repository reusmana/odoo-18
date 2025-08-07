{
    "name":"hospital management system",
    "author":"Reusmana Sujani",
    "license":"LGPL-3",
    "sequence": -1,
    "depends" : ['mail','product', 'account'],
    "data" : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'view/patient_views.xml',
        'view/patient_read_views.xml',
        'view/appointment_views.xml',
        'view/appointment_line_views.xml',
        'view/patient_tag_views.xml',
        'view/account_move_views.xml',
        'view/menu.xml',
    ],

    "application": True,
    'installable': True,
    "demo": [
    ],

}