{
    "name":"hospital management system",
    "author":"Reusmana Sujani",
    "license":"LGPL-3",
    "sequence": -1,
    'category': 'Learning',
    "depends" : ['mail','product', 'account'],
    "data" : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/cron.xml',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'wizard/cancel_appointment_views.xml',
        'wizard/patient_report_views.xml',
        'view/patient_views.xml',
        'view/patient_read_views.xml',
        'view/appointment_views.xml',
        'view/appointment_line_views.xml',
        'view/patient_tag_views.xml',
        'view/operation_views.xml',
        'view/account_move_views.xml',
        'reports/ir_action_report_temp.xml',
        'reports/report.xml',
        'reports/template_report_patients.xml',
        'view/menu.xml',
        'view/res_config_settings_views.xml',
    ],

    'assets': {
    'web.assets_backend': [
        'hospital/static/src/js/my_widget.js',
    ],
},

    "application": True,
    'installable': True,
    "demo": [
    ],

}