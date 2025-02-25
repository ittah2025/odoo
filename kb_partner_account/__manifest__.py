# -*- coding: utf-8 -*-
{
    'name': 'Account Partner by account',
    'version': '16.0.1',
    'summary': "Account Partner by account",
    'sequence': 15,
    'description': """
                    Odoo Account Partner by account
                    """,
    'category': 'Accounting',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',

        'reports/report_partner.xml',
        'reports/account_report_partner_template.xml',
        'wizard/account_report_partner_view.xml',

             ],
    'demo': [],
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
