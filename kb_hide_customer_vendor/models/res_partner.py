# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Created By Mujtaba
    kb_customer = fields.Boolean(string="Is a Vendor?", tracking=True)
    kb_vendor = fields.Boolean(string="Is a Customer?", tracking=True)




