# 
{
    'name': 'New Field in Fleet ',
    'version': '1.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'New Field in Fleet ',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
      'fleet',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/kb_fleet_new_field.xml',
        'views/kb_ir_attachment_field.xml',
        'views/data.xml',

 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
