from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def get_last_five_records(self):
        user_id = self.env.user.id
        attendance_records = self.search([('employee_id.user_id', '=', user_id)], order='check_in desc', limit=5)

        return [{
            'id': record.id,
            'check_in': record.check_in,
            'check_out': record.check_out,
            'worked_hours': record.worked_hours,
        } for record in attendance_records]
