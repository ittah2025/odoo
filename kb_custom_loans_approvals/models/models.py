# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, ValidationError, UserError


class HrLoansApprovals(models.Model):
    _inherit = 'hr.loan'

    # add new states
    state = fields.Selection(selection_add=[
        ('hr', 'HR'),
        ('accounting', 'Accounting'),
        ],
        string='Status', index=True, readonly=True, copy=False,
        default='draft', tracking=True)

    # employee with salary over 5,000 cannot take a loan
    @api.onchange('employee_id')
    def get_employee_total_wage(self):
        employee_id = self.env['hr.contract.history'].search([('id', '=', self.employee_id.id)])
        no_open = 0
        if employee_id.contract_ids:
            for x in employee_id.contract_ids:

                if x.state == 'open':
                    no_open += 1
                    if x.totalallowances >= 5000:
                        raise ValidationError("You Cannot Take a Loan. Total Wage Exceeds Allowable Amount \n لا يمكنك الحصول على قرض. إجمالي الأجر يتجاوز المبلغ المسموح به ")

            if no_open == 0:
                raise ValidationError("Your Contract Might Be Expired \n قد يكون العقد الخاص بك منتهي الصلاحية")
        else:
            raise ValidationError("You Do Not Have a Contract. Please Contact You Manager \n ليس لديك عقد. يرجى الاتصال بك مدير")




    # new buttons
    def kb_set_to_hr_state_loan(self):
        return self.write({'state': 'hr'})

    def kb_set_to_accounting_state_loan(self):
        self.state = 'accounting'



