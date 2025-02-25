# 
{
    'name': 'Draft salary report ',
    'version': '1.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'Draft salary report ',
    'description': """

       """,
    'website': 'https://www.knowledge-bonds.com',
    'depends': [
      'hr',
      'hr_payroll_community','report_xlsx'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/kb_salary_draft_report.xml',
        'wizard/kb_draft_salary_report_wizard_view.xml',
 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
