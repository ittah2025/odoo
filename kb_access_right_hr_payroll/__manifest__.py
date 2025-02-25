# 
{
    'name': ' HR Payroll',
    'version': '16.0.0',
    'author': 'Knowledge bonds',
    'category': 'Extra Tools',
    'sequence': 1,
    'summary': '',
    'website': 'https://www.knowledge-bonds.com',
    'depends': ['account','hr','hr_payroll_community'],
    'data': [
        'security/kb_security.xml',
        'security/ir.model.access.csv',
        'views/kb_inherit_hr_payslip_view.xml',
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
