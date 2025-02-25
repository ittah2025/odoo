# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "All in One Mobile Barcode/QRCode Scanner|Sale Order Mobile Barcode Scanner|Purchase Order Mobile Barcode Scanner|Invoice Mobile Barcode Scanner|Inventory Mobile Barcode Scanner|Bill Of Material Mobile Barcode Scanner",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.4",

    "category": "Extra Tools",

    "summary": "invoice mobile qrcode scanner bom mobile barcode All in One Mobile Barcode Scanner stock adjustment qrcode scan request for quotation mobile barcode scanner product mobile barcode warehouse mobile account mobile qrcode scanner purchase barcode Odoo Add Product on Sales by barcode scanner all barcode sale barcode purchase barcode invoice barcode bom barcode inventory barcode Scan product by Barcode Scanner scan barcode on purchase scan barcode on invoice scan barcode on sale order barcode report All in one mobile barcode QR code scanner barcode and qr code scanner widget mobile barcode mobile qr code mobile qrcode barcode scanner qr code scanner mobile qrcode scanner mobile barcode scanner mobile qrcode scanner",

    "description": """
Do you want to scan Barcode/QRCode in your mobile/tablet? Do your time wasting in odoo operations by manual product selection ? So here is the solutions this modules useful do quick operations of odoo mobile/tablet Barcode/QRCode scanner. You no need to select product and do one by one. scan it and you done! So be very quick in all operations of odoo in mobile/tablet and cheers!

 All In One Mobile Barcode Scanner For Sales, Purchase, Stock Adjustment, Invoice, Inventory, BOM Odoo.
 Inventory Mobile Barcode Scanner Odoo, Invoice Mobile Barcode Scanner Module, BOM Mobile Barcode Scanner Odoo, Stock Adjustment Mobile Barcode Scanner Odoo, Purchase Mobile Barcode Scanner Odoo, Sales Mobile Barcode Scanner Odoo.
All In One Mobile Barcode Scanner App,Package All in one Mobile barcode scanner,  Operations Of Sales, Purchase In Barcode Module, Invoice In Barcode, Inventory In Barcode, Bom In Barcode, Scrap Using Barcode Odoo.

Add products by barcode    
Add products using barcode    

sales mobile barcode scanner
so barcode scanner
so mobile barcode scanner
sale mobile barcode scanner

po mobile barcode scanner
purchase order mobile barcode scanner
purchase order barcode scanner
po barcode scanner
    
inventory mobile barcode scanner    
stock mobile barcode scanner
inventory barcode scanner
stock barcode scanner

inventory adjustment mobile barcode scanner
stock adjustment mobile barcode scanner
inventory adjustment barcode scanner
stock adjustment barcode scanner

invoice barcode scanner
bill barcode scanner
credit note barcode scanner
debit note barcode scanner
invoice barcode mobile scanner
bill barcode mobile scanner
credit note barcode mobile scanner
debit note barcode mobile scanner

    """,


    "depends": [
                # "mrp",
                "stock",
                "account",
                "purchase",
                "sale_management",
                "sh_product_qrcode_generator",
    ],

    "data": [

        "security/product_bm_security.xml",
        "security/ir.model.access.csv",
        "sh_product_barcode_mobile/views/res_config_settings_views.xml",
        "sh_product_barcode_mobile/wizard/sh_product_barcode_mobile_wizard.xml",

        "sh_sale_barcode_mobile/views/res_config_settings_views.xml",
        "sh_sale_barcode_mobile/views/sale_view.xml",

        "sh_purchase_barcode_mobile/views/res_config_settings_views.xml",
        "sh_purchase_barcode_mobile/views/purchase_view.xml",

        "sh_invoice_barcode_mobile/views/res_config_settings_views.xml",
        "sh_invoice_barcode_mobile/views/account_view.xml",

        # "sh_bom_barcode_mobile/views/res_config_settings_views.xml",
        # "sh_bom_barcode_mobile/views/mrp_view.xml",

        "sh_inventory_barcode_mobile/views/res_config_settings_views.xml",
        "sh_inventory_barcode_mobile/views/stock_view.xml",
        "sh_inventory_adjustment_barcode_mobile/views/stock_adjustment.xml",
        "sh_inventory_adjustment_barcode_mobile/views/res_config_settings_views.xml",

        # Product Custom Barcode MB
        "sh_product_custom_mb/views/product.xml",

        # Global Search Document
        "global_doc_search/views/res_config_settings.xml",

    ],

    "assets": {
        "web.assets_backend": [
            'sh_all_in_one_mbs/static/src/scss/sh_all_in_one_mbs.scss',
            # zxing js lib
            "sh_all_in_one_mbs/static/src/js/ZXing.js",
            # For play sound with notification.
            'sh_all_in_one_mbs/static/src/js/services/messaging_notification_handler_service.js',

            'sh_all_in_one_mbs/static/src/xml/sh_inventory_adjustment_barcode_mobile.xml',
            'sh_all_in_one_mbs/static/src/js/sh_inventory_adjustment_barcode_mobile.js',

            'sh_all_in_one_mbs/static/src/xml/global_doc_search/global_doc_search.xml',
            "sh_all_in_one_mbs/static/src/js/global_doc_search/global_doc_search.js",

            'sh_all_in_one_mbs/static/src/xml/search_bar/search_bar.xml',
            "sh_all_in_one_mbs/static/src/js/search_bar/search_bar.js",
        ],
        # 'web.assets_qweb': [
        #     'sh_all_in_one_mbs/static/src/xml/global_doc_search/global_doc_search.xml',
        #     'sh_all_in_one_mbs/static/src/xml/search_bar/search_bar.xml',
        #     'sh_all_in_one_mbs/static/src/xml/stock_adjustment.xml',
        # ]

    },



    'images': ['static/description/background.png', ],
    "installable": True,

    "application": True,
    "autoinstall": False,

    "price": 120,
    "currency": "EUR",
    "license": "OPL-1"
}
