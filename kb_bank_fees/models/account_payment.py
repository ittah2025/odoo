# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    bank_fee = fields.Float(string="Bank Fees")

    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the temporary liquidity account.
        - The lines using the counterpart account.
        - The lines being the write-off lines.
        :return: (liquidity_lines, counterpart_lines, writeoff_lines)
        '''
        self.ensure_one()

        liquidity_lines = self.env['account.move.line']
        counterpart_lines = self.env['account.move.line']
        writeoff_lines = self.env['account.move.line']


        for line in self.move_id.line_ids.filtered(lambda x: not x.is_bank_fee):
            if line.account_id in (
                    self.journal_id.default_account_id,
                    # self.journal_id.payment_debit_account_id,
                    # self.journal_id.payment_credit_account_id,
            ):
                liquidity_lines += line
            elif line.account_id.account_type in ('asset_receivable', 'liability_payable') or line.partner_id == line.company_id.partner_id:
                counterpart_lines += line
            else:
                writeoff_lines += line

        return liquidity_lines, counterpart_lines, writeoff_lines

    def apply_bank_fee(self):
        if self.journal_id.type == 'bank':
            if not self.journal_id.is_percentage_fee:
                bank_fees = [{
                    'account_id': self.journal_id.default_account_id.id,
                    'partner_id': self.payment_type in ('inbound', 'outbound') and self.env['res.partner']._find_accounting_partner(self.partner_id).id or False,
                    'name': self.ref,
                    'credit': self.journal_id.bank_fee,
                    'company_id': self.company_id.id,
                    'is_bank_fee': True
                }, {
                    'account_id': self.journal_id.default_bank_fee_account_id.id,
                    'partner_id': self.payment_type in ('inbound', 'outbound') and self.env['res.partner']._find_accounting_partner(self.partner_id).id or False,
                    'name': _("Vendor Payment: %s" % self.ref),
                    'debit': self.journal_id.bank_fee,
                    'company_id': self.company_id.id,
                    'is_bank_fee': True
                }]
                return bank_fees
            else:
                bank_fees = [{
                    'account_id': self.journal_id.default_account_id.id,
                    'partner_id': self.payment_type in ('inbound', 'outbound') and self.env[
                        'res.partner']._find_accounting_partner(self.partner_id).id or False,
                    'name': self.ref,
                    'credit': self.amount * self.journal_id.bank_fee_percentage/100,
                    'company_id': self.company_id.id,
                    'is_bank_fee': True
                }, {
                    'account_id': self.journal_id.default_bank_fee_account_id.id,
                    'partner_id': self.payment_type in ('inbound', 'outbound') and self.env[
                        'res.partner']._find_accounting_partner(self.partner_id).id or False,
                    'name': _("Vendor Payment: %s" % self.ref),
                    'debit': self.amount * self.journal_id.bank_fee_percentage/100,
                    'company_id': self.company_id.id,
                    'is_bank_fee': True
                }]
                return bank_fees

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        if not self.journal_id.is_percentage_fee:
            if self.journal_id.bank_fee > 0.0 and self.journal_id.default_bank_fee_account_id:
                res += self.apply_bank_fee()
        else:
            if self.journal_id.bank_fee_percentage > 0.0 and self.journal_id.default_bank_fee_account_id:
                res += self.apply_bank_fee()
        return res
