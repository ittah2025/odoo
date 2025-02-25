{
    'name': 'Report for HR school',
    'version': '1.0.0',
    'sequence': -100,


    'website': 'https://www.knowledge-bonds.com',
    'depends': [
        'hr'
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_inherit.xml',
        'report/absence_report.xml',
        'report/accountability_report.xml',
        'report/discipline_report.xml',

    ],

    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}