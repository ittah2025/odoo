from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    iqama_no = fields.Char(string="ID/Iqama No")
    acc_num = fields.Char(string="Account Number(IBAN)")
    bank_code = fields.Char(string="Bank Code")