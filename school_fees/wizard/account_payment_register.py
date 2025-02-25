from odoo import models

class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"
    
    def action_create_payments(self):
        res = super(AccountPaymentRegister, self).action_create_payments()
        if self._context.get('active_model') == 'account.move':
                move_id = self.env["{}".format(self._context.get('active_model'))].browse([self._context.get('active_id')])
                if move_id.student_payslip_id:
                    move_id.student_payslip_id.state = "paid"
        return res                    
                    