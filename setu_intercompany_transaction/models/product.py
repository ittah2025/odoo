from odoo import models, fields, api, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        product.company_id = False
        return product
