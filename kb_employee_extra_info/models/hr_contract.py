# -*- coding: utf-8 -*-


from datetime import timedelta
from odoo import models, fields, _, api
from odoo.exceptions import ValidationError, UserError

class HrContract(models.Model):
    _inherit = 'hr.contract'

    #Getting Allowances to add them to total salary

    totalallowances = fields.Monetary(string='Total With Allowances', readonly=True, compute='_compute_TotalWtihAllowances')


    @api.depends('totalallowances')
    def _compute_TotalWtihAllowances(self):
        totalallowances = 0
        for record in self:
            wage    = record.wage
            hra     = record.hra
            da      = record.da
            travel  = record.travel_allowance
            fixed   = record.fixed_allowance
            unfixed = record.unfixed_allowance
            woc     = record.working_other_companies_allowance
            meal    = record.meal_allowance
            medical = record.medical_allowance
            # other   = record.other_allowance
            
       

            record.totalallowances = 0
            # record.totalallowances = wage + hra + da + travel + fixed + unfixed + woc + meal + medical + 0
        # raise ValidationError(_(TotalWtihAllowances))
