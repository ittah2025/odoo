{
    'name': 'kb Contract End Date View',
    'version': '16.0.0',
    'category': 'hr',
    'summary': "view end date in employee",
    'description': """Contract End Date""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','account',],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/kb_hr_employee_tree_end.xml',
       


        
        
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
