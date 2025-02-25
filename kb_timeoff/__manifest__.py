# 
{
  'name': 'Al salem time off',
  'version': '1.0.0',
  'category': 'Extra Tools',
  'sequence': -100,
  'summary': 'Al salem time off',
  'description': """
      """,
  'website': 'https://www.knowledge-bonds.com',
  'depends': [
      'hr',
      'hr_holidays',
  ],
  'data': [
        'security/ir.model.access.csv',
        'views/hr_leave.xml',
        'views/menu.xml',
        'views/Extension.xml',
        'reports/ExtensionofExit.xml',
       

        ],
  'images': ['static/description/icon.png'],
  'demo': [],
  'installable': True,
  'license': 'LGPL-3',
  'auto_install': False,
  'qweb': [],
  'application': True,
}
