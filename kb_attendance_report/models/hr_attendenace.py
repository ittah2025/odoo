from odoo import api, fields, models
from datetime import datetime
import pytz


class NewModule(models.Model):
    _inherit = 'hr.attendance'

    day_number = fields.Integer(
        string='Day_number',
        required=False, compute="get_day_number", store=True)



    @api.depends("check_in")
    def get_day_number(self):
        for att in self:
            if att.check_in:
                att.day_number = att.check_in.day
            else:
                att.day_number = 0
