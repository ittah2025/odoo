from odoo import api, fields, models


class document_type(models.Model):
    _name = "document_type_student"
    _table = "document_type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Document Type Information"

    name = fields.Char(related='document_type_name', required=False)
    document_type_id = fields.Char(string='Document Type Id', required=False, help='Document Type id')
    document_type_code = fields.Char(string='Document Type Code', required=False, help='Document Type Code')
    document_type_name = fields.Char(string='Document Type Name', required=False, translate=True, help='Document Type Name')