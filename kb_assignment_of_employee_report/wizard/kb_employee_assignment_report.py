from odoo import api, fields, models
import arabic_reshaper
from bidi.algorithm import get_display
from hijri_converter import convert


class EmployeeAssignment(models.Model):
    _name = "employee.assignment.report"

    kb_employees_id = fields.Many2one('hr.employee', string='Employee')
    kb_employee_name = fields.Char(related='kb_employees_id.name')
    date = fields.Date(default=fields.Date.today(), store=True)
    arabic_date = fields.Date()
    job = fields.Char(required=True, string='About')
    content = fields.Char(required=True)

    @api.model
    def create(self, values):
        record = super(EmployeeAssignment, self).create(values)
        record._update_arabic_date()
        return record

    @api.onchange('date')
    def _onchange_date(self):
        self._update_arabic_date()

    def _update_arabic_date(self):
        if self.date:
            arabic_date = self.get_arabic_date(self.date)
            self.arabic_date = arabic_date
        else:
            self.arabic_date = None

    def get_arabic_date(self, gregorian_date):
        year, month, day = gregorian_date.year, gregorian_date.month, gregorian_date.day
        hijri_date = convert.Gregorian(year, month, day).to_hijri()
        hijri_date_str = str(hijri_date)  # Convert Hijri object to string
        reshaped_arabic_date = arabic_reshaper.reshape(hijri_date_str)
        bidi_arabic_date = get_display(reshaped_arabic_date)
        return bidi_arabic_date

    def action_print_report(self):
        data = {
            'form_data': self.read()[0],
            'employee_list': [],
            'result_ids': [],
        }

        for employee in self.kb_employees_id:
            if employee:
                domain = [('id', '=', employee.id)]
                employee_domain = self.env['hr.employee'].search(domain)
                for emp in employee_domain:
                    employee_list = []
                    vals = {
                        'employee_name': emp.name,
                        'employee_nationalty': emp.country_id.name,
                        'employee_jop': emp.job_title,

                    }
                    employee_list.append(vals)

                    data['employee_list'].append({
                        'employees': employee_list,
                    })
        return self.env.ref('kb_assignment_of_employee_report.employee_assignment_report_action').report_action(self,
                                                                                                                data=data)
