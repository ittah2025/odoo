# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _

class ResPartner(models.Model):

    _inherit = 'res.partner'

    kb_idNumber = fields.Char("ID Number")