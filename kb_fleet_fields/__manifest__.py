{
    'name': 'Car fleet fields',
    'version': '1.0.0',
    'category': 'fleet',
    'summary': "Car fleet fields",
    'description': """Car fleet fields""",
    'sequence': '10',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','account',],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_new_field.xml',
        'views/fleet_add_vehicle.xml',
        'reports/vehicle_print.xml',
       


        
        
    ],

    'assets': {
    'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },

    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
