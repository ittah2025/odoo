# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Created By Mujtaba
    kb_vendor_id = fields.Char(string="Vendor")
    kb_vendor_id2 = fields.Many2one('m2n_table', string="Products ID", tracking=True)

    # kb_partnr_m2n_id = fields.Many2one(string="Customer IDs", tracking=True)



class Partnerm2n(models.Model):
    _name = "m2n_table"

    # fields_ids = fields.Many2one('res.partner')

    name = fields.Char(string='Name', required=True)

