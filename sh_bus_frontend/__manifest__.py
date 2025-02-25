# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Bus Booking Management-Frontend",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "15.0.4",

    "category": "Website",
    
    "license": "OPL-1",

    "summary": "Bus Booking Module, Bus Management, Reservation Management, Transport Management, Ticket Reservation, Bus Reservation, Transport Booking, Bus Booking Website, Bus Management Shop Odoo",

    "description": """Are you looking for a bus booking management system on odoo? Here it is. We build an application for bus management. In this application, we will provide features like Ticket Booking from Website, Bus Management, Ticket Booking (Backend), Route Management, Special Price for Special Route, Trip Management, Real-Time Check-In, and so on.""",

    'depends': [
        'sh_bus_backend',
        'website_sale'
    ],

    'data': [
        # 'views/assets.xml',
        'views/website_bus_booking.xml',
        'data/website_bus_booking.xml',


    ],
    
    'assets': {

        'web.assets_frontend': [

            "sh_bus_frontend/static/src/js/jquery.seat-charts.js",
            "sh_bus_frontend/static/src/css/jquery.seat-charts.css",
            "sh_bus_frontend/static/src/scss/busbooking.scss",
            "sh_bus_frontend/static/src/scss/owl.carousel.css",
            "sh_bus_frontend/static/src/scss/owl.theme.default.min.css",
            "sh_bus_frontend/static/src/js/seat_booking.js",
            "sh_bus_frontend/static/src/js/custom.js",
            "sh_bus_frontend/static/src/js/owl.carousel.js",
            # "https://code.jquery.com/ui/1.12.1/jquery-ui.js",
            
            
        ],

        # 'web.assets_qweb': [
        #     'sh_bus_frontend/static/src/xml/*.xml',
        # ],

    },
    
    'demo': [

    ],
    "images": ["static/description/background.png", ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 200,
    "currency": "EUR"
}
