from odoo import models, fields,api
from datetime import date
from xml.dom import ValidationErr
from datetime import datetime, timedelta


class kb_innherit_worked_days(models.Model):
    _inherit = "hr.payslip.worked_days"

    kb_discount_by_days = fields.Float(string='Discount based on days', help='Discount based on days')
    kb_discount_by_amount = fields.Float(string='Discount based on amount',help='Discount based on amount')
    kb_deduction_from_one_day_salary = fields.Float(string='Deduction from one day salary',help='Deduction from one day salary')
    kb_fingerprint_discount = fields.Float(string='Fingerprint deduction',help='Fingerprint deduction')
    kb_reason_of_deduction = fields.Many2one('kb_reason_of_deduction',string='Reason of deduction',help='Reason of deduction')


class kb_reason_of_deduction(models.Model):
    _name = "kb_reason_of_deduction"
    _rec_name = "kb_reason_of_deduction"

    kb_reason_of_deduction = fields.Char("Reason of deduction")
