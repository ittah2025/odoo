{
    'name': 'kb_accidents',
    'version': '1.0.0',
    'category': 'fleet',
    'summary': "kb_accidents",
    'description': """kb_accidents""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','account',],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/accidents_fields.xml',

       


        
        
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
