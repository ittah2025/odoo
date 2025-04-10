# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Inventory Ledger Report',
    'version': '15.0',
    'price': 149,
    #'price' : 126,
    'currency': 'EUR',
    'category': 'stock',
    'summary': """	
        Inventory Ledger Report / Stock Card
        date wise real time inventory calculation along with opening & closing. Stock ledger report helps user to get summary as well as detailed of each days inventory movemenents.
        stock movement report, stock rotation report, product movement, daily product movement, product opening closing, product opening, product closing,
        detailed product report, product detailed report, product summary report, date wise opening, date wise closing,
        date wise calculated opening stock and closing stock, product detailed,
        date wise detailed data for each movement,
        capture  all possible inventory movements and separately visible all IN transactions and OUT transactions in report. (Date wise / Summary)
		""",
    'website': 'https://www.setuconsulting.com',
    'support': 'support@setuconsulting.com',
    'description': """
        Inventory Ledger Report
        It’s necessary to know inventory movements each day with all possible movements for each product for each warehouse or company and it’s very difficult to manage.
        So we introduced a solution for that and built an Inventory Ledger Report where users can track each day's transactions or summary of all dates together with real calculated opening and closing. 
        This app helps you to track the inventory for specific periods or up to a certain date.
    """,
    'author': 'Setu Consulting Services Pvt. Ltd.',
    'license': 'OPL-1',
    'sequence': 25,
    'depends': ['stock','base'],
    'images': ['static/description/banner.gif'],
    'data': [
        'views/setu_inventory_ledger_report.xml',
        'security/ir.model.access.csv',
        'db_function/get_products_movements_for_inventory_ledger.sql',
        'db_function/get_products_opening_stock.sql',
        'db_function/get_stock_data.sql',
        'db_function/get_products_movements_for_inventory_ledger_cmpwise.sql',
    ],
    'application': True,
    #'live_test_url': 'http://95.111.225.133:5929/web/login',
    # 'pre_init_hook': 'pre_init',
}
