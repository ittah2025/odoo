from odoo import api, fields, models,_

class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'