from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    

    # kb_vendor_ids = fields.Many2one('m2n_table', string="Vendor ID")
    
        
    def _default_barcode(self):
        # all_partner = self.env['res.partner'].search([('id', '=', self.order_id.partner_id.id)])
        
        # for xpartner in all_partner:  
        #         self.kb_vendor_ids = xpartner.kb_vendor_id2
        # ss =  self.env['res.partner'].search([('id', '=', self.order_id.partner_id.id)])      
        
        
        # x = self.env['product.product'].search([('kb_product_id.kb_customer_id', '=', ss.kb_vendor_id2.name)], limit=1).id
        
        all_partner = self.env['res.partner'].search([('id', '=', self.order_id.
                                                       partner_id.id)])
        xm = 0
        for xpartner in all_partner:
            self.kb_vendor_ids = xpartner.kb_vendor_id2
            xm = xpartner.kb_vendor_id2.id
        
        
        all_partner2 = self.env['product_partner'].search([('kb_product_ids','=', self.product_id.id)])  # self.product_template_id.id
        
        for y in all_partner2:
            if y.kb_customer_id == self.order_id.partner_id.kb_vendor_id2:
                xm = y.id
                break
        
        #, limit=1
        
        # raise ValidationError(_(all_partner2))
        # self.product_template_id.kb_product_id.id
        
        return xm
    
    
    
   
    kb_vendor_id = fields.Many2one('product_partner', string='Vendor Code')
    kb_vendor_ids = fields.Many2one('m2n_table', string="Vendor ID")
   
    def _prepare_invoice_line(self,**optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'kb_vendor_id': self.kb_vendor_id.id, })
        return res
    
   #fill function and set default 
    @api.onchange('product_id', 'order_id.add_prod_price')
    def _change_vendor(self):
        # raise ValidationError(_(f"RESU IS: {self.kb_vendor_ids.id}"))
        all_partner = self.env['res.partner'].search([('id', '=', self.order_id.
                                                       partner_id.id)])
        for xpartner in all_partner:
            self.kb_vendor_ids = xpartner.kb_vendor_id2
            # raise ValidationError(_(f"RESU IS: {self.kb_vendor_ids.id}"))
        
        self.kb_vendor_id = self._default_barcode() 
        
            
        
    
    





    
    

            
