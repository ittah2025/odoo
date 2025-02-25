{
    'name': 'kb alrajhi salary definition',
    'version': '16.0.0',
    'category': 'Contacts',
    'summary': "kb alrajhi salary definition",
    'description': """kb alrajhi salary definition""",
    'sequence': '25',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail',],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/definition_bank_salary.xml',
        'wizard/definition_bank_salary_template.xml',

       


        
        
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
