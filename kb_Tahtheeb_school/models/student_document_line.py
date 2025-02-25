from odoo import api, fields, models

class studentDocumentLine(models.Model):
    _name = "student_document_line_student"
    _table = "student_document_line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student document line Information"

    student_id = fields.Many2one('student', string="Student", required=True)

    @api.onchange('no')
    def _get_line_numbers(self):
        for order in self:
                lno = 1
        for line in self:
                line.no = lno
                lno += 1
                
    no = fields.Integer(compute='_get_line_numbers', string='Serial Number', readonly=True, default=False)

    document_types = fields.Many2one('document_type_student', string="Document Type")
    document_file = fields.Binary(string='Document')
    exp_date = fields.Date(string="Expiration Date", help="choose the expire date of the document", required=True)
    desceription = fields.Text(string= " desceription", help="write about the document")


