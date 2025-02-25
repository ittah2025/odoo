from odoo import api, fields, models


class report_school_hr(models.Model):
    _inherit = "hr.employee"

    select_report = fields.One2many('report_for_employee', 'select_report_to_print', string="Reports")

class report_for_employee(models.Model):
    _name = 'report_for_employee'
    select_report_to_print = fields.Many2one('hr.employee', string='Select')

    Select = fields.Selection([
        ('reason1', ' إشعار غياب '), ('reason2', ' إشعار سوء سلوك  '), ('reason3', ' مسائلة  '),
        ('reason4', ' اخرى  ')])

    Signature = fields.Char("Signature : ")
    kb_date_from = fields.Date("التاريخ من : ")
    kb_date_to = fields.Date("الى تاريخ:  ")
    kb_teacher_dec = fields.Char("رأي المعلم:  ")
    kb_Late_for = fields.Char("سبب العقوبة :  ")
    def print_pdf(self):
        for rec in self:

            if rec.Select == 'reason1':
                invoice_list=[]
                invoice_list.append({
                    'name':rec.select_report_to_print.name,
                    "kb_date_from":rec.kb_date_from,
                    "kb_date_to":rec.kb_date_to,
                    "Signature":rec.Signature,
                })

                data = {
                    'student': invoice_list,
                }
                return self.env.ref('kb_report_school_hr.kb_absence_report_action').report_action(self,data=data)

            if rec.Select == 'reason2':
                invoice_list = []
                invoice_list.append({
                    'name': rec.select_report_to_print.name,
                    "Signature": rec.Signature,
                })

                data = {
                    'student': invoice_list,
                }
                return self.env.ref('kb_report_school_hr.kb_discipline_report_action').report_action(self,data=data)

            if rec.Select == 'reason3':
                invoice_list = []
                invoice_list.append({
                    'name': rec.select_report_to_print.name,
                    "Signature": rec.Signature,
                    'kb_teacher_dec': rec.kb_teacher_dec,
                    'kb_Late_for': rec.kb_Late_for,
                    "kb_date_from": rec.kb_date_from.strftime('%A , %d %B %Y')

                })

                data = {
                    'student': invoice_list,
                }
                return self.env.ref('kb_report_school_hr.kb_accountability_report_action').report_action(self,data=data)

