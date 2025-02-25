# -*- coding: utf-8 -*-

{
    'name': 'KB hide vendor or customer',
    'version': '1.0.0',
    'description': 'Hide vendor in Purchase and Bills || Hide Customer in Quation ',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'customer',
    'license': 'OPL-1',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['sale_management','account','purchase'],

    'data': [
        'views/res_partner.xml',
        'views/account_move1.xml',
        'views/sale_order1.xml',
        'views/purchase_order1.xml',
        ],


    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 50,
    "currency": "USD",
}
