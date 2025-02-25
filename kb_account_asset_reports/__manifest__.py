# -*- coding: utf-8 -*-
{
    'name': 'Asset Reports',
    'version': '14.0',
    'summary': "Accounting Asset Report",
    'sequence': 15,
    'description': """
                    Asset Report
                    """,
    'category': 'Accounting',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'depends': ['account', 'om_account_asset', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/asset_report_view.xml',
        'reports/report.xml',
        'reports/asset_report_template.xml',

             ],
    'demo': [],
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
