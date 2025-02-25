# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime
from odoo.exceptions import  ValidationError,UserError
from odoo import _


class hrleave(models.Model):
    _inherit = "hr.leave"
    
    dayswithoutSalary = fields.Char( string='Day without Salary')
    # lastvacationfrom= fields.Date(string='Last Vacation date from')
    lastvacationto= fields.Char(string='Last Vacation date',compute="check_from_to")

    def check_from_to(self):
        VECTION = self.env['hr.leave'].search([('employee_ids.id','=',self.employee_id.id)], order='create_date desc', limit=2)
        for rec in self:
            for record in VECTION:
                if record.state == 'validate':
                    rec.lastvacationto =  "From "+ str(record.date_from)+ " To " +str(record.date_to)
                else:
                    rec.lastvacationto = "This is frist vacation"
    
   
       


class ExtensionofExit(models.Model):
    _name = 'extensionof.exit'
    _description = "Extension of Exit"

    name = fields.Many2one('hr.employee',string='Employee Name')
    nationality = fields.Many2one('res.country',string='Nationality')
    workin = fields.Char(string='Working in' )
    Date = fields.Date(string='To Date')
    exp = fields.Date(string='Exp of Residence')
    number = fields.Char(string="Number of Residence")

    @api.onchange('name')
    def check_name(self):
        cantoryeml = self.env['hr.employee'].search([("name","=",self.name.name)])
        for rec in self:
            for record in cantoryeml:
                if rec.name:
                    rec.nationality =record.country_id
                    rec.number =record.identification_id
                    rec.exp =record.Exp
                
            
    
       




