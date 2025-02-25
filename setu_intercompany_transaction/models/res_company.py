from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    stock_replenishment_priority = fields.Selection(
        [('refill_from_intercomapny', "Replenish stock from another company's warehouse"),
          ('refill_from_interwarehouse',"Replenish stock from another warehouse of the same company")],
         "Stock Replenish source", default="refill_from_interwarehouse",
         help="""
            User can choose whether stock will be replenished in the warehouse from another warehouse of the same company or 
            stock will be replenished from another company's warehouse.
         """)
    create_ict_option = fields.Selection(
        [('insufficient_stock_single_product','When any single product is out of stock in requestor company'),
          ('insufficient_stock_all_product','When all products out of stock in requestor company'),
          ('always','Always'),
          ('manual','Manual - Select ICT Channel manually in sale order'),
          ], "Create Inter Company Transfer", help="""
            this field is useful to control when the inter company record will be created automatically 
            1. When any single product of sale order is out of stock in requestor company
            2. When all products of sale order are out of stock in requestor company
            3. Always create intercompany record when sale order gets confirmed in requestor company
            4. Manual - provide an option to select inter company channel manual in sale order
        """, default='manual')

    create_iwt_option = fields.Selection(
        [('stock_plus_interwarehouse', 'First use available stock and create inter warehouse transfer for remaining'),
         ('insufficient_stock_single_product', 'When any single product is out of stock in requestor warehouse'),
         ('insufficient_stock_all_product', 'When all products out of stock in requestor warehouse'),
         ('always', 'Always replenish stock'),
         ('manual', 'Manual - Select Inter Warehouse Channel manually in sale order'),
         ], "Create Inter Warhouse Transfer", help="""
            this field is useful to control when the inter warehouse record will be created automatically 
            1. When any single product of sale order is out of stock in requestor warehouse
            2. When all products of sale order are out of stock in requestor warehouse
            3. Always create interwarehouse record when sale order gets confirmed in requestor warehouse
            4. Manual - provide an option to select inter warehouse channel manual in sale order
            """, default='manual')

    @api.model
    def create(self, vals):
        company = super(ResCompany, self).create(vals)
        company.partner_id.company_id = False
        return company
    