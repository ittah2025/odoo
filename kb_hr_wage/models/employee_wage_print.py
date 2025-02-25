from odoo import fields, models, api

# fields to print employee wage at the employee page
class EmployeeWage(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee Wage"

    currency_id = fields.Many2one('res.currency', related="company_id.currency_id")
    emp_wage = fields.Monetary(string='Monthly Wage', related='contract_ids.wage')