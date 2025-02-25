# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name2 = fields.Char()
    # street2 = fields.Char()
    street12 = fields.Char()
    street22 = fields.Char()
    city2 = fields.Char()
    country2 = fields.Char()




