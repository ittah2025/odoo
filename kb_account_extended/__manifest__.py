# -*- coding: utf-8 -*-
{
    'name': 'Accounting Extended',
    'version': '16.1',
    'summary': "KB Accounting Extended",
    'sequence': 15,
    'description': """
                    Accounting Extended
                    """,
    'category': 'Accounting',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'depends': ['account','sale_management'],
    'data': [
        'views/account_account_views.xml',
        'views/account_move_view.xml',

             ],
    'demo': [],
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
