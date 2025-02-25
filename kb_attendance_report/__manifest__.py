# 
{
    'name': 'kb attendance report',
    'version': '16',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'kb_attendance_report',
    'description': "kb_attendance_report",
    'website': 'https://www.knowledge-bonds.com',
    'depends': ['hr_attendance'],


    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/attendance_template.xml',
        'wizard/attendace_wizard.xml',
        # 'views/hr_employee_inherit.xml',

 
        ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
