from odoo import api, fields, models, _, tools
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
class transportReport(models.Model):
    _name = 'kb_transport_report'

    academic_id=fields.Many2one('academic_year',string='Academic year')
    print_report = fields.Selection([('reason1', 'Preparing students'), ('reason2', 'Bus transportation management')], string='Report')
    kb_date_from = fields.Date("Date from:", required=True)
    kb_date_to = fields.Date("To", required=True)
    kb_TransportRoot = fields.Many2one('tran_information', string='Transport Root Name')

    def print_transport_report_details(self):

        if self.print_report == 'reason2':
            kb_transportList = []
            domain = []
            data = {
                'form_data': self.read()[0],
                'kb_transportID': kb_transportList
            }
            academic_id = self.academic_id.id
            if academic_id:
                domain += [('academic_id', '=', academic_id)]

            if domain:
                kb_transportID = self.env['tran_information'].search(domain)
            else:
                kb_transportID = self.env['tran_information'].search([])

            for info in kb_transportID:
                for infoID in kb_transportID.kb_VehicleDetails:
                    vals = {
                        'kb_TransportRoot': info.kb_TransportRoot,
                        'kb_LicensePlate': infoID.kb_LicensePlate,
                        'kb_ContactPerson': info.kb_ContactPerson,
                        'kb_idNumber': infoID.kb_driver.kb_idNumber,
                        'kb_driver': infoID.kb_driver.name,
                        'kb_phone': infoID.kb_driver.phone,
                        'kb_district': info.kb_district,
                        'kb_recordsCount': info.kb_recordsCount,
                    }
                    kb_transportList.append(vals)
            return self.env.ref('kb_Tahtheeb_school.action_transport_report_print_ids').report_action(self, data=data)

        elif self.print_report == 'reason1':

            week = self.kb_date_to - self.kb_date_from
            week_num = week.days
            print(week_num)
            if week_num >= 5 : raise ValidationError(_('You must choose week only. '))
            kb_transportList = []
            domain = []
            data = {
                'form_data': self.read()[0],
                'kb_transportRootID': kb_transportList
            }
            if self.kb_date_from:
                kb_date_from = f"{self.kb_date_from} 00:00:00"
                domain += [('kb_check_out', '>=', kb_date_from)]

            if self.kb_date_to:
                kb_date_to = f"{self.kb_date_to} 23:59:59"
                domain += [('kb_check_out', '<=', kb_date_to)]

            if self.kb_TransportRoot:
                domain += [('kb_TransportRoot.id', '=', self.kb_TransportRoot.id)]

            if domain:
                kb_transportRootID = self.env['attendance.sheet'].search(domain, order='kb_studentID desc')
            else:
                kb_transportRootID = self.env['attendance.sheet'].search([], order='kb_studentID desc')
            vals = {}
            num = 0
            for info in kb_transportRootID:

                if info.kb_check_in:
                    if info.kb_studentID.name in vals.keys():
                        vals[info.kb_studentID.name].update({info.kb_check_in.weekday(): {"checkIn": info.kb_check_in,"checkout": info.kb_check_out , 'kb_TransportRoot': info.kb_TransportRoot}})

                    else:
                        num += 1
                        vals[info.kb_studentID.name] = {info.kb_check_in.weekday(): {"checkIn": info.kb_check_in,"checkout": info.kb_check_out , 'kb_TransportRoot': info.kb_TransportRoot}}
            for val in vals:
                checkIn_sunday = ""
                checkOut_sunday = ""
                checkIn_monday = ""
                checkOut_monday = ""
                checkIn_tuesday= ""
                checkOut_tuesday = ""
                checkIn_wednesday = ""
                checkOut_wednesday = ""
                checkIn_thursday = ""
                checkOut_thursday = ""

                v = vals[val]
                if 3 in v:
                    checkIn_thursday = v[3]['checkIn']
                    checkOut_thursday = v[3]['checkout']
                if 6 in v:
                    checkIn_sunday = v[6]['checkIn']
                    checkOut_sunday = v[6]['checkout']
                if 0 in v:
                    checkIn_monday = v[0]['checkIn']
                    checkOut_monday = v[0]['checkout']
                if 1 in v:
                    checkIn_tuesday = v[1]['checkIn']
                    checkOut_tuesday = v[1]['checkout']
                if 2 in v:
                    checkIn_wednesday = v[2]['checkIn']
                    checkOut_wednesday = v[2]['checkout']

                vals2 = {
                    'stu_name': val,
                    'course':info.kb_studentID.course,
                    'grades':info.kb_studentID.grades.name,
                    'kb_TransportRoot': info.kb_TransportRoot.kb_TransportRoot,
                    'checkIn_sunday': checkIn_sunday or '',
                    'checkOut_sunday': checkOut_sunday or '',
                    'checkIn_monday': checkIn_monday or '',
                    'checkOut_monday': checkOut_monday or '',
                    'checkIn_tuesday': checkIn_tuesday or '',
                    'checkOut_tuesday': checkOut_tuesday or '',
                    'checkIn_wednesday': checkIn_wednesday or '',
                    'checkOut_wednesday': checkOut_wednesday or '',
                    'checkIn_thursday': checkIn_thursday or '',
                    'checkOut_thursday': checkOut_thursday or ''
                }
                kb_transportList.append(vals2)

            return self.env.ref('kb_Tahtheeb_school.action_Preparing_students_print_ids').report_action(self,data=data)

