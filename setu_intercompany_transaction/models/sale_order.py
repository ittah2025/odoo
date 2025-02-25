from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    stock_replenishment_priority = fields.Selection(related='company_id.stock_replenishment_priority', readonly=True)
    intercompany_transfer_id = fields.Many2one("setu.intercompany.transfer","Intercompany Transfer", copy=False, index=True)
    create_ict_option = fields.Selection(related='company_id.create_ict_option', readonly=True)
    create_iwt_option = fields.Selection(related='company_id.create_iwt_option', readonly=True)
    intercompany_channel_id = fields.Many2one("setu.intercompany.channel", "Intercompany Channel", copy=False, index=True)
    interwarehouse_channel_id = fields.Many2one("setu.interwarehouse.channel", "Interwarehouse Channel", copy=False,
                                              index=True)

    ict_ids = fields.One2many('setu.intercompany.transfer', 'origin_order_id', string='ICT')
    ict_count = fields.Integer(string='ICT', compute='_compute_ict_ids')

    @api.depends('ict_ids')
    def _compute_ict_ids(self):
        for order in self:
            order.ict_count = len(order.ict_ids)

    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals.update({'intercompany_transfer_id' : self.intercompany_transfer_id.id})
        return vals

    def enouogh_stock_available(self, single_or_all='check_single'):
        check_single_prod_outofstock = True if single_or_all == 'check_single' else False
        outofstock_counter = 0
        total_lines = len(self.order_line.ids)
        for line in self.order_line:
            stock = line.product_id.with_context({'warehouse' : self.warehouse_id.id}).free_qty
            if stock < line.product_uom_qty:
                outofstock_counter = outofstock_counter + 1
            if check_single_prod_outofstock and outofstock_counter > 0:
                return False
            if outofstock_counter == total_lines:
                return False
        return True

    def action_create_intercompany(self):
        if self.intercompany_transfer_id:
                raise UserError(_('Inter company record has been already created.'))
        elif not self.intercompany_channel_id:
            raise UserError(_('Inter company channel must be selected to create inter company record.'))

        for order in self:
            if order.company_id.stock_replenishment_priority == "refill_from_intercomapny":
                self.check_and_create_ict()
        return True


    def action_create_interwarehouse(self):
        if self.intercompany_transfer_id:
                raise UserError(_('Inter warehouse record has been already created.'))
        elif not self.interwarehouse_channel_id:
            raise UserError(_('Inter warehouse channel must be selected to create inter warehouse record.'))

        for order in self:
            if order.company_id.stock_replenishment_priority == "refill_from_interwarehouse":
                self.check_and_create_iwt()
        return True

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.intercompany_transfer_id:
            return res
        for order in self:
            if order.company_id.stock_replenishment_priority == "refill_from_intercomapny":
                self.check_and_create_ict()
            elif order.company_id.stock_replenishment_priority == "refill_from_interwarehouse":
                self.check_and_create_iwt()
        return res

    def check_and_create_ict(self):
        create_ict_option = self.company_id.create_ict_option
        if create_ict_option == "manual" and not self.env.context.get('ict_manual',False):
            return True
        if self.env.context.get('ict_manual',False):
            self.create_intercompany_transfer_records()
        if create_ict_option == "always":
            self.create_intercompany_transfer_records()
        if create_ict_option == "insufficient_stock_single_product":
            if not self.enouogh_stock_available("check_single"):
                self.create_intercompany_transfer_records()
        if create_ict_option == "insufficient_stock_all_product":
            if not self.enouogh_stock_available("check_all"):
                self.create_intercompany_transfer_records()
        return True

    def check_and_create_iwt(self):
        create_ict_option = self.company_id.create_iwt_option
        print(self.env.context.get('iwt_manual',False))
        if create_ict_option == "manual" and not self.env.context.get('iwt_manual',False):
            return True
        if self.env.context.get('iwt_manual',False):
            self.create_interwarehouse_transfer_records()

        if create_ict_option == "stock_plus_interwarehouse":
            self.create_multi_interwarehouse_transfer_records()
        elif create_ict_option == "always":
            self.create_interwarehouse_transfer_records()
        elif create_ict_option == "insufficient_stock_single_product":
            if not self.enouogh_stock_available("check_single"):
                self.create_interwarehouse_transfer_records()
        elif create_ict_option == "insufficient_stock_all_product":
            if not self.enouogh_stock_available("check_all"):
                self.create_interwarehouse_transfer_records()
        return True

    def create_intercompany_transfer_records(self):
        channel_env = self.env['setu.intercompany.channel']
        channel = channel_env.get_channel_source_for_ict(self.company_id.id)
        if not channel:
            # Log internal note for sales order
            # ict creation process may have some error, please refer log
            msg = "<b>" + _(
                "Can't create ICT for this order, because ICT channel not found for this company. Create ICT manually.") + "</b>"
            self.message_post(body=msg)
            return False
        self.intercompany_channel_id = channel.id
        return channel.create_ict_from_channel(self)

    def get_product_stock(self, product_id, order_qty):
        wh_available = product_id.with_context({'warehouse': self.warehouse_id.id}).qty_available
        wh_outgoing = product_id.with_context({'warehouse': self.warehouse_id.id}).outgoing_qty
        net_on_hand = wh_available - (wh_outgoing - order_qty)
        return wh_available, wh_outgoing, net_on_hand


    def create_multi_interwarehouse_transfer_records(self):
        channel_env = self.env['setu.interwarehouse.channel']
        channels = channel_env.get_channel_source_for_internal_transfer(self.warehouse_id.id, all_channel=True)
        if not channels:
            # Log internal note for sales order
            # ict creation process may have some error, please refer log
            msg = "<b>" + _(
                "Can't create Inter Warehouse Transfer for this order, because Inter Warehouse Channel not found for this warehouse. Please create manually.") + "</b>"
            self.message_post(body=msg)
            return False

        ##Find total products and it's qty, write all products & qty in dict
        remaining_product_dict = {}
        iwt_ids = []
        for line in self.order_line:
            if line.product_id.is_pack:
                bundled_product_dict = {}
                bundled_product_dict = self.get_component_products(line.product_id, line.product_uom_qty, bundled_product_dict)
                for key, val in bundled_product_dict.items():
                    wh_available, wh_outgoing, net_on_hand = self.get_product_stock(key, val)
                    if net_on_hand < 0.0:
                        net_on_hand = 0.0
                    if net_on_hand > val:
                        continue
                    prod_qty = val
                    qty = remaining_product_dict.get(key.id)
                    if qty:
                        prod_qty = prod_qty + qty
                        remaining_product_dict.update({key.id: prod_qty})
                    else:
                        remaining_product_dict.update({key.id: val - net_on_hand})
            else:
                # wh_available = line.product_id.with_context({'warehouse' : self.warehouse_id.id}).qty_available
                # wh_outgoing = line.product_id.with_context({'warehouse': self.warehouse_id.id}).outgoing_qty
                # net_on_hand= wh_available - (wh_outgoing - line.product_uom_qty)
                wh_available, wh_outgoing, net_on_hand = self.get_product_stock(line.product_id, line.product_uom_qty)
                if net_on_hand < 0.0:
                    net_on_hand = 0.0

                if net_on_hand > line.product_uom_qty:
                    continue

                prod_qty = line.product_uom_qty
                qty = remaining_product_dict.get(line.product_id.id)
                if qty:
                    prod_qty = prod_qty + qty
                    remaining_product_dict.update({line.product_id.id: prod_qty})
                else:
                    remaining_product_dict.update({line.product_id.id: line.product_uom_qty - net_on_hand})

        for channel in channels:
            if not remaining_product_dict:
                continue
            channel.create_iwt_from_multiple_channels(self, remaining_product_dict=remaining_product_dict)

    def get_component_products(self, pack_product, order_qty, bundled_product_dict):
        for line in pack_product.pack_ids:
            if line.product_id.is_pack:
                bundled_product_dict = self.get_component_products(line.product_id, order_qty * line.qty_uom, bundled_product_dict)
            else:
                prod_qty = order_qty * line.qty_uom
                qty = bundled_product_dict.get(line.product_id)
                if qty:
                    prod_qty = prod_qty + qty
                bundled_product_dict.update({line.product_id : prod_qty})
        return bundled_product_dict

    def create_interwarehouse_transfer_records(self):
        channel_env = self.env['setu.interwarehouse.channel']
        channel = channel_env.get_channel_source_for_internal_transfer(self.warehouse_id.id)
        if not channel:
            # Log internal note for sales order
            # ict creation process may have some error, please refer log
            msg = "<b>" + _(
                "Can't create Inter Warehouse Transfer for this order, because Inter Warehouse Channel not found for this warehouse. Please create manually.") + "</b>"
            self.message_post(body=msg)
            return False
        self.interwarehouse_channel_id = channel.id
        return channel.create_iwt_from_channel(self)

    def action_view_ict(self):
        if not self.intercompany_transfer_id and self.interwarehouse_channel_id:
            return self.action_view_iwt()

        report_display_views = []
        form_view_id = self.env.ref('setu_intercompany_transaction.setu_intercompany_transfer_form').id
        tree_view_id = self.env.ref('setu_intercompany_transaction.setu_intercompany_transfer_tree').id
        report_display_views.append((tree_view_id, 'tree'))
        report_display_views.append((form_view_id, 'form'))

        return {
            'name': _('Inter Company Transactions'),
            'domain': [('id', 'in', self.ict_ids.ids)],
            'res_model': 'setu.intercompany.transfer',
            'view_mode': "tree,form",
            'type': 'ir.actions.act_window',
            'views': report_display_views,
        }

    def action_view_iwt(self):
        report_display_views = []
        form_view_id = self.env.ref('setu_intercompany_transaction.setu_interwareouse_transfer_form').id
        tree_view_id = self.env.ref('setu_intercompany_transaction.setu_interwarehouse_transfer_tree').id
        report_display_views.append((tree_view_id, 'tree'))
        report_display_views.append((form_view_id, 'form'))

        return {
            'name': _('Inter Warehouse Transactions'),
            'domain': [('id', 'in', self.ict_ids.ids)],
            'res_model': 'setu.intercompany.transfer',
            'view_mode': "tree,form",
            'type': 'ir.actions.act_window',
            'views': report_display_views,
        }
