from odoo import api, fields, models, _
from datetime import date
from datetime import timedelta, datetime

class companyDocuments(models.Model):
    _name = 'kb.company.documents'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    kb_srNo = fields.Integer(string='No.')
    kb_documentTypeID = fields.Many2one('kb.company.documents.info', string='Document Name', track_visibility=True)
    kb_doc_attachment = fields.Many2many('ir.attachment', 'kb_doc_attach', 'doc_ids', 'attach_id5',
                                         string="Attachment", help='You can attach the copy of your document', copy=False, track_visibility=True)
    kb_date = fields.Date(string='Expiry Date', track_visibility=True)

    def mail_reminder(self):
        companyDocuments = self.env['kb.company.documents'].search([])
        companyEmail = self.env['res.company'].search([])
        date_now = date.today()

        for rec in companyDocuments:
            for record in companyEmail:
                if rec.kb_date:
                    kb_expiryDate = rec.kb_date - date_now
                    kb_expiryDate = kb_expiryDate.days
                    if kb_expiryDate <= 10:
                        mail_content = "  Hello  " + ",<br>Your Document " +  rec.kb_documentTypeID.kb_documentType + "is going to expire on " + \
                                       str(rec.kb_date) + ". Please renew it before expiry date"
                        main_content = {
                        'subject': ('%s Expired On %s') % (
                            rec.kb_documentTypeID.kb_documentType, rec.kb_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': record.email,
                        }
                        self.env['mail.mail'].create(main_content).send()

class companyDocumentsInfo(models.Model):
    _name = 'kb.company.documents.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_documentType'

    kb_documentType = fields.Char(string='Document Name', track_visibility=True)

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    kb_doc_attach = fields.Many2many('document.fields', 'kb_doc_attachment', 'attach_id5', 'doc_ids', string="Attachment", invisible=1)