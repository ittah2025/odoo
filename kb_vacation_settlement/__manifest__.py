# 
{
    'name': 'vacation settlement report',
    'version': '1.0.0.0',
    'category': 'Extra Tools',
    'author': 'Knowledge Bonds',
    'sequence': -100,
    'summary': ' vacation settlement report ',
    'description': """
        vacation settlement report
       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
        'hr',
        'multi_branch_base',
        'ohrms_loan',
        'hr_holidays',
        'hr_contract',
        'hr_vacation_mngmt_(update)',
        'kb_hr_wage',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/vacation_settlement_view.xml',
        'views/hr_employees_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_timeoff_view.xml',
        'report/vacation_settlement_report.xml',
 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
