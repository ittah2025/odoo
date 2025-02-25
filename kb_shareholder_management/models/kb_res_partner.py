# -*- coding: utf-8 -*-
from odoo import api, fields, models,_

class ResPartner(models.Model):
    _inherit = 'res.partner'

    kb_nationality = fields.Many2one('res.country', string='Nationality')
    kb_idNumber = fields.Char(string='ID Number')
    kb_source = fields.Char(string='Source')
    kb_issueDate = fields.Date(string='Issue Date')
    kb_buildingNumber = fields.Char(string='Building Number')

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', '|', ('name', operator, name), ('phone', operator, name), ('kb_idNumber', operator, name)]
    #         return self._search(domain + args, limit=limit, access_rights_uid = name_get_uid)

class SaleOrder(models.Model):
    _name = 'student'
    