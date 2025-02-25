# -*- coding: utf-8 -*-
from email.policy import default
#from typing_extensions import Required
from odoo import api, fields, models, _
from datetime import date
import re
from odoo.exceptions import ValidationError
import logging


class school(models.Model):
    _name = "school"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "school"
    
    
    school_id = fields.Char(string='School ID', required=True,
                            copy=False, readonly=True, default=lambda self: ('New'))
    name = fields.Char(string='Name', required=True, translate=True, help='Enter the school name')
    license_No = fields.Char(sting="License Number" , required=True)
    cr = fields.Char(string='CR',  help='Enter the school registration id', required=True)
    vat = fields.Char(string='VAT',   help='Enter the school vat id', required=True)
    code = fields.Char(string='Code',   help='Enter the school code', required=True)

    Principal_name = fields.Many2one('teacher', string="Principal Name En", help='choose Principal')

    lang = fields.Selection([
        ('arabic', 'arabic'),
        ('english', 'english')
    ],  help='Choose the Language', required=True)
    min_age = fields.Char(string='Minimum Age',   help='Enter the min age of the students', required=True)
    max_age = fields.Char(string='Maximum Age',   help='Enter the max age of the students', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('both', 'Both Gender'),
    ],  help='Choose the students gender of the school', required=True)
    grade = fields.Selection([
        ('primary', 'Primary'),
        ('intermediate', 'Intermediate'),
        ('secondary', 'Secondary'),        
    ],  help='Choose the grade', required=True)
    note = fields.Text(string="Description")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    country_id = fields.Many2one('res.country', string='Country', required = True)
    street = fields.Char (string="Street", required=True)
    district = fields.Char (string="District", required=True)
    # building_number = fields.Char (string="Building Number", required=False)
    city = fields.Char (string="City", required=True)
    postal_code = fields.Char (string="Postal Code", required=True)
    extra_number = fields.Char (string="Extra Number", required=True)
    company_id = fields.Many2one('res.company', 'Company', ondelete="cascade",
                                 required=True, delegate=True,
                                 help='Company_id of the school')
    com_name = fields.Char('School Name', related='company_id.name',
                           store=True, help='School name')


    Gpa_out_of=fields.Selection([('out5', '5'),
        ('out4', '4'),], string='GPA out of')
    
    @api.model
    def create(self, vals):
        '''Inherited create method to assign company_id to school'''
        res = super(school, self).create(vals)
        main_company = self.env.ref('base.main_company')
        res.company_id.parent_id = main_company.id
        return res
        
        
        
    
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New School'
        if vals.get('school_id', ('New')) == ('New'):
            vals['school_id'] = self.env['ir.sequence'].next_by_code(
                'school') or ('New')
        res = super(school, self).create(vals)

        return res
        


class Subject(models.Model):
    _name = "subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "subject"

    name = fields.Char(string='name',  translate=True, help='Enter the subject name', required=True)
    code = fields.Char(string='Code',  help='Enter the subject code', required=True)

class Grade(models.Model):
    _name = "grade"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "grade"

    name = fields.Char(string='name',  translate=True, help='Enter the grade name', required=True)



    
