from odoo import api, fields, models, _


class KbAccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def _dynamic_choice(self):
        choices = [
            ('inbound', 'Receive'),
        ]
        if self.env.user.has_group('kb_account_payment_type_access_right.kb_group_can_make_payments'):
            choices += [('outbound', 'Send'), ]
        return choices

    payment_type = fields.Selection(selection=_dynamic_choice,
                                    string='Payment Type', default='inbound', required=True, tracking=True)
