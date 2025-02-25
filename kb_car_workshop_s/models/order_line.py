
from odoo import api, fields, models, _
from logging import getLogger



#start from here 


class ordersLine(models.Model):
    _name = "order_line"
    _table = "order_line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Orders line Information"

    order_id = fields.Many2one('orders', string="Orders")

    product_id = fields.Many2one('product.template', string="product Id")

   # product_code = fields.Char(string='Product Code', related="product_id.default_code", required=False)
    product_barcode = fields.Char(string='Product Barcode', related="product_id.barcode")
    product_price = fields.Float(string='Product Price', related="product_id.list_price")
    product_qty = fields.Float(string='Product Qty', required=False)
    transfer_check = fields.Boolean(string="Transfer")
    order_id_line = fields.Many2one('orders', string="Order ID")
    source_location = fields.Many2one('stock.location')
    destenation_location = fields.Many2one('stock.location')


    def move_to_transfer(self):
        stock_id = self.env['stock.picking'].create({
                    'origin': self.order_id_line.order_ID,
                    'location_id':self.source_location.id,
                    'location_dest_id':self.destenation_location.id,
                    # picking_type_id 2 for Outgoing 
                    'picking_type_id': 2,
                    # 'picking_type_code': 'outgoing',
                    })
        # for lines in self:
        stock_move_id = self.env['stock.move'].create({
            'product_id':self.product_id.id,
            'picking_id': stock_id.id,
            'product_uom_qty': self.product_qty,
            'location_id':self.source_location.id,
            'location_dest_id':self.destenation_location.id,
            'picking_type_id': 2,
            'name': stock_id.id,
        })
        if stock_move_id:
            self.transfer_check = True

    # move_ids_without_package