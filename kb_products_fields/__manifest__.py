{
    'name': 'kb products fields',
    'version': '1.0.0',
    'category': 'products',
    'summary': "products fields",
    'description': """products fields""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','account',],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/products_new_field.xml',
       


        
        
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
