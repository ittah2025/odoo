{
    'name': 'KB Biometric Integration',
    'version': '16.0.0.1',
    'summary': """Handle Biometric Data""",
    'description': """This Module Handle Biometric Data And Move It To hr_Attendance""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Knowledge bonds',
    'company': 'Knowledge bonds',
    'website': "https://www.knowledge-bonds.com",
    'depends': [
        'base_setup',
        'hr_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_machine_view.xml',
        'data/move_data.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
