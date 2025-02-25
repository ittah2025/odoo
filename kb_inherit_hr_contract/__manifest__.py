# 
{
    'name': 'kb hr contract',
    'version': '1.0.0',
    'author': 'Knowledge bonds',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': '',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
       'sale','base','account','hr_contract','hr'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
