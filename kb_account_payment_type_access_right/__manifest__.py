{
    'name': 'Kb Account Payment Type Access Right',
    'version': '16.0.0',
    'category': 'Accounting',
    'summary': "kb_account_payment_type_access_right",
    'description': """kb_account_payment_type_access_right""",
    'sequence': '15',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['om_account_accountant'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        
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
