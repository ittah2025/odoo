# 
{
    'name': 'kb_end_of_service',
    'version': '16.0.0',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'kb_end_of_service with jornal ',
    'description': "kb_end_of_service",
    'website': 'https://www.knowledge-bonds.com',
    'depends': ['hr','hr_holidays','hr_payroll_community','ohrms_loan_accounting','ohrms_loan'],


    'data': [
        'security/ir.model.access.csv',
        'views/employee_info.xml',
        'Reports/end_of_service_calc.xml',
        'Reports/definition_of_salary.xml',
        'security/security.xml',
        'wizard/hr_defintion_views.xml',
        # 'wizard/kb_salary_definition_template.xml',

        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
