from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import xlwt
from io import BytesIO
import base64
from xlwt import easyxf

class hr_defintion_of_salary_reports(models.TransientModel):
    _name = 'hr_defintion_of_salary_reports'
    
    sender = fields.Char(string="Name of the sender")
    employee_id = fields.Many2one('hr.employee', string="Employee name", required=True)
    
    
    
    def print_wizard_pdf(self):
        # raise ValidationError(_("{} after the for\n").format("result"))
        employee_ids = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])

        salary_ids_list = []
        for i in employee_ids:
            if i.contract_ids:
                for x in i.contract_ids:
                    vals = {
                        'wage': x.wage,
                        'name': i.name,
                        'job_id': i.job_id.name,
                        'identification_id': i.identification_id,
                    }
                    salary_ids_list.append(vals)
            else:
                raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد ")
                

        data = {
            'form_data': self.read()[0],
            'salary_list_loop': salary_ids_list,
            'result_ids': [],

        }
        return self.env.ref('kb_end_of_service.defintion_of_salary_ids_wizard').report_action(self, data=data)



        

        
