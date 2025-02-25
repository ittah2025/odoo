# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    default_bank_fee_account_id = fields.Many2one('account.account',
                                                     string='Default Bank Fee Account', domain=[('deprecated', '=', False)])

    is_percentage_fee = fields.Boolean(string="Percentage Bank Fee")
    bank_fee_percentage = fields.Float(string="Bank Fees(%)")
    bank_fee = fields.Float(string="Bank Fee")


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_bank_fee = fields.Boolean(string="Bank Fee")


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _create_payment_vals_from_wizard(self):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        if not self.journal_id.is_percentage_fee:
            res.update({'bank_fee': self.journal_id.bank_fee})
        else:
            res.update({'bank_fee': self.amount * self.journal_id.bank_fee_percentage/100})

        return res