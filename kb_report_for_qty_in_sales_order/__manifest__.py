# -*- coding: utf-8 -*-
{
    'name': "kb_report_for_qty_in_sales_order",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mohamed0halim",
    'website': "linkedin.com/in/mo-halim",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'product', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_view.xml',
        'report/report_action_for_excel.xml',
        'report/report_with_details.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
}
