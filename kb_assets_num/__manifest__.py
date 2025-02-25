{
    'name': 'Asset number sequance and barcode label',
    'version': '1.0.0',
    'sequence': -600,


    'website': 'https://www.knowledge-bonds.com',
    'depends': [
        'om_account_accountant',
    ],

    'data': [
        'views/kb_assetsNumview.xml',
        'data/kb_data.xml',
        'reports/barcode_label.xml',

            ],

    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}