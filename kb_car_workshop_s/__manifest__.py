{
    'name': 'Car Shop',
    'version': '1.0.0',
    'category': 'Account',
    'summary': "Car Shop",
    'description': """Car Shop""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','account','hr', 'fleet', 'kb_fleet_fields', 'kb_accidents'],
    'demo': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/orders.xml',
        'reports/report.xml',
        'reports/goods_trans_print.xml',
        'reports/damages_print.xml',
        'views/dameges_report.xml',
        'views/good_trans_rec.xml',
        # 'views/res_partner.xml',
        'wizards/wizardview.xml',
        'wizards/wizard_complete_view.xml',
        'views/employee_fileds.xml',
        
        'views/dashboard_companies_view.xml',
        



    ],

    'assets': {
    'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },

    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
