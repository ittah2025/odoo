{
    'name': 'KB ID Card Form',
    'version': '16.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'HR',
    'summary': 'kb ID Card Form',
    'description': """Customise kb ID Card Form""",
    'depends': [
            'hr',
            'hr_contract',
               ],
    'data': [
        'security/ir.model.access.csv',
        'views/kb_hr_employee_view.xml',
        'views/kb_id_card_view.xml',

      ],
    'images': ['/static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}