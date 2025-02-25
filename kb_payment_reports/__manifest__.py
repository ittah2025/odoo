# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'KB Payment Reports',
    'version': '15.0',
    'category': 'Accounts',
    'summary': "KB Payment Reports",
    'description': """KB Payment Reports""",
    'sequence': '10',
    'license': 'LGPL-3',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['account'],
    'demo': [],
    'data': [
        # 'report/report.xml',
        'views/account_payment.xml',
        'views/contract_view.xml',
        'report/payment_template.xml',

    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}