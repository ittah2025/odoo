from odoo import models, fields,tools,_
from odoo.exceptions import UserError, ValidationError

# discount and increase fields at the contract (salary information)
class hr(models.Model):
    _inherit = "hr.contract"


    wage_discount_value = fields.Float(string='Deduction Value', compute="kb_count_dec_and_inc")
    wage_inclease_value = fields.Float(string='Increase Value', compute="kb_count_dec_and_inc")
    
    def kb_count_dec_and_inc(self):
        wage = self.env['hr.payslip'].search([('employee_id.id', '=', self.employee_id.id)])
        inc=0
        dec=0
        for recored in self:
            if not recored.date_end:
                for reco in wage:
                    if recored.date_start > reco.date_from :
                        dec += reco.wage_discount_value
                        inc += reco.wage_inclease_value
            elif recored.date_end:
                for reco in wage:
                    if (recored.date_start > reco.date_from) and (recored.date_end < reco.date_from):
                        dec += reco.wage_discount_value
                        inc += reco.wage_inclease_value
            recored.wage_discount_value = dec
            recored.wage_inclease_value = inc
