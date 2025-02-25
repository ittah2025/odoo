# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class kbHrEmployee(models.Model):
    _inherit = "hr.employee"

    kb_branchID = fields.Many2one("res.branch", string='Branch')
    to_branch = fields.Many2one("res.branch", string='To Branch Name', default=False)
    kb_teacher_job_description = fields.Char('Teacher job Description: ')
    kb_iban = fields.Char(string="IBAN")
    # first_contract_date = fields.Char(string="IBAN")
    contract_warning = fields.Char(string="IBAN")
    contracts_count = fields.Char(string="IBAN")
    calendar_mismatch = fields.Char(string="IBAN")
    contract_id = fields.Many2one(
        'hr.contract', string='Current Contract', groups="hr.group_hr_user",
        help='Current contract of the employee',
        readonly=True)

    nationality_name = fields.Char('الجنسية')
    experiance = fields.Char('الخبرة')

