import calendar

from odoo import models, fields, api, _
from datetime import datetime,date
import dateutil.parser
from odoo.exceptions import ValidationError

class attendens_wizard(models.TransientModel):
    _name = 'attendens_in_school_wizard'

    kb_TransportRoot = fields.Many2one('tran_information', string='Transport Root Name')
    kb_bus_responsible = fields.Many2one('hr.employee',"Bus responsible" , readonly=True , related='kb_TransportRoot.kb_bus_responsible')
    studentID = fields.Many2one('student', string='Student ID', required=True)

    def attendance_sheet_fun(self):
        record_ids = self.env['attendance.sheet.school'].search([('kb_studentID', '=', self.studentID.id), ('kb_check_in', '!=', False)])
        kb_check_student = self.env['tran_information'].search([('trans_participants_ids.student_id', '=', self.studentID.name)])
        write_id=[]
        for record in self:
            if kb_check_student:
                for check in kb_check_student:
                    for student_part in check.trans_participants_ids:
                        if student_part.state != 'registration':
                            raise ValidationError(_('This student not Registered'))
                        if student_part.transportRoot != record.kb_TransportRoot:
                            raise ValidationError(_('This student not in this Root'))

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

                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }


class AttendanceSheet(models.Model):
    _name = 'attendance.sheet.school'

    kb_studentID = fields.Many2one('student', string='Student ID')
    kb_check_in = fields.Datetime(string="Check In")
    kb_check_out = fields.Datetime(string="Check Out")
    kb_check_out_date = fields.Date('Check_out_date')
    kb_weekday = fields.Char('Weekday')
    kb_TransportRoot = fields.Many2one('tran_information', string='Transport Root Name')

