from email.policy import default
# from typing_extensions import Required
from odoo import api, fields, models , _
from datetime import date
from odoo.exceptions import UserError, ValidationError
import re
from odoo.tools.translate import _
from datetime import date, datetime


class StudentYearlyFees(models.Model):
    _name = "student.yearly.fees"
    _description = "Configure Yearly and trimesterly fees for students per grade"

    name = fields.Char("Name")
    year = fields.Many2one("academic_year" ,string="Year")
    grade = fields.Many2one("grade" ,string="Grade")
    total = fields.Float("Total Fees", required=True)
    t1 = fields.Float(string='T1', store=True)
    t2 = fields.Float(string='T2', store=True)
    t3 = fields.Float(string='T3', store=True)

    @api.onchange('total')
    def _compute_fields(self):
        for record in self:
            if record.total:
                po1 = record.total * 0.4
                po2 = record.total * 0.3
                po3 = record.total * 0.3
                record.t1 = po1
                record.t2 = po2
                record.t3 = po3
            else:
                record.t1 = 0
                record.t2 = 0
                record.t3 = 0