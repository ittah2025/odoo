# -*- coding: utf-8 -*-

from odoo import api, fields, models

# this is the wizard "structure" of change (deduct or increase)salary at payslip page
class SalaryDeductionWizard(models.TransientModel):
    _name = 'salary.deduction.wizard'
    _description = 'Salary Deduction Wizard'
    
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    change_type= fields.Selection([('increase','Increase'),('deduction','Deduction')], default="deduction")
    change_value = fields.Float(string='Value')
    increase_reason = fields.Char(string='Increase Reason')
    deduction_reason = fields.Char(string='Deduction Reason')

    # function to handle the salary change (increase or deduction) and assign reason
    def action_change_salary(self):
        if self.change_type == 'increase':
                self.employee_id.slip_ids.wage_inclease_value = self.change_value
                self.employee_id.slip_ids.sal_increase_reason = self.increase_reason 
        elif self.change_type == 'deduction':
                self.employee_id.slip_ids.wage_discount_value = self.change_value
                self.employee_id.slip_ids.sal_deduct_reason = self.deduction_reason