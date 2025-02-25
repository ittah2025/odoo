{
    'name': 'Badge ID Employee',
    'version': '16.0',
    'currency': 'SAR',
    'website': 'http://www.knowledge-bonds.com',
    'support': 'info@knowledge-bonds.com',
    'author': 'Knowledge Bonds',
    "depends": ['hr'],
    'license': 'OPL-1',
    'sequence': 20,
    'data': [
        'security/ir.model.access.csv',
        'data/kb_data.xml',
        'views/kb_hr_employee_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}