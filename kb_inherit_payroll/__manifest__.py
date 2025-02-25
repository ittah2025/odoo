{
    'name': 'hr payslip worked days',
    'version': '1.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'HR',
    'summary': 'hr payslip worked days',
    'description': """hr payslip worked days""",
    'depends': [
            'hr',
            'hr_contract',
        'hr_payroll_community',

               ],
    'data': [
        'security/ir.model.access.csv',
        'views/kb_worked_days_inherit_view.xml',
        'views/kb_reasone_of_deduction.xml',
    ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
