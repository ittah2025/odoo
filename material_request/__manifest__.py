# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Issue Request',
    'version' : '1.0',
    'summary': '',
    'author':'Rawan Mohieldeen',
    'description': """Create Material Request by user the approved by DM. After that the invetory user can decide to issue this items from the stock or create the approved""",
    'depends' : ['base_setup','project','product','stock','sale_management','account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/material_request_views.xml',
    ],

    'installable': True,
    'application': True,

}
