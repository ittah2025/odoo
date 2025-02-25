# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import qrcode
import base64
from io import BytesIO


# Created by Sukainah
class ShareholderManagementFields(models.Model):
    _name = 'kb.shareholder.management.fields'
    _description = 'Shareholder Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_shareholderName'

    kb_shareholderName = fields.Many2one('res.partner', string='Shareholder Name', track_visibility=True)
    kb_nationalityID = fields.Many2one(related='kb_shareholderName.kb_nationality', string='Nationality',
                                       readonly=False)
    kb_idNumberIDs = fields.Char(related='kb_shareholderName.kb_idNumber', string='ID Number', readonly=False)
    kb_sourceIDs = fields.Char(related='kb_shareholderName.kb_source', string='Source', readonly=False)

    kb_street = fields.Char(related='kb_shareholderName.street', string='street', readonly=False)
    kb_street2 = fields.Char(related='kb_shareholderName.street2', string='street2', readonly=False)
    kb_city = fields.Char(related='kb_shareholderName.city', string='city', readonly=False)
    kb_zip = fields.Char(related='kb_shareholderName.zip', string='zip', readonly=False)
    kb_countryID = fields.Many2one(related='kb_shareholderName.country_id', string='country', readonly=False)

    kb_phone = fields.Char(related='kb_shareholderName.phone', string='phone', readonly=False)
    kb_mobile = fields.Char(related='kb_shareholderName.mobile', string='mobile', readonly=False)
    kb_email = fields.Char(related='kb_shareholderName.email', string='email', readonly=False)

    kb_joiningDate = fields.Date(string='Joining Date')

    kb_stockNumber = fields.Float(string='Stock Number', track_visibility=True, required=True)
    # kb_allStock = fields.Float(string='All Stock Number', required=True)
    kb_percentage = fields.Float(string="Percentage", store=True)

    kb_shareholderID = fields.Char(string='Shareholder ID', required=True,
                                   copy=False, readonly=True, default=lambda self: _('Draft'))
    note = fields.Char()

    doc_attachment_id00 = fields.Many2many('ir.attachment', 'doc_attach_rel00', 'doc_ids', 'attach_id5',
                                           string="Attachment",
                                           help='You can attach the copy of your document', copy=False,
                                           track_visibility=True)

    active = fields.Boolean(string='Active', default=True)

    # kb_qr_code = fields.Binary("QR Code", compute='_generate_qr_code')
    kb_qr_code = fields.Char("QR Code", compute='_generate_qr_code', store=True)


    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Order'
        if vals.get('kb_shareholderID', ('New')) == ('New'):
            vals['kb_shareholderID'] = self.env['ir.sequence'].next_by_code(
                'kb_shareholderID.seq') or ('New')
        res = super(ShareholderManagementFields, self).create(vals)
        return res

    @api.onchange('kb_stockNumber')
    def compute_percentage(self):
        kb_companyInfo = self.env['res.company'].search([('id', '=', 1)])
        for record in self:
            if kb_companyInfo.kb_allStock != 0.00:
                record.kb_percentage = (record.kb_stockNumber / kb_companyInfo.kb_allStock)

    @api.depends('kb_shareholderID')
    def _generate_qr_code(self):
        for record in self:
            if record.kb_shareholderID:
                # Generate the content for the QR code
                qr_content = f"{record.kb_shareholderID} - tahtheeb"
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_content)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue()).decode('utf-8')
                record.kb_qr_code = qr_image


# class Attachment(models.Model):
#     _inherit = 'ir.attachment'

#     doc_attach_rel00 = fields.Many2many('document.fields', 'doc_attachment_id00', 'attach_id5', 'doc_ids',
#                                         string="Attachment", invisible=1)


class SaleManagement(models.Model):
    _name = 'kb.sale.management'
    _description = 'Sale and Purchase Request'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    transaction_date = fields.Date(string='Transaction Date')
    purchaser = fields.Many2one('res.partner', string='Purchaser')
    seller = fields.Many2one('res.partner', string='Seller')
    number_of_shares = fields.Integer(string='Number of Shares Sold')
    price = fields.Float(string='Selling Price')
    description = fields.Char(string='Description')
    user_id = fields.Many2one('res.users', string='Responsible User', )

    # New field for QR code
    qr_code = fields.Char("QR Code", compute='_generate_qr_code')

    def _generate_qr_code(self):
        for record in self:
            if record.name:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(record.name)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue()).decode('utf-8')  # Convert to string
                record.qr_code = qr_image

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('kb.sale.management') or _('New')
        res = super(SaleManagement, self).create(vals)
        res.update_shareholder_stock()
        return res

    def write(self, vals):
        res = super(SaleManagement, self).write(vals)
        self.update_shareholder_stock()
        return res

    def update_shareholder_stock(self):
        for record in self:
            # Update purchaser stock number
            shareholder = self.env['kb.shareholder.management.fields'].search(
                [('kb_shareholderName', '=', record.purchaser.id)], limit=1)
            if shareholder:
                shareholder.kb_stockNumber += record.number_of_shares
            else:
                self.env['kb.shareholder.management.fields'].create({
                    'kb_shareholderName': record.purchaser.id,
                    'kb_stockNumber': record.number_of_shares
                })

            # Update seller stock number
            shareholder_seller = self.env['kb.shareholder.management.fields'].search(
                [('kb_shareholderName', '=', record.seller.id)], limit=1)
            if shareholder_seller:
                shareholder_seller.kb_stockNumber -= record.number_of_shares

            else:
                self.env['kb.shareholder.management.fields'].create({
                    'kb_shareholderName': record.seller.id,
                    'kb_stockNumber': record.number_of_shares * -1
                })
