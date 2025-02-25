# -*- coding: utf-8 -*-
from odoo import api, fields, models

# Created By Mujtaba
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    kb_vendor_id = fields.Char(string="Vendor ID", tracking=True)
    kb_product_id = fields.One2many('product_partner','kb_product_ids', string="Product IDs", related="product_variant_id.kb_product_id")

class ProductProduct(models.Model):
    _inherit = 'product.product'

    kb_vendor_id = fields.Char(string="Vendor ID", tracking=True)
    kb_product_id = fields.One2many('product_partner', 'kb_product_ids', string="Product IDs")


class ProductPartner(models.Model):
    _name = "product_partner"
    _table = "product_partner"
    _rec_name = 'combination'

    kb_customer_id = fields.Many2one('m2n_table', string="Customer ID")
    kb_code = fields.Char(string="CODE", tracking=True)
    kb_product_ids = fields.Many2one('product.product', string="Product IDs")
    kb_product_idse = fields.Many2one('product.template', string="Product IDs")
    # kb_partnr_m2n_id = fields.Many2one('m2n_table', string="Customer IDs", tracking=True)

    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.depends('kb_customer_id', 'kb_code')
    def _compute_fields_combination(self):
        for recs in self:
            recs.combination = f"{recs.kb_customer_id.name} - {recs.kb_code}"



