from odoo import fields, models, api, _
from datetime import datetime


class SetuIntercomapnyChannel(models.Model):
    _name = 'setu.intercompany.channel'
    _description="""
        Intercompany channel is used to define an automated actions should be taken when source company receive orders
    """
    name = fields.Char("Name")
    requestor_company_id = fields.Many2one("res.company", "Requestor")
    fulfiller_company_id = fields.Many2one("res.company", "Fulfiller", change_default=True)
    fulfiller_warehouse_id = fields.Many2one("stock.warehouse", "Fulfiller Warehouse", change_default=True)
    manage_lot_serial = fields.Boolean("Manage serial / lot number in Inter Company Transactions?", help="""
        This option helps to manage lot/serial number automatically in requestor company.
        Lot /Serial number which are set in fulfiller company's delivery will set directly in requestor company's incoming shipmenet
    """)
    direct_deliver_to_customer = fields.Boolean("Direct deliver to origin sale order's customer?",help="""
        If requester company wants to deliver his order directly to it's sale order's customer then 
        this option must be selected.
        If this option is selected fulfiller company will deliver stock to requestor company's order
        Note: 
		it will close incoming shipment of requestor company when destination company deliver order to customer
    """)

    active = fields.Boolean("Active", default=True)
    auto_workflow_id = fields.Many2one("setu.ict.auto.workflow", "Auto workflow")
    vendor_bill_journal_id = fields.Many2one("account.journal", "Vendor Bill Journal", change_default=True)
    customer_invoice_journal_id = fields.Many2one("account.journal", "Customer Invoice Journal", change_default=True)
    ict_user_id = fields.Many2one("res.users", "Inter Company User")
    sales_team_id = fields.Many2one("crm.team", "Sales Team")
    fulfiller_fiscal_position_id = fields.Many2one('account.fiscal.position', "Fulfiller Fiscal Position", change_default=True)
    requestor_fiscal_position_id = fields.Many2one('account.fiscal.position', "Requestor Fiscal Position", change_default=True)
    sequence = fields.Integer("Priority")
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')

    @api.onchange('fulfiller_company_id')
    def onchange_fulfiller_company_id(self):
        if self.fulfiller_company_id:
            warehouse = self.env['stock.warehouse'].search([('company_id','=',self.fulfiller_company_id.id)])
            if len(warehouse.ids) == 1:
                self.fulfiller_warehouse_id = warehouse
            else:
                self.fulfiller_warehouse_id =False
            self.fulfiller_fiscal_position_id = False
            self.customer_invoice_journal_id = False

    @api.onchange('requestor_company_id')
    def onchange_requestor_company_id(self):
        self.fulfiller_company_id = False
        self.customer_invoice_journal_id = False
        self.vendor_bill_journal_id = False
        self.fulfiller_warehouse_id = False
        self.fulfiller_fiscal_position_id = False
        self.requestor_fiscal_position_id = False
        self.pricelist_id = self.requestor_company_id.partner_id.property_product_pricelist and self.requestor_company_id.partner_id.property_product_pricelist.id or False

    def get_channel_source_for_ict(self, requestor_company_id):
        channel = self.search([('requestor_company_id','=',requestor_company_id)], order='sequence', limit=1)
        return channel or False

    def prepare_ict_line_vals(self, order_line, ict):
        return {
            'product_id': order_line.product_id.id,
            'quantity': order_line.product_uom_qty,
            'unit_price': order_line.price_unit,
            'intercompany_transfer_id': ict.id,
        }

    def create_ict_lines(self, origin_sale_id, ict):
        ict_lines = []
        for line in origin_sale_id.order_line:
            ict_line_vals = self.prepare_ict_line_vals(line, ict)
            ict_line = self.env['setu.intercompany.transfer.line'].create(ict_line_vals)
            ict_line.product_id_change()
            ict_line.unit_price = ict_line.get_price()
            ict_lines.append(ict_line)
        return ict_lines

    def prepare_intercompany_vals(self, origin_sale_id):
        ict_vals = {
            'ict_date' : datetime.today(),
            'requestor_warehouse_id' : origin_sale_id.warehouse_id.id,
            'fulfiller_warehouse_id' : self.fulfiller_warehouse_id.id,
            'direct_deliver_to_customer' : self.direct_deliver_to_customer,
            'manage_lot_serial' : self.manage_lot_serial,
            'auto_workflow_id' : self.auto_workflow_id.id,
            'intercompany_channel_id' : self.id,
            'pricelist_id' : self.pricelist_id.id,
            'sales_team_id' : self.sales_team_id.id,
            'ict_user_id' : self.ict_user_id.id,
            'origin_order_id' : origin_sale_id.id,
            'transfer_type' : 'inter_company',
            'state' : 'draft',
        }

        return ict_vals

    def create_ict_from_channel(self, origin_sale_id):
        ict_vals = self.prepare_intercompany_vals(origin_sale_id)
        ict = self.env['setu.intercompany.transfer'].create(ict_vals)
        ict_lines = self.create_ict_lines(origin_sale_id, ict)

        ict.onchange_requestor_warehouse_id()
        ict.onchange_fulfiller_warehouse_id()
        ict.pricelist_id = self.pricelist_id.id

        self.execute_workflow(ict)
        return ict

    def execute_workflow(self, ict):
        if ict.state == 'draft' and self.auto_workflow_id and self.auto_workflow_id.validate_ict:
            ict.action_validate_intercompany_transfer()


        
    