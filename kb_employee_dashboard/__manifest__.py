# -*- coding: utf-8 -*-
{
    'name': 'KB Employee Dashboard ',
    'version': '1.0.0.1',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'license': 'AGPL-3',

    'depends': ['base', 'hr', 'hr_payroll_community', 'kb_hr_forms', 'hr_attendance','ohrms_loan','hr_resignation','project','kb_end_of_service','odoo_website_helpdesk'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_dashboard_action.xml',
        'reports/definition_of_salary.xml',
        'wizard/hr_defintion_views.xml',
        'wizard/kb_salary_definition_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kb_employee_dashboard/static/src/css/style.css',
            'kb_employee_dashboard/static/src/js/employee_dashboard.js',
            'kb_employee_dashboard/static/src/xml/employee_dashboard.xml',
        ],
    },
    'demo': [
        'demo/demo.xml',
    ],
}
