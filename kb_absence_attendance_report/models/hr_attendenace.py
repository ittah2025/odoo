from odoo import api, fields, models


class NewModule(models.Model):
    _inherit = 'hr.attendance'


    date = fields.Date(
        string='Date',
        required=False, compute="get_check_date")

    @api.depends("check_in")
    def get_check_date(self):
        for att in self:
            if att.check_in:
                att.date = att.check_in.date()
            else:
                att.date = False


