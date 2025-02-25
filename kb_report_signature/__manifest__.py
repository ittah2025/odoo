{
    'name': 'Confidentiality of the information',
    'version': '1.0.0',
    'sequence': -100,


    'website': 'https://www.knowledge-bonds.com',
    'depends': [
        'hr'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/employee_inherit.xml',
        'report/signature_employee.xml'

    ],

    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}