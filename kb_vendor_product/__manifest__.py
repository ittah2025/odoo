# -*- coding: utf-8 -*-

{
    'name': 'KB vendor ID',
    'version': '1.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'customer',
    'license': 'OPL-1',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['sale_management',
                'contacts',
                'om_account_accountant',
                'base',

                ],

    'data': [
        'security/ir.model.access.csv',
        'views/invoice_xpath.xml',
        'views/product_template_view.xml',
        'views/res_partner.xml',
        'views/account_move_view.xml',
        'views/kb_sale_order.xml',

        ],


    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 50,
    "currency": "USD",
}
