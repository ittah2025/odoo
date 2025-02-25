# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime,timedelta
from odoo.exceptions import ValidationError
from odoo import _


class vacationsettlementreport(models.Model):
    _name = "vacation_settlement_report"
    _description = "vacation settlement report"
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    employee_ar = fields.Char(string="Arabic Name")

    employee_code = fields.Char(string="Code(Employee id)")
    branch=fields.Many2one('res.branch',string="Branch")
    start_working=fields.Date(string="Start Working")
    vacation_days_balance=fields.Integer(string="Vacation days balance")
    current_loan=fields.Integer(string="Current loan")


    Salary_emp = fields.Float(string="Salary")
    Last_vacation_end = fields.Date(string="Last Vacation End")
    vacation_start_date = fields.Date(string="Vacation Start Date")
    vacation_end_date = fields.Date(string="Vacation End Date")


    vacation_duration=fields.Integer(string="Vacation Duration")
    period_of_Calc=fields.Integer(string="Period_of_Calc")
    paid_vacation_days=fields.Integer(string="Paid Vacation Days")
    unpaid_vacation_days=fields.Integer(string="Unpaid Vacation Days")
    vacation_days_salary=fields.Float(string="Vacation Days Salary", compute="unpid_and_vacation_salary")

    current_month_days = fields.Char(string="Current Month Days")
    current_month_salary = fields.Float(string="Current Month Salary")
    other_earnings = fields.Float(string="Other Earnings")

    Ticket_Cost = fields.Float(string="Ticket_Cost")
    Ticket_Give = fields.Float(string="Ticket_Give")
    Ticket_Deduc = fields.Float(string="Ticket_Deduc")


    Iqama_Deduc = fields.Float(string="Iqama_Deduc", compute="get_from_hr_contract")
    Visa_Duration = fields.Char(string="Visa_Duration")
    Visa_Deduc = fields.Float(string="Visa_Deduc",compute="get_from_hr_contract")
    Work_Permit_Deduc = fields.Float(string="Work_Permit_Deduc",compute="get_from_hr_contract")
    Health_Ins_Deduc = fields.Float(string="Health_Ins_Deduc",compute="get_from_hr_contract")
    GOSI_Deduc = fields.Float(string="GOSI_Deduc",compute="get_from_hr_contract")
    Health_certificate = fields.Float(string="Health_certificate",compute="get_from_hr_contract")

    Other_Deduc = fields.Float(string="Other_Deduc")
    Loan_Instalment = fields.Float(string="Loan_Instalment")

    earnings_total= fields.Float(string="Earnings Total",compute='get_earnings_total')
    deduction_total= fields.Float(string="Deduction Total",compute='get_deduction_total')
    Net= fields.Float(string="Net",compute='get_Net')

    employe_sign = fields.Char(string='Employee Signature')

    @api.onchange("employee_id")
    def get_from_hr_employee(self):
        employee_data=self.env['hr.employee'].search([('id','=',self.employee_id.id)])
        for rec in self:
            for record in employee_data:
                rec.employee_ar = record.arabic_name
                rec.branch = record.kb_branch
                rec.employee_code = record.id
                rec.start_working = record.first_contract_date
                rec.Salary_emp = record.emp_wage

    @api.onchange("employee_id")
    def get_from_hr_leave(self):
        employee_data = self.env['hr.leave'].search([('employee_id.id', '=', self.employee_id.id)],limit=2)
        employee = self.env['hr.leave'].search([('employee_id.id', '=', self.employee_id.id)], limit=1)
        for rec in self:
            for record in employee_data:
                for reco in employee:
                    # raise ValidationError(_(employee))
                    date_day=reco.date_from - timedelta(1)
                    rec.vacation_start_date = reco.date_from
                    rec.vacation_end_date = reco.date_to
                    rec.Last_vacation_end = record.date_to
                    day = date_day.day
                    rec.current_month_days = str(day)
                    peried =  rec.vacation_start_date-rec.Last_vacation_end
                    rec.period_of_Calc = peried.days
                    rec.vacation_duration = reco.number_of_days

    @api.onchange("employee_id")
    def get_visa_duration(self):
        contract_data = self.env['hr.contract'].search([('employee_id.id', '=', self.employee_id.id)], limit=1)
        for rec in self:
            for record in contract_data:
                rec.Visa_Duration = (record.Iqama_exp).year - (record.Iqama_start).year

    @api.onchange("employee_id")
    def piad_viction_days(self):
        duration_id = self.env['hr.leave.allocation'].search([('employee_id.id', '=', self.employee_id.id)])
        timetaken_id = self.env['hr.leave'].search([('employee_id.id', '=',self.employee_id.id), ('state', '=', 'validate'), ('holiday_status_id', '=', [1])])
        total_timeoff_taken=0
        days_display=0
        for rec in self:
            for rese in timetaken_id:
                if rese.holiday_status_id.id == 1:
                    total_timeoff_taken += rese.number_of_days
            if duration_id:
                for recs in duration_id:
                    days_display += recs.number_of_days_display
            rec.vacation_days_balance = days_display - total_timeoff_taken
            # rec.paid_vacation_days = days_display - total_timeoff_taken

    def unpid_and_vacation_salary(self):
        for record in self:
            record.vacation_days_salary = (record.Salary_emp/30) * record.paid_vacation_days



    @api.onchange("employee_id")
    def get_from_hr_flight_ticket(self):
        employee_data = self.env['hr.flight.ticket'].search([('employee_id.employee_id.id', '=', self.employee_id.id)],limit=1)
        for rec in self:
            for record in employee_data:
                rec.Ticket_Cost = record.ticket_fare
                if record.is_ticket:
                    rec.Ticket_Deduc = (rec.Ticket_Cost/730) * rec.period_of_Calc
                    rec.Ticket_Give = record.ticket_fare - rec.Ticket_Give
                else:
                    rec.Ticket_Give = (rec.Ticket_Cost / 730) * rec.period_of_Calc
                    rec.Ticket_Deduc = record.ticket_fare - rec.Ticket_Deduc

    # @api.onchange("employee_id")
    def get_from_hr_contract(self):
        contract_data = self.env['hr.contract'].search([('employee_id.id', '=', self.employee_id.id)],limit=1)
        employee_data = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        for rec in self:
            for record in contract_data:
                for reco in employee_data:
                    rec.Iqama_Deduc = round(((record.Iqama_price/((record.Iqama_exp-record.Iqama_start).days)) * rec.unpaid_vacation_days),2)
                    rec.Visa_Deduc = round(((record.Visa_price/((reco.visa_expire-record.Visa_start).days)) * rec.unpaid_vacation_days),2)
                    rec.Work_Permit_Deduc = round(((record.Work_Permit_price/((reco.work_permit_expiration_date-record.Work_Permit_start).days)) * rec.unpaid_vacation_days),2)
                    rec.Health_Ins_Deduc =round(((record.Health_Ins_price/((record.Health_Ins_exp-record.Health_Ins_start).days)) * rec.unpaid_vacation_days),2)
                    rec.GOSI_Deduc = round(((record.GOSI_price/((record.GOSI_exp-record.GOSI_start).days)) * rec.unpaid_vacation_days),2)
                    rec.Health_certificate =round(((record.Health_certificate_price/((reco.kb_Exp_health_certificate-reco.kb_releaseDate).days)) * rec.unpaid_vacation_days),2)




    @api.onchange("employee_id")
    def get_from_hr_loan(self):
        employee_data = self.env['hr.loan'].search([('employee_id.id', '=', self.employee_id.id)])
        for rec in self:
            for record in employee_data:
                date_day = (record.date).month
                day_today= date.today().month
                rec.current_loan += record.balance_amount
                if date_day == day_today:
                    rec.Loan_Instalment += record.balance_amount

    @api.onchange("employee_id")
    def get_from_hr_payslip(self):
        employee_data = self.env['hr.payslip'].search([('employee_id.id', '=', self.employee_id.id)],limit=1)
        employee_salary=self.env['hr.employee'].search([('name','=',self.employee_id.name)])
        for rec in self:
            for record in employee_data:
                rec.current_month_salary= employee_salary.emp_wage + record.wage_inclease_value - record.wage_discount_value


    def get_deduction_total(self):
       for record in self:
           record.deduction_total = record.Iqama_Deduc + record.Visa_Deduc + record.Work_Permit_Deduc + record.Ticket_Deduc\
                                    + record.Health_Ins_Deduc+ record.GOSI_Deduc + record.Health_certificate + record.Other_Deduc

    def get_earnings_total(self):
        for record in self:
            record.earnings_total = record.Ticket_Give + record.current_month_salary + record.other_earnings + record.vacation_days_salary

    def get_Net(self):
        for record in self:
            record.Net = record.earnings_total - record.deduction_total

    @api.onchange("employee_id")
    def unpid_and_paid(self):
        employee_data = self.env['hr.leave'].search([('employee_id.id', '=',self.employee_id.id)] ,limit=1 )
        for record in self:
            for rec in employee_data:
                # raise ValidationError(_(employee_data.holiday_status_id.id))
                if rec.holiday_status_id.id== 1:
                    # raise ValidationError(_(rec.number_of_days))
                    record.paid_vacation_days = rec.number_of_days
                    record.unpaid_vacation_days = rec.dayswithoutSalary
                elif rec.holiday_status_id.id == 2:
                    # raise ValidationError(_(0))
                    record.paid_vacation_days = 0
                    record.unpaid_vacation_days = rec.number_of_days

