import calendar
from odoo import models, fields, api, _
from datetime import datetime, date, time
import dateutil.parser
from odoo.exceptions import ValidationError

class attendens_wizard(models.TransientModel):
    _name = 'attendens.wizard'

    kb_TransportRoot = fields.Many2one('tran_information', string='Transport Root Name')
    kb_bus_responsible = fields.Many2one('hr.employee', "Bus responsible", readonly=True, related='kb_TransportRoot.kb_bus_responsible')
    studentID = fields.Many2one('student', string='Student ID', required=True)
    date_now = fields.Datetime('time' , default=datetime.now())

    def attendance_sheet_fun(self):
        record_ids = self.env['attendance.sheet'].search([('kb_studentID', '=', self.studentID.id), ('kb_check_in', '!=', False)])
        record_ids2 = self.env['attendance.sheet'].search([('kb_studentID', '=', self.studentID.id), ('kb_check_in_second', '=', False)])
        record_ids3 = self.env['attendance.sheet'].search([('kb_studentID', '=', self.studentID.id), ('kb_check_in_second', '!=', False)])
        kb_check_student = self.env['tran_information'].search([('trans_participants_ids.student_id', '=', self.studentID.name)])
        write_id = []
        start_time = time(2, 0, 0)  # 5:00 AM
        end_time = time(6, 0, 0)  # 8:00 AM
        current_time = datetime.now().time()

        for record in self:
            if kb_check_student:
                for check in kb_check_student:
                    for student_part in check.trans_participants_ids:
                        if student_part.state != 'topaid':
                            raise ValidationError(_('This student is not registered.'))
                        if student_part.transportRoot != record.kb_TransportRoot:
                            raise ValidationError(_('This student is not in this Root.'))

                    if start_time <= current_time <= end_time:
                        for rex in record_ids:
                            if date.today() == dateutil.parser.parse(str(rex.kb_check_in)).date():
                                if rex.kb_check_in:
                                    write_id = rex.write({
                                        'kb_check_out': datetime.now(),
                                        'kb_check_out_date': date.today(),
                                        'kb_weekday': calendar.day_name[rex.kb_check_in.weekday()],
                                    })


                        if not write_id:
                            vals = {
                                'kb_studentID': self.studentID.id,
                                'kb_check_in': datetime.now(),
                                'kb_TransportRoot': self.kb_TransportRoot.id,
                            }

                            kb_attendance_Sheet = self.env['attendance.sheet'].create(vals)
                    else:
                        if record_ids2:
                            vals = {
                                'kb_studentID': self.studentID.id,
                                'kb_check_in_second': datetime.now(),
                                'kb_TransportRoot': self.kb_TransportRoot.id,
                            }

                            kb_attendance_Sheet = record_ids2.write(vals)

                        for rex in record_ids3:
                            if rex.kb_check_in_second:
                                if not rex.kb_check_out_second:
                                    if date.today() == rex.kb_check_in_second.date():
                                        if rex.kb_check_in_second:
                                            write_id = rex.write({
                                                'kb_check_out_second': datetime.now(),
                                                'kb_check_out_date': date.today(),
                                                'kb_weekday': calendar.day_name[rex.kb_check_in.weekday()],
                                            })



                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

class AttendanceSheet(models.Model):
    _name = 'attendance.sheet'

    kb_studentID = fields.Many2one('student', string='Student ID')
    kb_check_in_second = fields.Datetime(string="Check In")
    kb_check_out_second = fields.Datetime(string="Check Out")
    kb_check_in = fields.Datetime(string="Check In")
    kb_check_out = fields.Datetime(string="Check Out")
    kb_check_out_date = fields.Date()
    kb_weekday = fields.Char("Week Days")
    kb_TransportRoot = fields.Many2one('tran_information', string='Transport Root Name')