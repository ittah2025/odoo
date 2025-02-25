from odoo import models, fields, api

class HistoryMergeAccount(models.Model):
    _name = 'history.merge.account'
    _description = 'History of Merged Accounts'
    
    name = fields.Char(string='Name', required=True)
    date = fields.Datetime(string='Merge Date', default=fields.Date.context_today)
    batch = fields.Integer(string='Batch')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    account_move_line_id = fields.Many2one('account.move.line', string='Account Move Line')
    source_account_id = fields.Many2one('account.account', string='Source Account')
    destination_account_id = fields.Many2one('account.account', string='Destination Account')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('history.merge.account') or '/'
        return super(HistoryMergeAccount, self).create(vals)
