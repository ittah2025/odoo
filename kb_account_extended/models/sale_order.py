from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    CUSTOM_FIELD_STATES = {
        state: [('readonly', False)]
        for state in {'sale', 'done', 'cancel'}
    }
    date_order = fields.Datetime(
        string="Order Date",
        states=CUSTOM_FIELD_STATES,
        copy=False, required=True,
        help="Creation date of draft/sent orders,\nConfirmation date of "
             "confirmed orders.")