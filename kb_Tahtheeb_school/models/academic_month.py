# -*- coding: utf-8 -*-
from email.policy import default
#from typing_extensions import Required
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import date
import re
import calendar
from dateutil.relativedelta import relativedelta




class academic_month(models.Model):
    '''Defining a month of an academic year.'''

    _name = "academic_month"
    _description = "Academic Month"
    _order = "date_start"

    name = fields.Char('Name', required=True, help='Name')
    code = fields.Char('Code', required=True, help='Code')
    date_start = fields.Date('Start of Period', required=True,
                             help='Start date')
    date_stop = fields.Date('End of Period', required=True,
                            help='End Date')
    year_id = fields.Many2one('academic_year', 'Academic Year', required=True,
                              help="Related academic year ")
    # description = fields.Text('Description', help='Description', required=True)

    _sql_constraints = [
        ('month_unique', 'unique(date_start, date_stop, year_id)',
         'Academic Month should be unique!'),
    ]
    
    

    sequence = fields.Integer(string = 's', default=0)
    @api.constrains('year_id', 'date_start', 'date_stop')
    def _check_year_limit(self):
        '''Method to check year limit'''
        if self.year_id and self.date_start and self.date_stop:
            if (self.year_id.date_stop < self.date_stop or
                    self.year_id.date_stop < self.date_start or
                    self.year_id.date_start > self.date_start or
                    self.year_id.date_start > self.date_stop):
                raise ValidationError(_(
        "Some of the months periods overlap or is not in the academic year!"))

    @api.constrains('date_start', 'date_stop')
    def check_months(self):
        '''Method to check duration of date'''
        if (self.date_stop and self.date_start and
                self.date_stop < self.date_start):
            raise ValidationError(_(
        "End of Period date should be greater than Start of Periods Date!"))
        """Check start date should be less than stop date."""
        exist_month_rec = self.search([('id', 'not in', self.ids)])
        for old_month in exist_month_rec:
            if old_month.date_start <= \
                    self.date_start <= old_month.date_stop \
                    or old_month.date_start <= \
                    self.date_stop <= old_month.date_stop:
                raise ValidationError(_(
                            "Error! You cannot define overlapping months!"))
