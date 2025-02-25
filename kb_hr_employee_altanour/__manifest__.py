# 
{
    'name': 'Hr employee Al tanor',
    'version': '1.0.0.0',
    'category': 'Extra Tools',
    'author': 'Knowledge Bonds',
    'sequence': -100,
    'summary': 'count Service Reward ',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
      'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/kb_hr_altanour_data.xml',
        'views/hr_employee_view.xml',
 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
