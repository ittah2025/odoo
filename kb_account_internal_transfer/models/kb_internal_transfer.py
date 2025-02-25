from odoo import api, fields, models,_
from datetime import datetime

class kbInternalTransfer(models.Model):
    _name = "kb_internal_transfer"
    _rec_name = 'kb_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    kb_number = fields.Integer(string="Number", readonly=True, default=1)
    kb_name = fields.Char(string="Internal ID", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    kb_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer/Vendor",
        store=True, readonly=False, ondelete='restrict',
        domain="['|', ('parent_id','=', False), ('is_company','=', True)]",
        tracking=True,
        check_company=True)

    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        compute='_compute_currency_id', store=True, readonly=False, precompute=True,
        help="The payment's currency.")
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id)]",
        check_company=True,
    )

    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id),('id', '!=', journal_id)]",
        check_company=True,
    )
    payment_reference = fields.Char(string="Payment Reference", copy=False, tracking=True,
                                    help="Reference of the document used to issue this payment. Eg. check number, file name, etc.")

    kb_date = fields.Date(string="Date", default=datetime.today())

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], readonly=True, default="draft")
    
    kb_account_move = fields.Many2one('account.move',string="Journal Item")

    @api.depends('journal_id')
    def _compute_currency_id(self):
        for pay in self:
            pay.currency_id = pay.journal_id.currency_id or pay.journal_id.company_id.currency_id

    # Make sequence for internal Transfer orders
    @api.model
    def create(self, vals):
        # make a seq to Transfer
        if vals.get('name', 'New') == 'New':
            vals['kb_name'] = self.env['ir.sequence'].next_by_code(
                'seq.transfer') or 'New'
        result = super(kbInternalTransfer, self).create(vals)
        return result


    def action_confirm(self):
        for rec in self:
            rec.state='confirm'

    def action_done(self):
        for rec in self:
            vals = {
                'ref': rec.payment_reference,
                'date': rec.kb_date,
                'journal_id': rec.journal_id.id,
                'kbInternalTransfer': rec.id,
                'line_ids': [(0, 0, {
                    'name': rec.payment_reference,
                    'credit': rec.amount,
                    'account_id': rec.journal_id.default_account_id.id,
                    'partner_id': rec.kb_partner_id.id,
                }), (0, 0, {
                    'name': rec.payment_reference,
                    'debit': rec.amount,
                    'account_id': rec.destination_journal_id.default_account_id.id,
                    'partner_id': rec.kb_partner_id.id,
                })]
            }
            account_move = self.env['account.move'].create(vals)
            rec.kb_account_move = account_move.id
            if account_move:
                rec.state='done'
                account_move.action_post()


    def action_cancel(self):
        for rec in self:
            rec.state='cancel'

    # int_count = fields.Integer(compute='compute_count')
    
    # def compute_count(self):
    #     for record in self:
    #         record.int_count = self.env['account.move'].search_count(
    #             [('kbInternalTransfer', '=', self.id)])
    # def get_move(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Account Move',
    #         'view_mode': 'tree,form',
    #         'res_model': 'account.move',
    #         'domain': [('kbInternalTransfer', '=', self.id)],
    #         'context': "{'create': False}"
    #     }
        
        
class AccountMove(models.Model):
    _inherit = 'account.move'

    kbInternalTransfer = fields.Many2one('kb_internal_transfer')
