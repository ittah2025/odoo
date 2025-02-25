
# -*- coding: utf-8 -*-
{
    'name': 'Merge Chart of Accounts',
    'version': '16.0.0.1',
    'category': 'Accounting/Accounting',
    'summary': 'This module allows you to merge multiple charts of accounts into a single one.It provides a wizard to select source and target charts, and handles the merging process.And also provide a rollback feature for the merged accounts.',
    'description': """
        This module allows you to merge multiple charts of accounts into a single one.
        It provides a wizard to select source and target charts, and handles the merging process.
        And also provide a rollback feature for the merged accounts.
    """,
    'author': 'Prime Solution',
    'website': '',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_views.xml',
        'wizard/wizard_merge_account_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'price': 15,
    'currency': 'USD',
    'images': ['static/description/banner.png'],
}
