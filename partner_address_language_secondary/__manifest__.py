# -*- coding: utf-8 -*-

{
    'name': 'Address Secondary Language',
    'version': '15.0.0.2',
    'summary': """Secondary language in the partner/customer/supplier form. Like address in Arabic/Spanish/Chinese/Dutch/Greek/Russian """,
    'description': """Secondary language in the partner/customer/supplier form. Like address in Arabic/Spanish/Chinese/Dutch/Greek/Russian """,
    'category': 'Base',
    'author': 'bisolv',
    'website': "",
    'license': 'AGPL-3',

    'price': 0,
    'currency': 'USD',

    'depends': ['base_setup'],

    'data': [
        'views/res_config_settings_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
