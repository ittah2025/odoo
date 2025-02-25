# 
{
    'name': 'Smart button in project ',
    'version': '1.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'Smart button in project',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
      'project',
        'base',
        'mail',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/kb_smart_project.xml',

 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
