from odoo import api, fields, models, _
from datetime import timedelta, time, datetime
import pytz
from odoo.exceptions import ValidationError


class AttendancetToday(models.Model):
    _name = "attendance_today"

    date_from = fields.Date(string='Start Date', required=False)
    date_to = fields.Date(string='End Date', required=False)
    employee_id = fields.Many2many('hr.employee')
    day_count = fields.Integer()
    works_days_in_month = fields.Integer()
    department_id = fields.Many2one('hr.department')

    def action_print_document(self):
        unaware = datetime.now() + timedelta(hours=3)
        print('Timezone naive:', unaware)

        domain = []
        employee_id = self.employee_id
        if employee_id:
            domain += [('employee_id', 'in', employee_id.ids)]

        date_from = self.date_from
        if date_from:
            domain += [('check_in', '>=', date_from)]

        date_to = self.date_to
        if date_to:
            domain += [('check_in', '<=', date_to)]

        department = self.department_id
        if department:
            domain += [('employee_id.department_id.id', '=', department.id)]

        attendances_obj = self.env['hr.attendance'].search(domain)

        attendance_list = []
        attendance_dict = {}
        for x in attendances_obj:

            check_in_day = x.check_in.strftime('%A') if x.check_in else ''
            day = ''
            if check_in_day == "Friday":
                day = '4'
            elif check_in_day == "Thursday":
                day = '3'
            elif check_in_day == "Wednesday":
                day = '2'
            elif check_in_day == "Tuesday":
                day = '1'
            elif check_in_day == "Monday":
                day = '0'
            elif check_in_day == "Saturday":
                day = '5'
            elif check_in_day == "Sunday":
                day = '6'

            day_of_week = x.employee_id.resource_calendar_id.attendance_ids.filtered(
                lambda att: att.dayofweek == day
            )

            record_count_morning = 0
            record_count_afternoon = 0
            check_in_count = self.env['hr.attendance'].search_count([
                ('employee_id', '=', x.employee_id.id),
                ('check_in', '>=', self.date_from),
                ('check_in', '<=', self.date_to),
            ])
            print(check_in_count, "chhhhh")

            domain2 = [
                ('id', 'in', attendances_obj.ids),
                ('employee_id', '=', x.employee_id.id),
                ('day_number', '=', x.day_number),
            ]
            attendances_obj2 = self.env['hr.attendance'].search(domain2, order='check_in')
            attendance_time_1 = 0
            attendance_time_2 = 0
            check_in = None
            check_out = None
            delay_1 = None
            worked_hours = None
            check_in_2 = None
            check_out_2 = None
            delay_2 = None
            worked_hours_2 = None

            if len(attendances_obj2) > 1:
                if x.id == attendances_obj2[0].id:
                    filtered_attendance_morning = x.employee_id.resource_calendar_id.attendance_ids.filtered(
                        lambda att: att.day_period == 'morning' and att.dayofweek == day
                    )

                    if filtered_attendance_morning:
                        attendance_time_1 = filtered_attendance_morning[0].hour_from
                        check_in = x.check_in# + timedelta(hours=3)
                        check_out = x.check_out + timedelta(hours=3)
                        worked_hours = x.worked_hours

                        float_time = float(attendance_time_1)
                        hours = int(float_time)
                        minutes = int((float_time % 1) * 60)
                        time_obj = time(hours, minutes)

                        datetime_value = x.check_in + timedelta(hours=3)

                        combined_datetime = datetime.combine(datetime_value.date(), time_obj)
                        time_delta = datetime_value - combined_datetime
                        duration_minutes_1 = int(time_delta.total_seconds() // 60)

                        delay_1 = duration_minutes_1

                for y in attendances_obj:

                    if y.id == attendances_obj2[1].id:
                        filtered_attendance_afternoon = y.employee_id.resource_calendar_id.attendance_ids.filtered(
                            lambda att: att.day_period == 'afternoon' and att.dayofweek == day
                        )

                        if filtered_attendance_afternoon:
                            attendance_time_2 = filtered_attendance_afternoon[0].hour_from
                            check_in_2 = y.check_in #+ timedelta(hours=3)
                            check_out_2 = y.check_out + timedelta(hours=3)
                            worked_hours_2 = y.worked_hours

                            float_time = float(attendance_time_2)
                            hours = int(float_time)
                            minutes = int((float_time % 1) * 60)
                            time_obj = time(hours, minutes)

                            datetime_value = y.check_in + timedelta(hours=3)

                            combined_datetime = datetime.combine(datetime_value.date(), time_obj)
                            time_delta = datetime_value - combined_datetime
                            duration_minutes_2 = int(time_delta.total_seconds() // 60)

                            delay_2 = duration_minutes_2

            elif len(attendances_obj2) == 1:
                filtered_attendance_morning = x.employee_id.resource_calendar_id.attendance_ids.filtered(
                    lambda att: att.day_period == 'morning' and att.dayofweek == day
                )

                if filtered_attendance_morning:
                    attendance_time_1 = filtered_attendance_morning[0].hour_from
                    check_in = x.check_in
                    check_out = x.check_out
                    worked_hours = x.worked_hours

                    float_time = float(attendance_time_1)
                    hours = int(float_time)
                    minutes = int((float_time % 1) * 60)
                    time_obj = time(hours, minutes)

                    datetime_value = x.check_in + timedelta(hours=3)

                    combined_datetime = datetime.combine(datetime_value.date(), time_obj)
                    time_delta = datetime_value - combined_datetime
                    duration_minutes_1 = int(time_delta.total_seconds() // 60)

                    delay_1 = duration_minutes_1

            vals = {
                'name': x.employee_id.name,
                'check_in': check_in + timedelta(hours=3) if check_in else '',
                'check_out': check_out + timedelta(hours=3) if check_out else '',
                'worked_hours': worked_hours,
                'day_count': self.day_count,
                'works_days_in_month': self.works_days_in_month,
                'check_in_count': check_in_count - record_count_morning - record_count_afternoon,
                'attendance_time': attendance_time_1,
                'delay_1': delay_1,
                'attendance_time_2': attendance_time_2,
                'check_in_2': check_in_2 + timedelta(hours=3) if check_in_2 else '',
                'check_out_2': check_out_2 + timedelta(hours=3) if check_out_2 else '',
                'worked_hours_2': worked_hours_2,
                'delay_2': delay_2,
            }
            
            if attendance_time_1:
                
                if x.employee_id.name in attendance_dict:
                    attendance_dict[x.employee_id.name].append(vals)
                else:
                    attendance_dict[x.employee_id.name] = [vals]
                
        # raise ValidationError(_("{}").format(attendance_dict))
        data = {
            'form_data': self.read()[0],
            'employees_id': attendance_dict,
            'result_ids': [],

        }
        return self.env.ref('kb_attendance_report.employee_attendance_today_print').report_action(self, data=data)
