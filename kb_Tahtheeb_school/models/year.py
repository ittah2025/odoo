# -*- coding: utf-8 -*-
from odoo import api, fields, models


class year(models.Model):
    _name = "year"
    _table = "year"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Year Information"

    photo = fields.Binary(String='photo', help='Choose the student photo for the id card')

    studentID = fields.Char(string='Student Id', required=True, help='Enter Student id')

    first_name_en = fields.Char(string='First Name in English', required=True, help='Enter First Student Name in English')
    middle_name_en = fields.Char(string='Middle Name in English', help='Enter Middle Student Name in English', required=True)
    last_name_en = fields.Char(string='Last Name in English', help='Enter Last Student Name in English', required=True)

    first_name_ar = fields.Char(string='First Name in Arabic', required=True, help='Enter First Student Name in Arabic')
    middle_name_ar = fields.Char(string='Middle Name in Arabic', help='Enter Middle Student Name in Arabic', required=True)
    last_name_ar = fields.Char(string='Last Name in Arabic', help='Enter Last Student Name in Arabic', required=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, help='Choose the student gender')

    birthdayDate = fields.Date('Birthday Date', required=True)
    admissionDate = fields.Date('Admission Date', required=True)

    phone = fields.Char(string='Student Phone', help='Enter Student Phone', required=True)
    mobile = fields.Char(string='Student Mobile', help='Enter Student Mobile', required=True)
    email = fields.Char(string='Student Email', help='Enter Student Email', required=True)
    nationality = fields.Selection([
        ('saudi', 'Saudi'),
        ('non', 'Non'),
    ], required=True, help='Choose the student nationality')

    website = fields.Char(string='Website', help='Enter Student website')

  

    emergencyPhone = fields.Char(string='Emergency Phone', help='Enter Emergency Phone', required=True)
    emergencyMobile = fields.Char(string='Emergency Mobile', help='Enter Emergency Mobile', required=True)

    school_id = fields.Many2one('school', 'School', help='choose school', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('terminate', 'Terminate'),
        ('cancel', 'Cancel'),
        ('alumni', 'Alumni'),
    ], readonly=True, default="draft", help='Choose the student state')


