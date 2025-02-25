# -*- coding: utf-8 -*-


from datetime import timedelta
from odoo import models, fields, _, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Driver License Information
    license_id = fields.Char(string='Driver License Id', required=False, help='Enter Driver License Id')
    license_release_date = fields.Date(string='Driver License Release Date', required=False, help='Enter Driver License Release Date')
    license_expiry_date = fields.Date(string='Driver License Expiry Date', required=False, help='Enter Driver License Expiry Date')
    license_attachment_id = fields.Many2many(
    'ir.attachment',
    'license_attachment_rel',
    'license_ref', 'attach_ref2',
    string="Attachment",
    help='You can attach the copy of driver license')

    # Bank Information
    bank_name = fields.Char(string='Bank Name', required=False, help='Enter Bank Name')
    bank_soft_code = fields.Char(string='Soft Code', required=False, help='Enter Soft Code')
    bank_account_number = fields.Char(string='Account Number', required=False, help='Enter Account Number')
    bank_iban_number = fields.Char(string='Iban Number', required=False, help='Enter Iban Number')

    # Employee Border Information
    border_number = fields.Char(string='Border Number', required=False, help='Enter Border Number')
    date_of_entry = fields.Date(string="Date of Entry", required=False, help='Enter Date of Entry')

    # Add extra value to certificat selection feild
    certificate = fields.Selection([
    ('high_school', 'High School'),
    ('diploma', 'Diploma'),
    ('graduate', 'Graduate'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('doctor', 'Doctor'),
    ('other', 'Other'),
    ], 'Certificate Level', default='other', groups="hr.group_hr_user", tracking=True)

