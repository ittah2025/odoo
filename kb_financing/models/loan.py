from odoo import api, fields, models, _


class FinanceLoan(models.Model):
    _name = "finance.loan"
    _rec_name = 'kb_name'

    kb_name = fields.Char(string="Loan ID", readonly=True, required=True, copy=False, default='New')
    kb_loan_number = fields.Char(string="Loan Number")
    kb_date = fields.Date(string="Date", default=fields.Date.context_today, readonly=True)
    kb_note = fields.Char(string="Note")
    kb_financing_amount = fields.Float(string="Financing Amount")
    kb_payment_amount = fields.Float(string="Payment Amount")
    num_of_installments = fields.Integer(string="Number Of Installment")
    kb_total_amount = fields.Float(string="Total Amount", compute="_calc_kb_total_amount")
    kb_finance_loan_line_ids = fields.One2many('finance.loan.line', 'kb_finance_loan_id')

    @api.model
    def create(self, vals):
        # make a seq to statement
        if vals.get('name', 'New') == 'New':
            vals['kb_name'] = self.env['ir.sequence'].next_by_code(
                'seq.loan') or 'New'
        result = super(FinanceLoan, self).create(vals)
        return result

    @api.depends('kb_finance_loan_line_ids', 'kb_finance_loan_line_ids.kb_amount')
    def _calc_kb_total_amount(self):
        for rec in self:
            rec.kb_total_amount = sum(
                rec.kb_finance_loan_line_ids.mapped('kb_amount')) if rec.kb_finance_loan_line_ids else 0.0


class FinanceLoanLine(models.Model):
    _name = "finance.loan.line"

    kb_amount = fields.Float(string="Amount")
    kb_interest = fields.Float(string="Interest")
    kb_month = fields.Char(string="Month")
    kb_year = fields.Char(string="Year")
    kb_finance_loan_id = fields.Many2one('finance.loan')
