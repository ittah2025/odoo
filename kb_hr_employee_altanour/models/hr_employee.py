# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime,timedelta
from odoo.exceptions import ValidationError
from odoo import _


class kb_hr_employee(models.Model):
    _inherit = "hr.employee"
    _description = "hr"

    kb_number_Certificate = fields.Char(string='Health certificate number  ')
    kb_releaseDate = fields.Date(string='Release Date')
    kb_Exp_health_certificate = fields.Date(string='Expiration Date')

    kb_health_programme = fields.Char(string='Type of educational programme ')
    kb_Exp_programme = fields.Date(string='Expiration date of educational programme ')

    def mail_reminder_for_kb_Exp_health_certificate(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        for rec in self:
            if rec.kb_Exp_health_certificate:
                id_expiry_date = rec.kb_Exp_health_certificate - timedelta(days=10)
                if date_now >= id_expiry_date:
                    mail_content = "  Hello  " + rec.name + ",<br>Your Health certificate is going to expire on " + \
                                       str(rec.kb_Exp_health_certificate) + ". Please renew it before expiry date"
                    main_content = {
                         'subject': _('ID-%s Expired On %s') % (
                                rec.name, rec.kb_Exp_health_certificate),
                        'email_from': self.env.user.partner_id.email,
                        'author_id': self.env.user.partner_id.id,
                        'body': mail_content,
                        'email_to': rec.work_email,
                    }
                    self.env['mail.mail'].create(main_content).send()

    def mail_reminder_for_kb_Exp_programme(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        for rec in self:
            if rec.kb_Exp_programme:
                id_expiry_date = rec.kb_Exp_programme - timedelta(days=10)
                if date_now >= id_expiry_date:
                    mail_content = "  Hello  " + rec.name + ",<br>Your Document " + rec.kb_health_programme + "is going to expire on " + \
                                   str(rec.kb_Exp_programme) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('ID-%s Expired On %s') % (
                            rec.kb_health_programme, rec.kb_Exp_programme),
                        'email_from': self.env.user.partner_id.email,
                        'author_id': self.env.user.partner_id.id,
                        'body': mail_content,
                        'email_to': rec.work_email,
                    }
                    self.env['mail.mail'].create(main_content).send()