class kb_hr_employee(models.Model):
    _inherit = 'hr.employee'
    _description = 'branch in res.employee'

    kb_branch = fields.Many2one('res.branch', string="Branch")


class hr_employee_inherit(models.Model):
    _inherit = "hr.employee"
    _description = "Add arabic name"

    arabic_name=fields.Char('Arabic Name')

class hr_contract_inherit(models.Model):
    _inherit = "hr.contract"
    _description = "Add Deducs"

    Iqama_price = fields.Float(string="Iqama Price")
    Iqama_start=  fields.Date(string="Iqama Start Date ")
    Iqama_exp =  fields.Date(string="Iqama End Date")
    # Visa_Duration = fields.Char(string="Visa_Duration")

    Visa_price = fields.Float(string="Visa Price")
    Visa_start = fields.Date(string="Visa Start Date ")
    # Visa_exp = fields.Date(string="Visa End Date")

    Work_Permit_price = fields.Float(string="Work Permit Price")
    Work_Permit_start = fields.Date(string="Work Permit Start Date ")
    # Work_Permit_exp = fields.Date(string="Work Permit End Date")

    Health_Ins_price= fields.Float(string="Health Ins Price")
    Health_Ins_start = fields.Date(string="Health Ins Start Date ")
    Health_Ins_exp = fields.Date(string="Health Ins End Date")

    GOSI_price = fields.Float(string="GOSI Price")
    GOSI_start = fields.Date(string="GOSI Start Date ")
    GOSI_exp = fields.Date(string="GOSI End Date")

    Health_certificate_price = fields.Float(string="Health certificate Price")
    # Health_certificate_start = fields.Date(string="Health_certificate Start Date ")
    # Health_certificate_exp = fields.Date(string="Health_certificate End Date")

    @api.onchange("Iqama_exp")
    def check_Iqama_date(self):
        if (self.Iqama_start > self.Iqama_exp):
            raise ValidationError(_("The Start Date greate than End Date "))

    @api.onchange("GOSI_exp")
    def check_Iqama_date(self):
        if self.GOSI_start > self.GOSI_exp:
            raise ValidationError(_("The Start Date greate than End Date "))


class kb_hr_timeoff(models.Model):
    _inherit = "hr.leave"
    _description = "Add days without Salary"

    dayswithoutSalary = fields.Char( string='Day without Salary')
