from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    kb_date = fields.Date(
        string='Date',
        required=False, compute="get_attendance_date",store=True)

    @api.depends("check_in")
    def get_attendance_date(self):
        for att in self:
            if att.check_in:
                att.kb_date = att.check_in.date()
            else:
                att.kb_date = False
