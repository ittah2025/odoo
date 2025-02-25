# 
{
    'name': 'Alsalembank',
    'version': '1.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': '',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
       'sale', 'partner_autocomplete','base','account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/salembanks.xml',
        'views/salembank2.xml',
        
 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
