# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 OM Apps 
#    Email : omapps180@gmail.com
#################################################

{
    'name': 'Sale Purchase Invoice Excel',
    'category': 'Sales',
    'sequence':5,
    'version': '16.0.1.0',
    'summary': "Plugin will help to print Sale, purchase, invoice Excel and send excel using send by email. export excel, export sale excel, export purchase excel, export invoice excel, mass excel, all in one excel, daynemic excel, daynemic sale excel, daynemic purchase excel, daynemic invoice excel, generate excel, generate purchase excel, generate invoice excel, generate sale excel, xlxs, xlxs file, xlxs formate, xlxs report, export excel, excel sale purchase invoice, sale, purchase,invoice",
    'description': "Application print sale, purchase,invoice excel and send excel using send by email",
    'author': 'OM Apps',
    'website': '',
    'depends': ['sale_management','purchase','account','report_xlsx'],
    'license': 'AGPL-3',
    'data': [
        'views/res_config_settings_views.xml',
        'report/excel_report_views.xml',
        'data/mail_data.xml',
    ],
    'installable': True,
    'application': True,
    'images' : ['static/description/banner.png'],
    "price": 18,
    "currency": "EUR",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
