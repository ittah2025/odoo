# -*- coding: utf-8 -*-

{
    'name': 'KB Delivery Note ',
    'version': '1.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'customer',
    'license': 'OPL-1',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/delivery_note_print.xml',
        ],


    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 50,
    "currency": "USD",
}
