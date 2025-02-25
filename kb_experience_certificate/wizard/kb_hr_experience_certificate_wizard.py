from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class hr_experience_certificate_reports(models.TransientModel):
    _name = 'kb_hr_experience_certificate_reports'

    employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True)

    def print_wizard_pdf(self):
        employee_ids = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        experienceCertificate_ids_list = []
        for i in employee_ids:
            if i.contract_ids:
                for x in i.contract_ids:
                    vals = {
                        'name': i.name,
                        'job_title': i.job_title,
                        'first_contract_date':i.first_contract_date,
                    }
                    experienceCertificate_ids_list.append(vals)
            else:
                raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد ")
                

        data = {
            'form_data': self.read()[0],
            'experienceCertificate_list_loop': experienceCertificate_ids_list,
            'result_ids': [],
        }
        return self.env.ref('kb_experience_certificate.kb_hr_experience_certificate_ids').report_action(self, data=data)



        
