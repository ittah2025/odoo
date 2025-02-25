# 
{
    'name': 'KB Employee Timeoff Report',
    'version': '15.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'employee_timeoff',
    'description': "employee_timeoff",
    'website': 'https://www.knowledge-bonds.com',
    'depends': ['hr','hr_holidays','hr_payroll_community','ohrms_loan_accounting','ohrms_loan',],


    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/kb_timeoff_view.xml',
        'wizard/employee_timeoff.xml',
        'wizard/timeoff.xml',

 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
