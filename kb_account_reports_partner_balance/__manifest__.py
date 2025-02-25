# -*- coding: utf-8 -*-
{
    'name': 'Partner balance report',
    'version': '14.0',
    'summary': "Partner balance report",
    'sequence': 15,
    'description': """
                    Odoo Partner balance report
                    """,
    'category': 'Accounting',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_report_balance_view.xml',
        'reports/report_balance.xml',
        'reports/account_report_balance_template.xml',

             ],
    'demo': [],
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
