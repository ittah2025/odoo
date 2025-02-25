# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

from odoo import models, fields, api, _


class CompanyDocument(models.Model):
    # _name = 'hr.employee.document'
    _name = 'hr.company.document'
    _description = 'Company Documents'

    def mail_reminder(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.expiry_date:
                exp_date = i.expiry_date - timedelta(days=7)
                if date_now >= exp_date:
                               mail_content = "  Hello  " + i.company_ref.name + ",<br>Your Document " + i.name + "is going to expire on " + \
                                   str(i.expiry_date) + ". Please renew it before expiry date"
                main_content = {
                        'subject': _('Document-%s Expired On %s') % (i.name, i.expiry_date),
                        # 'author_id': self.env.company.partner_id.id,
                        # 'author_id': self.env.company.id,
                         'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.company_ref.email,
                    }
                self.env['mail.mail'].create(main_content).send()
                
                    # mail_content = "  Hello  " + i.employee_ref.name + ",<br>Your Document " + i.name + "is going to expire on " + \
                    #                str(i.expiry_date) + ". Please renew it before expiry date"
                        # main_content = {
                        # 'subject': _('Document-%s Expired On %s') % (i.name, i.expiry_date),
                        # 'author_id': self.env.user.partner_id.id,
                        # 'body_html': mail_content,
                        # 'email_to': i.employee_ref.work_email,
                    #       }
                    # self.env['mail.mail'].create(main_content).send()

    @api.onchange('expiry_date')
    def check_expr_date(self):
        for each in self:
            exp_date = each.expiry_date
            if exp_date and exp_date < date.today():
                return {
                    'warning': {
                        'title': _('Document Expired.'),
                        'message': _("Your Document Is Already Expired.")
                    }
                }

    name = fields.Char(string='Document Number', required=True, copy=False)
    document_name = fields.Text(string='Document', copy=False)
    description = fields.Text(string='Description', copy=False)
    expiry_date = fields.Date(string='Expiry Date', copy=False)
    # employee_ref = fields.Many2one('hr.employee', copy=False)
    company_ref = fields.Many2one('res.company', copy=False)
    doc_attachment_id1 = fields.Many2many('ir.attachment', 'doc_attach_rel1', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)
    issue_date = fields.Date(string='Issue Date', default=fields.Date.context_today, copy=False)


class HrCompany(models.Model):
    _inherit = 'res.company'


    def _document_count(self):
        for each in self:
            document_ids = self.env['hr.company.document'].search([('company_ref', '=', each.id)])
            each.document_count = len(document_ids)


    def document_view(self):
        self.ensure_one()
        domain = [
            ('company_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'hr.company.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_company_ref': '%s'}" % self.id
        }

    document_count = fields.Integer(compute='_document_count', string='# Documents')


class HrCompanyAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel1 = fields.Many2many('hr.company.document', 'doc_attachment_id1', 'attach_id3', 'doc_id',
                                      string="Attachment", invisible=1)
