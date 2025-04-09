from odoo import fields, models


class  DismissalCause(models.TransientModel):
    """ For rejection reason wizard """

    _name = "dismissal.cause"
    _description = "Dismissal Cause"

    reason = fields.Text(string='Remarks')
    reason_type_id=fields.Many2one('rejection.types', string="Reason Types")

    # reason_type=fields.Selection([
    #     ('applicaion_threshold', 'Your Application  does not meet academic threshold'),
    #     ('missed_deadline', 'Your application missed the deadline'),
    #     ('admission_over','Maximum Admisssion have taken'),
    #     ('company_letter','Parent Company Letter  not properly authenticated')])


    def cancel_state(self):

        active_id=self._context.get('active_id')

        student=self.env['student.student'].browse(active_id)

        student.state = 'cancel'


        # student.admission_done()=condition
        # return condition


   
