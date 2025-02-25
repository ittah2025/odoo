{
    'name': 'kb customer parent',
    'version': '16.0.0',
    'category': 'Contacts',
    'summary': "kb_customer_parent",
    'description': """kb_customer_parent""",
    'sequence': '15',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail', 'sale_management'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/kb_res_partner_view.xml',
        

        
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
