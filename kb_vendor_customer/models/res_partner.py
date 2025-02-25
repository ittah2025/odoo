# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Created By Mujtaba
    kb_vendor = fields.Boolean(string="Vendor", tracking=True)
    kb_customer = fields.Boolean(string="Customer", tracking=True)




