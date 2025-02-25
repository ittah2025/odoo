# -*- coding: utf-8 -*-
{
    'name': "kb_absence_attendance_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'version': '16',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/templates.xml',
        'wizard/attendance_template.xml',
        'wizard/attendace_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
