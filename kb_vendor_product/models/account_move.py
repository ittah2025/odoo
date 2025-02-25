# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# Created By Mujtaba
class Accountmoveline(models.Model):
    _inherit = 'account.move.line'


    def _default_barcode(self):
        
        all_partner = self.env['res.partner'].search([('id', '=', self.move_id.
                                                       partner_id.id)])
        xm = 0
        for xpartner in all_partner:
            self.kb_vendor_ids = xpartner.kb_vendor_id2
            xm = xpartner.kb_vendor_id2.id
        
        
        all_partner2 = self.env['product_partner'].search([('kb_product_ids','=', self.product_id.id)])  # self.product_template_id.id
        
        for y in all_partner2:
            if y.kb_customer_id == self.move_id.partner_id.kb_vendor_id2:
                xm = y.id
                break
        
        return xm
    
    kb_vendor_id = fields.Many2one('product_partner', string='Vendor Code')
    kb_vendor_ids = fields.Many2one('m2n_table', string="Vendor ID")



   #fill function and set default 
    @api.onchange('product_id', 'move_id.partner_id')
    def _change_vendor(self):
        # raise ValidationError(_(f"RESU IS: {self.kb_vendor_ids.id}"))
        all_partner = self.env['res.partner'].search([('id', '=', self.move_id.
                                                       partner_id.id)])
        for xpartner in all_partner:
            self.kb_vendor_ids = xpartner.kb_vendor_id2
            # raise ValidationError(_(f"RESU IS: {self.kb_vendor_ids.id}"))
        
        self.kb_vendor_id = self._default_barcode() 
        
