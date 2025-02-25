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
            'kb_reject_reason': self.name,
            'kb_reject_by': active_obj.env.user,
            'kb_rejection_date': datetime.now(),
        })

        return True

    def action_reject_order(self):
        active_obj = self.env[self.env.context.get('active_model')].browse(
            self.env.context.get('active_id'))
        if self.env.context.get('active_model') == 'kb.maintenance.form':
            active_obj.write({
                'kb_state': 'reject',
                'kb_reject_reason': self.name,
                'kb_reject_by': active_obj.env.user,
                'kb_rejection_date': datetime.now(),
            })
