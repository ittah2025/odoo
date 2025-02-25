# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Created By Mujtaba
    kb_supplier = fields.Char(string="Supplier", tracking=True)




