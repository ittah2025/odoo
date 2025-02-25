from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountAccount(models.Model):
    _inherit = 'account.account'

    history_merge_account_ids = fields.One2many('history.merge.account', 'source_account_id', string='History Merge Accounts')

    def action_merge_accounts(self):
        if len(self) < 2:
            raise ValidationError("You must select at least two accounts to merge.")

        return {
            'name': 'Merge Accounts',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.merge.account',
            'view_mode': 'form',
            'res_id': self.env['wizard.merge.account'].create({
                'source_account_ids': self.ids,
                'destination_account_id': self.ids[0],}).id,
            'target': 'new',
        }


    def action_rollback_merge_accounts(self):
        '''
        This code is responsible for rolling back the merge of accounts. 
        It iterates through the accounts selected for rollback, and for each account, it retrieves the latest merge history. 
        It then finds all the merge history entries for the same batch as the latest one, and for each of those entries, 
        it updates the account_id field on the corresponding account move lines to the source account ID, and then deletes the merge history entry.
        '''
        for account in self:
            if not account.history_merge_account_ids:
                raise ValidationError("No merge history found for this account.")
            
            latest_history = account.history_merge_account_ids[-1]
            history_merges = account.history_merge_account_ids.filtered(lambda x: x.batch == latest_history.batch)
            
            for history_merge in history_merges:
                history_merge.account_move_line_id.write({
                    'account_id': history_merge.source_account_id.id
                })
                history_merge.unlink()