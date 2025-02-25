# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    name2 = fields.Char(string="Name (Second Lang)")
    street12 = fields.Char(string="Street1 (Second Lang)")
    street22 = fields.Char(string="Street2 (Second Lang)")
    city2 = fields.Char(string="City (Second Lang)")
    country2 = fields.Char(string="Country (Second Lang)")




