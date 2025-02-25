from odoo import fields, models, api
from datetime import datetime


class kbInventoryAdjustmentsExtendedWizard(models.TransientModel):
    _name = "kb.inventory.adjustments.extended.wizard"

    kb_warehouse = fields.Many2one('stock.warehouse', string="Warehouse", required=True)
    def count_inventory_adjustments(self):
        products = self.env['product.product'].search(
            [('detailed_type', 'in', ['product'])])
            #, ('qty_available', '<=', 0)
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        for product in products:
            stock_quant = self.env['stock.quant']
            stock_quant.sudo().create({
                'in_date': datetime.now(),
                'location_id': self.kb_warehouse.lot_stock_id.id,
                'product_id': product.id,
                'reserved_quantity': product.qty_available,
                'quantity': product.qty_available,
            })
