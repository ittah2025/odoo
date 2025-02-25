from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class PettyCash(models.Model):
    _name = "petty.cash"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_name'

    kb_name = fields.Char(string="Petty Cash Number", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    name = fields.Char(related='kb_name')
    kb_date = fields.Date(string="Date", default=fields.Date.context_today, readonly=True)
    kb_note = fields.Char(string="Note")
    kb_journal_id = fields.Many2one('account.journal', string="Journal")
    kb_move_id = fields.Many2one('account.move', string="Move")
    kb_total_amount = fields.Float(string="Total Amount", compute="_calc_kb_total_amount")
    kb_petty_cash_line_ids = fields.One2many('petty.cash.line', 'kb_petty_cash_id')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)


    note = fields.Char(string='')
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Application'
        if vals.get('kb_name', ('New')) == ('New'):
            vals['kb_name'] = self.env['ir.sequence'].next_by_code('seq_petty') or ('New')
        res = super(PettyCash, self).create(vals)
        return res
    

    @api.depends('kb_petty_cash_line_ids', 'kb_petty_cash_line_ids.kb_amount')
    def _calc_kb_total_amount(self):
        for rec in self:
            rec.kb_total_amount = sum(
                rec.kb_petty_cash_line_ids.mapped('kb_amount_taxed')) if rec.kb_petty_cash_line_ids else 0.0

    def action_create_entry(self):
        if not self.kb_journal_id:
            raise ValidationError("Please select a journal.")

        journal = self.kb_journal_id
        vals = {
            'journal_id': journal.id,
            'date': self.kb_date,
            'ref': self.kb_name,
            'line_ids': []
        }

        # Create entry lines for each petty cash line
        for line in self.kb_petty_cash_line_ids:
            product_account = line.kb_product_id.property_account_expense_id
            if not product_account:
                raise ValidationError("Product %s does not have an expense account." % line.kb_product_id.name)

            vals['line_ids'].append((0, 0, {
                'name': line.kb_product_id.name,
                'account_id': product_account.id,
                'credit': line.kb_amount_taxed,
                'debit': 0.0,
                'tax_ids': [(6, 0, line.kb_tax_ids.ids)],
            }))


        # Add a line for the total amount with the default account of the journal
        vals['line_ids'].append((0, 0, {
            'name': "Total Amount",
            'account_id': journal.default_account_id.id,
            'credit': 0.0,
            'debit': self.kb_total_amount,
        }))
        # Create the accounting entry
        move = self.env['account.move'].create(vals)

        # Update the petty cash with the created move
        self.write({'kb_move_id': move.id})


class PettyCashLine(models.Model):
    _name = "petty.cash.line"

    kb_product_id = fields.Many2one('product.product', string="Product")
    kb_amount = fields.Float(string="Amount")
    kb_date = fields.Date(string="Date")
    kb_note = fields.Char(string="Notes")
    kb_tax_ids = fields.Many2many(comodel_name="account.tax", string="Taxes")
    kb_petty_cash_id = fields.Many2one('petty.cash')
    kb_amount_taxed = fields.Float(string="Amount Taxed", compute="_compute_amount_taxed")

    @api.depends('kb_amount', 'kb_tax_ids', 'kb_tax_ids.amount')
    def _compute_amount_taxed(self):
        for line in self:
            taxes_amount = 0.0
            for tax in line.kb_tax_ids:
                taxes_amount += (line.kb_amount * tax.amount) / 100
            line.kb_amount_taxed = line.kb_amount + taxes_amount
