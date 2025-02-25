# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Payroll Reports XLSX&PDF',
    'version': '16.0..0.1',
    'category': 'Employees',
    'summary': "Employee Payslip XLSX and PDF Report",
    'description': """Employee Payslip XLSX and PDF Report""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Odoo Mates',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['hr', 'hr_payroll_community'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizards/wizard.xml',
        'report/report.xml',
        'report/report_template.xml',
        # 'views/contract_view.xml'

    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}