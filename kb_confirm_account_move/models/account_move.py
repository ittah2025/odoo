

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.env.user.has_group('kb_confirm_account_move.group_confirm_move_post'):
            raise AccessError(_('You are not allowed to confirm journal entry.'))
        return super(AccountMove, self).action_post()
