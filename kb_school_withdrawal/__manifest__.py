# -*- coding: utf-8 -*-

{
    'name': 'School withdrawal',
    'version': '1.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'customer',
    'license': 'OPL-1',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['kb_Tahtheeb_school'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/school_withdrawal_view.xml',
        'views/web/parent_withdrawal_web_form.xml',
        'views/web/parent_withdrawal_web_form_result.xml',

        # 'wizard/action_wizard_view.xml',

        ],


    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 50,
    "currency": "USD",
}
