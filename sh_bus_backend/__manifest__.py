# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Bus Booking Management-Backend",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "15.0.2",

    "category": "Industries",

    "license": "OPL-1",

    "summary": "Bus Booking Module, Bus Management, Reservation Management, Transport Management, Ticket Reservation, Bus Reservation, Transport Booking Odoo",

    "description": """Are you looking for a bus booking management system on odoo? Here it is. We build an application for bus management. In this application, we will provide features like Bus Management, Ticket Booking, Route Management, Special Price for Special Route, Trip Management, Real-Time Check-In, and so on.""",

    'depends': [
        'sale_management',
        'account_fleet',
    ],

    'data': [

        'security/ir.model.access.csv',
        'security/sh_bus_backend_security.xml',
        'views/ticket.xml',
        'data/route_management_sequence.xml',
        'views/sale_order_view.xml',
        'views/account_move.xml',
        'views/bus_booking_wizard.xml',
        'views/sh_bus_backend.xml',
        'views/fleet_vehical_inherit.xml',
    ],

    'assets': {

        'web.assets_backend': [

            "sh_bus_backend/static/src/js/busboard.js",
            "sh_bus_backend/static/src/js/jquery.seat-charts.js",
            "sh_bus_backend/static/src/scss/booking.scss",
        ],

        'web.assets_qweb': [
            'sh_bus_backend/static/src/xml/*.xml',
        ],

    },

    'demo': [

    ],
    "images": ["static/description/background.png", ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 100,
    "currency": "EUR"
}
