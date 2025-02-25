# -*- coding: utf-8 -*-

{
    'name': 'Driving License, Bank, Border Information',
    'version': '16.0.1.0.0',
    'summary': """Adding Bank Information And Driving License Fields In Employee Master""",
    'description': 'This module helps you to add more information in employee records.',
    'category': 'Generic Modules/Human Resources',
    'author': 'Knowledge Bonds',
    'company': 'Knowledge Bonds',
    'website': "https://www.knowledge-bonds.com",
    'depends': ['hr_employee_updation', 'hr_payroll_community'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
        # 'views/hr_contract_view.xml',
        'views/hr_contract_history.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
