# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import date

class HrEmployeeIdCard(models.Model):
    _inherit = "hr.employee"

    bloodGroup = fields.Selection([
        ('A+', 'A+'), 
        ('A-', 'A-'), 
        ('B+', 'B+'), 
        ('B-', 'B-'),
        ('O+', 'O+'), 
        ('O-', 'O-'),  
        ('AB+', 'AB+'), 
        ('AB-', 'AB-')], string='Blood Group')

    
    # note = fields.Char()
    # @api.model
    # def create(self, vals):
    #     if not vals.get('note'):
    #         vals['note'] = 'New Employee'
    #     if vals.get('employeeId', ('New')) == ('New'):
    #         vals['employeeId'] = self.env['ir.sequence'].next_by_code(
    #             'hr.employee.seq') or ('New')
    #     res = super(HrEmployee, self).create(vals)
    #     return res

    
