# -*- coding: utf-8 -*-
from email.policy import default

# from sympy import sequence
#from typing_extensions import Required
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime, date
import re
import calendar
from dateutil.relativedelta import relativedelta




class academic_year(models.Model):
    '''Defines an academic year.'''

    _name = "academic_year"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "academic year"
    _rec_name="name"


    academic_yearID = fields.Char(string='year ID', required=True,
                            copy=False, readonly=True, default=lambda self: ('New'))
    date_start = fields.Date('Start Date', required=True,
                             help='Starting date of academic year')
    date_stop = fields.Date('End Date', required=False,
                            help='Ending of academic year')
    
    academic_type = fields.Selection([
        ('semester', 'Semester'),
        ('trimester', 'Trimester'),
        ('quarter', 'Quarter'),
    ], required=True, help='Choose the academic')

    
    current=fields.Boolean('Current')

    sequence = fields.Integer(string = 's', default=0)

    note = fields.Text(string="Description", required=True)

    month_ids = fields.One2many('academic_month', 'year_id', 'Months',
                                help="Related Academic months")


    school_id = fields.Many2one('school', string="School",
                                help='Select school')

    grade_id = fields.Many2many('grade', string="Grade",
                                help='Select grade')

    name = fields.Char(string='Combination')

    @api.onchange('date_stop')
    def _compute_fields_combination(self):
        for test in self:
            if test.date_start and test.date_stop:
                yearstart = test.date_start.strftime("%Y")
                yearstop = test.date_stop.strftime("%Y")
                test.name = yearstart + ' ' + '-' + ' ' + str(yearstop)

    # @api.onchange("academic_type")
    def n(self):
        if(self.academic_type == "semester"):
            interval = 1
            month_obj = self.env['academic_month']
            for rec in self:
                start_date = rec.date_start
                while start_date < rec.date_stop:
                    end_date = start_date + relativedelta(months=interval, days=-1)
                    if end_date > rec.date_stop:
                        end_date = rec.date_stop
                    month_obj.create({
                        'name': start_date.strftime('%B'),
                        'code': start_date.strftime('%m/%Y'),
                        'date_start': start_date,
                        'date_stop': end_date,
                        'year_id': rec.id,
                    })
                    start_date = start_date + relativedelta(months=interval)


    def generate_academicmonth(self):
            """Generate academic months."""
            interval = 1
            month_obj = self.env['academic_month']
            for rec in self:
                start_date = rec.date_start
                while start_date < rec.date_stop:
                    end_date = start_date + relativedelta(months=interval, days=-1)
                    if end_date > rec.date_stop:
                        end_date = rec.date_stop
                    month_obj.create({
                        'name': start_date.strftime('%B'),
                        'code': start_date.strftime('%m/%Y'),
                        'date_start': start_date,
                        'date_stop': end_date,
                        'year_id': rec.id,
                    })
                    start_date = start_date + relativedelta(months=interval)

    def generat_grades(self):
        grade = self.school_id.grade
        for rec in self:
            start_date = rec.date_start
            if grade == "primary":
                for i in range(2,31):
                    if i <10:

                        self.env['student'].create({
                                    'name': str("test" + str(i)),
                                    'student_nat_id': int("911111111" + str(i)),
                                    })
                    else:
                        self.env['student'].create({
                                    'name': str("test" + str(i)),
                                    'student_nat_id': int("11111111" + str(i)),
                                    })
                for i in range(1,7):
                    
                    grade_ids = self.env['grade'].create({
                                'name': str(start_date.strftime('%Y'))+"/"+str(i),
                                'grade_line_ids': self.env['grade_line'].create({
                                    'class_name':"1"
                                    })
                                })

                    
                    
            elif grade == "intermediate":
                for i in range(1,4):
                    grade_ids = self.env['grade'].create({
                                'name': str(start_date.strftime('%Y'))+"/"+str(i),
                                'grade_line_ids': self.env['grade_line'].create({
                                    'class_name':"1"
                                    })
                                })
            else:
                for i in range(1,4):
                    grade_ids = self.env['grade'].create({
                                'name': str(start_date.strftime('%Y'))+"/"+str(i),
                                'grade_line_ids': self.env['grade_line'].create({
                                    'class_name':"1"
                                    })
                                })

    @api.onchange('current')
    def change_student_status(self):
        if self.current:
           academics = self.env['academic_year'].search([('academic_yearID', '!=', self.academic_yearID)])
           for academic in academics:
               academic.current = False


    @api.constrains('date_start', 'date_stop')
    def _check_academic_year(self):
        '''Method to check start date should be greater than end date
           also check that dates are not overlapped with existing academic
           year'''
        new_start_date = self.date_start
        new_stop_date = self.date_stop
        delta = new_stop_date - new_start_date
        if delta.days > 365 and not calendar.isleap(new_start_date.year):
            raise ValidationError(_(
                "The duration of the academic year is invalid."))
        if (self.date_stop and self.date_start and
                self.date_stop < self.date_start):
            raise ValidationError(_(
        "The start date of the academic year should be less than end date."))
        for old_ac in self.search([('id', 'not in', self.ids)]):
            # Check start date should be less than stop date
            if (old_ac.date_start <= self.date_start <= old_ac.date_stop or
                    old_ac.date_start <= self.date_stop <= old_ac.date_stop):
                raise ValidationError(_(
                    "Error! You cannot define overlapping academic years."))



    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New academic year'

        if vals.get('academic_yearID', ('New')) == ('New'):
            vals['academic_yearID'] = self.env['ir.sequence'].next_by_code(
                'academic_year') or ('New')
        res = super(academic_year, self).create(vals)
        for rec in self:
            if rec.date_start:
                date_start = rec.date_start
                date_end = rec.date_stop
                startdateyear = datetime.strptime(str(date_start), '%Y-%m-%d').year
                startdatemonth = datetime.strptime(str(date_start),'%Y-%m-%d').month
                enddateyear = datetime.strptime(str(date_end), '%Y-%m-%d').year
                enddatemonth = datetime.strptime(str(date_end), "%Y-%m-%d" ).month
                res.name = str(startdatemonth) + '/' + str(startdateyear) + '-' + str(enddatemonth) + '/' + str(enddateyear)
        return res

class Grade(models.Model):
    _name = "grade"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "grade"

    name = fields.Char(string='name',  translate=True, help='Enter the grade name')
    # code = fields.Char(string='Code',  help='Enter the subject code')

    




    

    


