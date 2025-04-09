from odoo import fields, models


class ConditionalAcceptance(models.TransientModel):
    """ For conditional acceptance wizard """

    _name = "conditional.acceptance"
    _description = "Conditional Acceptance"

    reason = fields.Char(string='Acceptance Reason')
    description = fields.Text(string="Description")

    def acceptance_state(self):
        active_id = self._context.get('active_id')
        student = self.env['student.student'].browse(active_id)
        student.state = 'condition'
        student.write({'condition_accept': True,
                       'conditional_acceptance_reason': self.reason})
        condition = student.admission_done()
        return condition
