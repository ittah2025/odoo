from odoo import api, fields, tools, models, _
from datetime import datetime


class RejectionReasonWizard(models.TransientModel):
    _name = 'kb.reject.reason.wizard'
    _description = "Reject reason wizard"

    name = fields.Char(string="Reason", required=True)

    def action_reject_order(self):
        
        active_obj = self.env[self.env.context.get('active_model')].browse(
            self.env.context.get('active_id'))
        active_obj.write({
            'reject_reason': self.name,
            'reject_by': active_obj.env.user,
            'rejection_date': datetime.now(),
        })

        return True

    def action_reject_order(self):

        active_obj = self.env[self.env.context.get('active_model')].browse(
            self.env.context.get('active_id'))
        if self.env.context.get('active_model') == 'kb.customer.register.payment':
            active_obj.write({
                'kb_state': 'reject',
                'reject_reason': self.name,
                'reject_by': active_obj.env.user,
                'rejection_date': datetime.now(),
            })
            active_obj.env['bus.bus']._sendone(active_obj.user_id.partner_id, 'sh_notification_info',
                                               {'title': _('Notitification'),
                                                'message': 'Dear User!! Your payment has been rejected'
                                                })
        elif self.env.context.get('active_model') == 'kb.vender.register.payment':
            active_obj.write({
                'kb_state': 'reject',
                'reject_reason': self.name,
                'reject_by': active_obj.env.user,
                'rejection_date': datetime.now(),
            })
            active_obj.env['bus.bus']._sendone(active_obj.user_id.partner_id, 'sh_notification_info',
                                               {'title': _('Notitification'),
                                                'message': 'Dear User!! Your payment has been rejected'
                                                })