from odoo import api, fields, models
from datetime import date, datetime,timedelta
from odoo.exceptions import  ValidationError
from odoo import _

class rejectnewstudent(models.TransientModel):

    _name = "rejectnewstudent"
    _inherit = "registrationrequest"
    _description = "Accept registration request"
    
    resone=fields.Char(string="Rejection Reason")
    Note = fields.Text(string="Note")
    email=fields.Char(string=' ')


    def action_mail_to_student(self):
        active_id = self._context.get('active_id')
        student = self.env['registrationrequest'].browse(active_id)
        student.state = 'reject'
        for rec in student:
                    mail_content = "  Dear,  " + str(rec.name) + ",<br>Thank you for applying in STTC " \
                     "<br>We appreciate the time and effort you invested in your application," \
                                "but unfortunately the position you applied for is no longer available. "
                    template_data = {
                            'subject': _(' المدرسة '),
                            'email_from': self.env.user.partner_id.email,
                            'author_id': self.env.user.partner_id.id,
                            'body': mail_content,
                            'email_to': rec.email,
                        }
                    self.env['mail.mail'].create(template_data).send()

