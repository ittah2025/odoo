from odoo import fields, models, api,_
from odoo.exceptions import UserError, ValidationError


# reasons to be added at the empployee payslip page (python fields)
class EmployeeWage(models.Model):
    _inherit = 'hr.payslip'
    _description = "Employee Salary Reason"

    sal_increase_reason = fields.Char(string='Salary Increase Reason')
    sal_deduct_reason = fields.Char(string='Salary Deduction Reason')
    wage_discount_value = fields.Float(string='Deduction Value')
    percentage_value_de = fields.Integer(string='Percentage Value')
    wage_inclease_value = fields.Float(string='Increase Value')
    department = fields.Many2one('hr.department', string='Department', required=True)
    check_way=fields.Boolean(string="Percentage deduction",default=False)

    @api.onchange("percentage_value_de")
    def grt_swich_deduct(self):
        wage=self.env['hr.contract'].search([('employee_id.id', '=', self.employee_id.id)],limit=0)
        # raise ValidationError(_(self.wage_discount_value))
        if self.check_way == True:
            self.wage_discount_value = wage.wage *(self.percentage_value_de/100)
