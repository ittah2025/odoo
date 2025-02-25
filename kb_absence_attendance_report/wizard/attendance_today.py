from odoo import api, fields, models
from datetime import timedelta, time, datetime
from datetime import date, timedelta


class AttendanceTodayNew(models.Model):
    _name = "attendance_today_new"

    date_from = fields.Date(string='Start Date', required=False)
    date_to = fields.Date(string='End Date', required=False)

    def action_print_document(self):
        domain = []

        date_from = self.date_from 
        if date_from:
            domain += [('check_in', '>=', date_from)]

        date_to = self.date_to
        if date_to:
            domain += [('check_in', '<=', date_to)]

        attendances_obj = self.env['hr.attendance'].search(domain)
        employees_obj = self.env['hr.employee'].search([])

        attendance_dict = {}

        employee_list = []

        for attendance in attendances_obj:
            employee_id = attendance.employee_id.id
            check_in_day = attendance.check_in.day

            if employee_id in attendance_dict and check_in_day in attendance_dict[employee_id]:
                continue
            attendance_dict.setdefault(employee_id, set()).add(check_in_day)

            employee = employees_obj.filtered(lambda e: e.id == employee_id)
            if employee:
                vals = {
                    'name': employee.name,
                    'id': employee.id,
                    'department': employee.department_id.name,
                    'check_in': attendance.check_in + timedelta(hours=3),
                    'check_out': None,
                    'worked_hours': None,
                }
                employee_list.append(vals)

        data = {
            'form_data': self.read()[0],
            'employees_id': employee_list,
            'result_ids': [],

        }
        return self.env.ref('kb_absence_attendance_report.employee_attendance_today_print_new').report_action(self,
                                                                                                              data=data)

    def action_print_absence(self):
        domain = []

        date_from = self.date_from
        if date_from:
            domain += [('check_in', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('check_in', '<=', date_to)]
        attendances_obj = self.env['hr.attendance'].search(domain)
        dates = []
        for x in attendances_obj:
            if x.date in dates:
                continue
            else:
                dates.append(x.date)
        employee_ids = self.env['hr.employee'].search([])
        employee_list = []
        for att_date in dates:
            for employee in employee_ids:
                hr_att = attendances_obj.filtered(lambda x: x.employee_id.id == employee.id and x.date == att_date)
                if hr_att:
                    continue
                else:
                    vals = {
                        'name': employee.name,
                        'id': employee.id,
                        'department': employee.department_id.name,
                        'check_in': att_date,
                        'check_out': None,
                        'worked_hours': None,
                    }
                    employee_list.append(vals)

        data = {
            'form_data': self.read()[0],
            'employees_id': employee_list,
            'result_ids': [],
        }

        return self.env.ref('kb_absence_attendance_report.employee_attendance_today_print_new').report_action(self,
                                                                                                              data=data)
