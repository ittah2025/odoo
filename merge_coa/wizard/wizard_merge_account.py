from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class WizardMergeAccount(models.TransientModel):
    _name = 'wizard.merge.account'
    _description = 'Wizard for Merging Accounts'

    source_account_ids = fields.Many2many('account.account', string='Source Account', required=True, readonly="True")
    destination_account_id = fields.Many2one('account.account', string='Destination Account', required=True, domain="[('id', 'in', source_account_ids)]")
    force = fields.Boolean(string='Force', help="Force the merging of accounts even if there are deprecated.", default=False )
    notes = fields.Text(string='Notes')
    start_date = fields.Date(string='Start Date')

    def action_merge_accounts(self):
        self.ensure_one()
        """
        Validate that all accounts have the same account_type
        """
        if len(set(self.source_account_ids.mapped('account_type'))) > 1:
            raise ValidationError("The selected accounts have different account types. Please select accounts with the same type.")

        """
        If the 'force' option is enabled, it iterates through the 'source_account_ids' and checks if each account is deprecated. If an account is deprecated, it sets the 'deprecated' flag to False and adds the account to the 'deprecated_accounts' list.
        This is done to ensure that the deprecated accounts are restored to an active state before the account merging process is executed.
        """
        deprecated_accounts = []
        if self.force:
            for account in self.source_account_ids:
                if account.deprecated: 
                    account.deprecated = False
                    deprecated_accounts.append(account)

        
        account_batches = self.action_get_source_account_batches()
        
        domain = [('account_id', 'in', self.source_account_ids.ids)]
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        move_lines = self.env['account.move.line'].search(domain)

        for line in move_lines:
            if line.account_id != self.destination_account_id:
                self.action_generate_history_merge_account(line, line.account_id, account_batches)
            line.write({'account_id': self.destination_account_id.id})
            

        """
        If the `force` option is enabled and there are any deprecated accounts in the `deprecated_accounts` list, this code will restore the `deprecated` flag to `True` for those accounts.
        """
        if self.force and deprecated_accounts:
            for account in deprecated_accounts:
                account.deprecated = True

        return {'type': 'ir.actions.act_window_close'}

    def action_get_source_account_batches(self):
        """
        Get the last batch number for each source account from History Merge Account model.
        """
        batches = {}
        for account in self.source_account_ids:
            last_history = self.env['history.merge.account'].search([
                ('source_account_id', '=', account.id)
            ], order='batch DESC', limit=1)
            
            batches[account.code] = last_history.batch + 1 if last_history else 1
            
        return batches

    def action_generate_history_merge_account(self, account_move_line, account, account_batches):
        self.env['history.merge.account'].create({
            'date': fields.Datetime.now(),
            'batch': account_batches[account.code],
            'user_id': self.env.user.id,
            'account_move_line_id': account_move_line.id,
            'source_account_id': account.id,
            'destination_account_id': self.destination_account_id.id,
            'company_id': self.env.company.id,
            'notes': self.notes,
        })