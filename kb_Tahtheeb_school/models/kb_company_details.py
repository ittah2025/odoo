from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    kb_companyDocumentID = fields.One2many('kb.company.documents', 'kb_companyID', string='')

    name = fields.Char(string="sequencs", default='New', tracking=True)

    # SNO.
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('res.company')
        res = super(ResCompany, self).create(vals)
        sr_no = 0
        for line in res.kb_companyDocumentID:
            sr_no += 1
            line.kb_srNo = sr_no

        return res

    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        sr_no = 0
        for line in self.kb_companyDocumentID:
            sr_no += 1
            line.kb_srNo = sr_no
        return res

class companyDocuments(models.Model):
    _name = 'kb.company.documents'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    kb_srNo = fields.Integer(string='No.')
    kb_documentTypeID = fields.Many2one('kb.company.documents.info', string='Document Name', track_visibility=True)
    doc_attachment_id1 = fields.Many2many('ir.attachment', 'doc_attach_rel1', 'doc_ids', 'attach_id5',
                                         string="Attachment", help='You can attach the copy of your document', copy=False, track_visibility=True)
    kb_date = fields.Date(string='Date', track_visibility=True)

    kb_companyID = fields.Many2one('res.company')

class companyDocumentsInfo(models.Model):
    _name = 'kb.company.documents.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_documentType'

    kb_documentType = fields.Char(string='Document Name', track_visibility=True)

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel1 = fields.Many2many('document.fields', 'doc_attachment_id1', 'attach_id5', 'doc_ids', string="Attachment", invisible=1)