from odoo import _, api, fields, models

class PayFeesWizard(models.TransientModel):
    
    _name = 'pay.fees.wizard'
    _description = "Pay Fees Wizard"

    is_paid=fields.Boolean(string="Paid  fees",default=True)
    company_id = fields.Many2one("res.company",default=lambda x:x.env.company.id,invisible=True)
    journal_id = fields.Many2one(
        "account.journal", "Journal", help="Select Journal", required=True, domain="[('company_id','=',company_id),('type', 'in', ('bank', 'cash'))]")

    def  action_pay_fees(self):
        ctx = self._context.copy()
        student_payslip = self.env['student.payslip'].browse(ctx.get("active_id",False))
        move_id = student_payslip.with_context(journal_id=self.journal_id.id,is_paid=self.is_paid).student_pay_fees()
        return move_id
