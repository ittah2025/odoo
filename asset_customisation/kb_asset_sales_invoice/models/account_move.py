# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class AccountMove(models.Model):
    _inherit = "account.move"

    account_asset_asset_id = fields.Many2one('account.asset.asset', string="Asset")
