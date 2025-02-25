# -*- coding: utf-8 -*-

{
    'name': 'KB company document ',
    'version': '1.0.0.1',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'license': 'AGPL-3',


    'depends': ['base', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/company_doc_view.xml',
        'views/company_check_list_view.xml',],



    'installable': True,
    'auto_install': False,
    'application': False,
}
