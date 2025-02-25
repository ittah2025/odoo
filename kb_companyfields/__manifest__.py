# -*- coding: utf-8 -*-

{
    'name': 'KB company fields ',
    'version': '15.0.0.1',
    'category': 'Other',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'company': 'Knowledge Bonds',
    'license': 'AGPL-3',


    'depends': ['base', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/companyfields.xml',
        ],



    'installable': True,
    'auto_install': False,
    'application': False,
}

