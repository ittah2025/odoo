from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class kbHrPayslip(models.Model):
    _inherit = 'hr.payslip'


    def action_payslip_waiting(self):
        for rec in self:
            rec.state = 'verify'

    def action_payslip_done(self):
        if not self.user_has_groups('kb_access_right_hr_payroll.group_kb_accounting'):
            raise ValidationError('You dont have access to confirm, please contact your administrator')
        else:
            return super(kbHrPayslip, self).action_payslip_done()
