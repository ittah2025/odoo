from odoo import api, fields, models, _


class KbCustomerParentField(models.Model):
    _inherit = 'res.partner'


    kb_customer_category = fields.Many2one('customer_m2n', string="Customer Category")







