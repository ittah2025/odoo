# -*- coding:utf-8 -*-
import calendar
import babel
from odoo import api, fields, models, _, tools
from datetime import date, datetime, time


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    kb_over_time_hours = fields.Float(
        string='OverTime Hours',
        required=False, compute="get_over_time_hours", store=True)
    kb_day_work_hours = fields.Float(
        string='Day Work Hours',
        required=False, compute="get_over_time_hours", store=True)
    kb_month_last_day = fields.Integer(
        string='month last Day',
        required=False, compute="get_over_time_hours", store=True)

    @api.onchange('employee_id', 'date_from', 'date_to', 'contract_id')
    def onchange_employee(self):
        for payslip in self:
            if (not payslip.employee_id) or (not payslip.date_from) or (not payslip.date_to):
                return
            employee = payslip.employee_id
            date_from = payslip.date_from
            date_to = payslip.date_to
            contract_ids = []
            ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
            locale = self.env.context.get('lang') or 'en_US'
            payslip.name = _('Salary Slip of %s for %s') % (
                employee.name, tools.ustr(
                    babel.dates.format_date(date=ttyme, format='MMMM-y',
                                            locale=locale)))
            payslip.company_id = employee.company_id

            if not self.env.context.get('contract') or not payslip.contract_id:
                contract_ids = payslip.get_contract(employee, date_from, date_to)
                if not contract_ids:
                    payslip.contract_id = False
                    return
                payslip.contract_id = self.env['hr.contract'].browse(contract_ids[0])
            payslip.struct_id = payslip.contract_id.struct_id
            if payslip.contract_id:
                contract_ids = self.contract_id.ids
            contracts = self.env['hr.contract'].browse(contract_ids)

            input_line_ids = payslip.get_inputs(contracts, date_from, date_to)
            input_lines = payslip.input_line_ids.browse([])
            for r in input_line_ids:
                input_lines += input_lines.new(r)
            payslip.input_line_ids = input_lines
            payslip.worked_days_line_ids = [(5, 0, 0)]
            # payslip.contract_id = payslip.employee_id.contract_id if payslip.employee_id.contract_id else False
            if payslip.contract_id:
                if payslip.date_from and payslip.date_to and payslip.employee_id:
                    contract = payslip.contract_id or payslip.employee_id.contract_id
                    day_from = datetime.combine(fields.Date.from_string(payslip.date_from), time.min)
                    day_to = datetime.combine(fields.Date.from_string(payslip.date_to), time.max)
                    work_data = contract.employee_id.get_work_days_data(day_from, day_to,
                                                                        calendar=contract.resource_calendar_id)

                    attendance_domain = [('employee_id', '=', payslip.employee_id.id),
                                         ('check_in', '>=', payslip.date_from),
                                         ('check_in', '<=', payslip.date_to)]
                    attendance_date = self.env['hr.attendance'].search(attendance_domain).mapped("kb_date")
                    date_list = []
                    for att_date in attendance_date:
                        if att_date not in date_list:
                            date_list.append(att_date)
                        else:
                            continue
                    if contract:
                        work_hours = work_data['hours'] / work_data['days'] if work_data['days'] > 0 else 0
                        attendances = {
                            'name': _("Normal Working Days paid at 100%"),
                            'sequence': 1,
                            'code': 'WORK100',
                            'number_of_days': work_data['days'],
                            'number_of_hours': work_data['hours'],
                            'contract_id': contract.id,
                        }
                        absent_value = {
                            'name': _("Absent Days"),
                            'sequence': 2,
                            'code': 'ABSENT',
                            'number_of_days': work_data['days'] - len(date_list),
                            'number_of_hours': (work_data['days'] - len(date_list)) * work_hours,
                            'contract_id': contract.id,
                        }
                        over_time_value = {
                            'name': _("Over Time Hours"),
                            'sequence': 3,
                            'code': 'OVT',
                            'number_of_days': 0,
                            'number_of_hours': payslip.kb_over_time_hours,
                            'contract_id': contract.id,
                        }
                        absent_days_line = payslip.worked_days_line_ids.filtered(lambda x: x.code == 'ABSENT')
                        work100_days_line = payslip.worked_days_line_ids.filtered(lambda x: x.code == 'WORK100')
                        over_time_line = payslip.worked_days_line_ids.filtered(lambda x: x.code == 'OVT')
                        if not work100_days_line:
                            payslip.worked_days_line_ids = [(0, 0, attendances)]
                        else:
                            work100_days_line.update({
                                'number_of_days': work_data['days'],
                                'number_of_hours': work_data['days'],
                                'contract_id': contract.id,
                            })
                        if not absent_days_line:
                            payslip.worked_days_line_ids = [(0, 0, absent_value)]


                        else:
                            absent_days_line.update({
                                'number_of_days': work_data['days'] - len(date_list),
                                'number_of_hours': (work_data['days'] - len(date_list)) * work_hours,
                                'contract_id': contract.id,
                            })
                        if not over_time_line:
                            payslip.worked_days_line_ids = [(0, 0, over_time_value)]
                        else:
                            over_time_line.update({
                                'number_of_hours': payslip.kb_over_time_hours
                            })

        # return super().compute_sheet()

    @api.depends("employee_id", 'date_from', 'date_to', 'contract_id')
    def get_over_time_hours(self):
        for payslip in self:
            if payslip.contract_id and payslip.employee_id:
                date_from = payslip.date_from
                current_year = date_from.year
                current_month = date_from.month
                _, last_day = calendar.monthrange(current_year, current_month)
                payslip.kb_month_last_day = int(last_day) if date_from else 0
                contract = payslip.contract_id or payslip.employee_id.contract_id
                day_from = datetime.combine(fields.Date.from_string(payslip.date_from), time.min)
                day_to = datetime.combine(fields.Date.from_string(payslip.date_to), time.max)
                work_data = contract.employee_id.get_work_days_data(day_from, day_to,
                                                                    calendar=contract.resource_calendar_id)
                work_hours = work_data['hours'] / work_data['days'] if work_data['days'] > 0 else 0
                payslip.kb_day_work_hours = work_hours
                attendance_domain = [('employee_id', '=', payslip.employee_id.id),
                                     ('check_in', '>=', payslip.date_from), ('check_in', '<=', payslip.date_to)]
                attendance_date = self.env['hr.attendance'].search(attendance_domain).mapped("kb_date")
                attendance_date_list = []
                for att_date in attendance_date:
                    if att_date not in attendance_date_list:
                        attendance_date_list.append(att_date)
                    else:
                        continue
                all_over_time_hours = 0
                for current_date in attendance_date_list:
                    date_object = fields.Date.from_string(current_date)
                    day_name = date_object.strftime('%A')
                    attendance_day_domain = [('kb_date', '=', current_date),
                                             ('employee_id', '=', payslip.employee_id.id)]
                    attendance_hours = sum(
                        self.env['hr.attendance'].search(attendance_day_domain).mapped('worked_hours'))
                    diff_hours = attendance_hours - work_hours if attendance_hours > work_hours else 0
                    over_time_hours = (attendance_hours * 2) if day_name == 'Friday' else (
                            attendance_hours * 1.5) if day_name == 'Saturday' else (diff_hours * 1.5)
                    print("diff_hours", diff_hours, "current_date", current_date, "day_name", day_name, "diff_hours",
                          diff_hours,
                          "over_time_hours", over_time_hours, "attendance_hours", attendance_hours)

                    all_over_time_hours += over_time_hours
                payslip.kb_over_time_hours = all_over_time_hours if all_over_time_hours > 0 else 0
