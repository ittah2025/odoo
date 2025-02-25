# -*- coding: utf-8 -*-

{
    'name': 'Bulk Invoices Payment',
    'summary': '',
    'description': '',
    'version': '1.0.0.1',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'license': 'AGPL-3',
    'depends': ['sale', 'account'],
    'data': [
              
        'security/ir.model.access.csv',
        'wizard/kb_upload_xlsx_view.xml',
        
    ],

    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 80,
    "currency": "USD"
}
