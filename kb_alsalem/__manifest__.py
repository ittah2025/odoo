# 
{
    'name': 'Al salem employee',
    'version': '1.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'Al salem employee',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
      'hr',
      'ohrms_loan',
      'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employees.xml',
        'views/hr_loan.xml',
 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
