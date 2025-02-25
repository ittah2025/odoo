from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)

class employee_timeoff(models.Model):
    # _inherit = 'hr.leave'
    _name = "employee_timeoff"

    leave_type = fields.Selection([('paid',"Paid"),('notpaid',"Not Paid"),('all',"All")])

    date_from = fields.Date(string="Date From")
    date_to =   fields.Date(string="Date To")


    def action_print_document(self):
        date_from = self.date_from
        date_to = self.date_to

        employee_ids = self.env['hr.employee'].search([])


        employee_time_off_list = []
        remaning = 0
        for employees_ids in employee_ids:
            total_timeoff_taken = 0
            total_timeoff = 0
            i=0
            j=0
            if self.leave_type == 'all':
                timetaken_id = self.env['hr.leave'].search([ ('date_from', '>=', date_from), ('date_to', '<=', date_to), ('employee_id', '=', employees_ids.id), ('state', '=', 'validate')])
                duration_id = self.env['hr.leave.allocation'].search(
                    [('employee_id', '=', employees_ids.id), ('state', '=', 'validate')])
                for rese in timetaken_id:
                    # if rese.holiday_status_id.id:
                    total_timeoff_taken += rese.number_of_days
                    # print(rese.number_of_days)
                for recs in duration_id:
                    total_timeoff += recs.number_of_days_display




            elif self.leave_type == 'paid':
                type_list = []
                time_type = self.env['hr.leave.type'].search([
                    ('kb_time_of_type', '=', 'True')])
                for x in time_type:
                    type_list.append(x.id)
                timetaken_paid_id = self.env['hr.leave'].search(
                    [('date_from', '>=', date_from), ('date_to', '<=', date_to), ('employee_id', '=', employees_ids.id),
                     ('state', '=', 'validate'), ('holiday_status_id','in', type_list) ])
                duration_id = self.env['hr.leave.allocation'].search(
                    [('employee_id', '=', employees_ids.id), ('state', '=', 'validate')])
                for rese in timetaken_paid_id:
                    total_timeoff_taken += rese.number_of_days
                for recs in duration_id:
                    total_timeoff += recs.number_of_days_display





            elif self.leave_type == 'notpaid':
                type_list = []
                time_type = self.env['hr.leave.type'].search([
                    ('kb_time_of_type', '!=', 'True')])
                for x in time_type:
                    type_list.append(x.id)
                timetaken_id = self.env['hr.leave'].search([('date_from', '>=', date_from),('date_to', '<=', date_to),
                                            ('employee_id', '=', employees_ids.id), ('state','=','validate'),('holiday_status_id','in', type_list)])
                # raise ValidationError(_("{} after the for\n").format(timetaken_id))
                duration_id = self.env['hr.leave.allocation'].search(
                    [('employee_id', '=', employees_ids.id), ('state', '=', 'validate')])
                # raise ValidationError(_("{} after the for\n").format(duration_id))

                for rese in timetaken_id:
                    if rese:
                        total_timeoff_taken += rese.number_of_days
                for recs in duration_id:
                    total_timeoff += recs.number_of_days_display


            total_wage = employees_ids.contract_id.wage + employees_ids.contract_id.hra + employees_ids.contract_id.da + \
                         employees_ids.contract_id.travel_allowance + employees_ids.contract_id.meal_allowance + \
                         employees_ids.contract_id.medical_allowance + employees_ids.contract_id.other_allowance

            vals = {
                'name': employees_ids.name,
                'total_timeoff': total_timeoff ,
                'Total_timeoff_taken': total_timeoff_taken,
                'time_remaining': total_timeoff - total_timeoff_taken,
                'employee_cost': (((total_wage) /30) * (total_timeoff - total_timeoff_taken)),
                'badge_id': employees_ids.barcode,
            }
            employee_time_off_list.append(vals)



        data = {
            'form_data': self.read()[0],
            'employees_id': employee_time_off_list,
        }
        return self.env.ref('kb_hr_timeoff_report.employee_time_off_print').report_action(self, data=data)



