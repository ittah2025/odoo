from odoo import api, fields, models
class Employee_Signature(models.Model):
  _inherit =  "hr.employee"

  Signature = fields.Char("Signature : ")

  def print_pdf(self):

    return self.env.ref('kb_report_signature.kb_signature_employee_action').report_action(self)