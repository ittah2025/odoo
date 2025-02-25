# 
{
    'name': 'Experience Certificate',
    'version': '16.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'description': "Experience Certificate",
    'website': 'https://www.knowledge-bonds.com',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/kb_hr_experience_certificate_wizard_view.xml',
        'wizard/kb_hr_experience_certificate_report.xml',
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
