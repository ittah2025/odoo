# -*- coding: utf-8 -*-
{
    'name' : 'Sales/Invoice Report',
    'version' : '14.1.0',
    'summary': "Sales/Invoice Report v14",
    'sequence': 15,
    'description': """
                    Sales/Invoice Report
                    """,
    'category': 'Accounting/Accounting',
    "price": 10,
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'images': ['static/description/banner.gif'],
    'depends': ['account','sale','report_xlsx'],
    'data': [
             'security/ir.model.access.csv',
             'wizard/invoice_report_xlxs.xml',
             'wizard/sales_report_view.xml',
             'report/invoice_report.xml'
             ],
    'demo': [],
    'license': 'OPL-1',
    'qweb': ['static/src/xml/view.xml'],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
