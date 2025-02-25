# -*- coding: utf-8 -*-

{
    'name': 'KB Custom invoice',
    'version': '1.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'account',
    'license': 'OPL-1',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['account'],

    'data': [
        'views/kb_custom_invoice2.xml',
        # 'views/kb_custom_invoice_dotmatrix.xml',
        # 'views/kb_extend_sale_order.xml',
        ],


    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 25,
    "currency": "USD",
}
