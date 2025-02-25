# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date, formatLang


class AccountPayment(models.Model):
    _inherit = "account.payment"

    purchase_order = fields.Many2one('purchase.order','PO Referance',domain="[('partner_id','=',partner_id)]")