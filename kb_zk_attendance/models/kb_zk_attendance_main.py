from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


import logging
_logger = logging.getLogger(__name__)

class ZkMachine(models.Model):
    _name = 'kb_zk_attendance'
    _description = 'kb zk attendance'
    # _auto = False
    # _order = 'punching_day desc'
    _rec_name = 'kb_employee_id'

    kb_employee_id = fields.Many2one('hr.employee', string="Employee", required=False, ondelete='cascade', index=True, help="Employees List")
    kb_punching_time_in = fields.Datetime(string='Punching Time In', help="Attend Time")
    kb_punching_time_out = fields.Datetime(string='Punching Time Out', help="Leaving Time")
    kb_punch_type_in = fields.Char(string='Punch Type In', help="Type Of Punch When Attend")
    kb_punch_type_out = fields.Char(string='Punch Type Out', help="Type Of Punch When Leaving")
    kb_worked_hours = fields.Float(string='Worked Hours', compute='_KBcompute_worked_hours', store=True, readonly=True, help="Calculate Worked Hours")
    kb_attendance_type_in = fields.Char(string='Attendance Type In', help="Check-In Type (Finger, Face, Card)")
    kb_attendance_type_out = fields.Char(string='Attendance Type Out', help="Check-Out Type (Finger, Face, Card)")
    kb_moved_check = fields.Boolean(string="Moved Record?", readonly=True, help="If Recorded Moved to main attendance module this checkbox Will Be True")


    @api.depends('kb_punching_time_in', 'kb_punching_time_out')
    def _KBcompute_worked_hours(self):
        for attendance in self:
            if attendance.kb_punching_time_out and attendance.kb_punching_time_in:
                delta = attendance.kb_punching_time_out - attendance.kb_punching_time_in
                attendance.kb_worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.kb_worked_hours = False

    @api.model
    def cron_moveData(self):
        _logger.info(f' Scheduled Actions (HR Attendance: Move data from Log to Attendance) Running...')
        kb_zk_attendance_obj = self.env['kb_zk_attendance'].search([('kb_moved_check', '=', False),('kb_punching_time_in', '!=', False),('kb_punching_time_out', '!=', False)])
        hr_attendance_obj = self.env['hr.attendance']

        for kb_zk_attendance in kb_zk_attendance_obj:
            if kb_zk_attendance.kb_worked_hours > 0:
                vals_zk = {}
                vals_hr = {}

                vals_zk = {
                'employee_id': kb_zk_attendance.kb_employee_id.id,
                'check_in': kb_zk_attendance.kb_punching_time_in,
                'check_out': kb_zk_attendance.kb_punching_time_out,
                }
                hr_attt_result = hr_attendance_obj.search([('employee_id', '=', kb_zk_attendance.kb_employee_id.id),
                                                        ('check_in', '=', kb_zk_attendance.kb_punching_time_in),
                                                        ('check_out', '=', kb_zk_attendance.kb_punching_time_out)])
                for hr_attendance in hr_attt_result:
                    vals_hr = {
                    'employee_id': hr_attendance.employee_id.id,
                    'check_in': hr_attendance.check_in,
                    'check_out': hr_attendance.check_out,
                    }
                if vals_zk != vals_hr:
                    try:
                        hr_attendance_id = hr_attendance_obj.create(vals_zk)
                        kb_zk_attendance.kb_moved_check = True
                    except Exception as e:
                        print(f'Cannot Move Attendance Because The Following Error: ==>{e}')
                        _logger.error(f'Cannot Move Attendance Because The Following Error: ==>{e}')
                    # raise ValidationError(_("Unsupported File Type"))

        # machines = self.env['zk.machine'].search([])
        # for machine in machines:
        #     machine.download_attendance()
    # attendance_type = fields.Selection([('1', 'Finger'),
    #                                     ('15', 'Face'),
    #                                     ('2','Type_2'),
    #                                     ('3','Password'),
    #                                     ('4','Card')],
    #                                    string='Category')
    # punch_type = fields.Selection([('0', 'Check In'),
    #                                ('1', 'Check Out'),
    #                                ('2', 'Break Out'),
    #                                ('3', 'Break In'),
    #                                ('4', 'Overtime In'),
    #                                ('5', 'Overtime Out')], string='Punching Type')
