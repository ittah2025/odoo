# -*- coding: utf-8 -*-
{
    'name': 'KB Internal transfer',
    'version': '17.0.0.0',
    'summary': "KB Internal transfer",
    'sequence': 15,
    'description': """
                    Odoo KB Internal transfer
                    """,
    'category': 'Accounting',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'depends': ['account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/kb_transfer_seq.xml',
        'views/kb_internal_transfer_views.xml',
             ],
    'demo': [],
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
