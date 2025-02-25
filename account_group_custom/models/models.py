# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools


class AccountAccount(models.Model):
    _inherit = "account.account"

    # parent_id = fields.Many2one('account.account')
    fourth_group_id = fields.Many2one('account.account','Fourth Level') # 4 level
    third_group_id = fields.Many2one('account.account','Third Level') # Third level
    fourth_group_new = fields.Many2one('account.group','Level 4') # 4 level
    third_group_new = fields.Many2one('account.group','Level 3') # Third level
    sub_group = fields.Many2one('account.group','Second Level') #Second group
    Sub_sub_group = fields.Many2one('account.group','First Level') #Main group