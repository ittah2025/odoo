# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    kb_custody_ids = fields.One2many('custody.details', 'kb_asset_id', compute="_calc_custody")
    kb_show_asset_in_custody = fields.Boolean(string="Show The Asset In Custody")

    @api.depends()
    def _calc_custody(self):
        for rec in self:
            custody_ids = self.env['custody.details'].search([('kb_asset_id', '=', rec.id)])
            if custody_ids:
                rec.kb_custody_ids = custody_ids.ids
            else:
                rec.kb_custody_ids = False
