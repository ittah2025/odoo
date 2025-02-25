# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime
from odoo.exceptions import  ValidationError
from odoo import _


class hrloan(models.Model):
    _inherit = "hr.loan"
 
    guarantee= fields.Many2one('hr.employee', string='Guarantee', required=False)
    money = fields.Float(string="How much does the employee have to pay?",compute="check_pay")


    def check_pay(self):
        contract = self.env['hr.loan'].search(['&',('employee_id.id','=',self.employee_id.id),('department_id.id', '=' ,self.department_id.id)])
        for rec in self:
            for record in contract:
                totalnotpaid=record.total_amount-record.total_paid_amount
                rec.money += totalnotpaid
        rec.money -= rec.loan_amount
           
    