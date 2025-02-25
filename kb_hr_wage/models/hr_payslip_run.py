from odoo import models, fields,api
from datetime import date
from datetime import datetime


class HrEmployeeRun(models.Model):
    _inherit = "hr.payslip.run"
    