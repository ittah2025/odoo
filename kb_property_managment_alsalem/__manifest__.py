{
    "name": "Property Managment Alsalem",
    "author": "Knowledge Bonds",
    "license": "OPL-1",
    "website": "https://www.rawabt.sa",
    "support": "info@knowledge-bonds.com",
    "category": "Extra Tools",
    'sequence': -240,
    # "summary": "Restrict To Change Unit Price, Extra Access Rights In Unit Price, Read Only Unit Price,Unit Price Management Module, Restrict To Change Unit Price, Unit Price Extra Access Rights,Read Only Unit Price, Product Unit Price Limitation Odoo",
    # "description": """Do you want to manage the unit price? The manager can set the unit price and everyone can't change the unit price. This module provides read-only access to a particular salesperson for which you don' want to allow them to edit the unit price in the product. """,
    "version": "14.0.1",
    "depends": ["sale_management","hr","mail","base",'account'],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/action_create_invoice.xml',
        'views/contract_view.xml',
        'views/apartments.xml',
        'views/property_view.xml',
        'views/maintenance_view.xml',
        'views/room_view.xml',
        'views/transportation.xml',
        'views/menuitem.xml', 
        'wizard/summary_report_wizard.xml',
        'wizard/payment_report_wizard.xml',
        'wizard/all_payment.xml',
        'wizard/late_payment.xml',
        'wizard/report_details.xml',
        # 'wizard/report.xml',
        'wizard/profit_report_wizard.xml',
        'wizard/profit_report.xml',

        

     
    ],
    'images': ['static/description/icon.png'],    
    "auto_install": False,
    "installable": True,
    "price": 15,
    "currency": "SAR"
}
