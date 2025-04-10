{
    'name': 'School Maintenance Orders',
    'version': '1.0.0',
    'summary': "School Maintenance Orders",
    'description': """School Maintenance Orders""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','account', 'hr'],
    'demo': [],
    'data': [
        'security/kb_security.xml',
        'security/ir.model.access.csv',
        'data/kb_data.xml',
        'wizard/kb_rejection_wizard_view.xml',
        'views/kb_maintenance_form_view.xml',
        'views/kb_menuitem.xml',
        'views/kb_building_info_view.xml',
        'views/kb_maintenance_type_view.xml',
        'views/rooms_view.xml',
        'wizard/report_template.xml',
        'wizard/report_view.xml',
        
    ],

    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
