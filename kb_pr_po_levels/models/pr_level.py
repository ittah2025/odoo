from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError



class KbRrLevel(models.Model):
    _name = "kb_pr_level"
    _description = "Request"
    _rec_name = "kb_pr_levels_ids"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "incoming"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "incoming"), ("warehouse_id", "=", False)]
            )
        return types[:1]
    @api.depends("state")
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in (
                "approved",
                "done",
                "in_progress",
                "cancel",
                "reject",
            ):
                rec.is_editable = False
            else:
                rec.is_editable = True
    kb_product_line_ids = fields.One2many('kb_pr_level_line', 'kb_product_line_ids', copy=True)

    kb_vendor_id = fields.Many2one('res.partner', string="Vendor")
    kb_date = fields.Date(string="Date", default=datetime.today())

    kb_user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id, string=" Created By")
    assigned_to = fields.Many2one("res.users",
        string="Approver",tracking=True,index=True,related="kb_user_id.employee_id.parent_id.user_id",)
    picking_type_id = fields.Many2one(comodel_name="stock.picking.type",string="Picking Type",required=True,default=_default_picking_type,)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)

    stock_hide_button = fields.Boolean(string="Hide", default=False)
    purchase_hide_button = fields.Boolean(string="purchase Hide", default=False)


    kb_location_id = fields.Many2one('stock.location', string="Source Location", domain="[('usage', '=', 'internal')]")
    kb_destination_id = fields.Many2one('stock.location', string="Destination Location", domain="[('usage', '=', 'internal')]")
    is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True)
    def action_new(self):
        self.state = 'new'

    def kb_set_to_supervisor_state(self):
        for rec in self:
            if not rec.kb_product_line_ids:
                raise UserError(
                    _(
                        "You can't request an approval for a purchase request "
                        "which is empty."
                    )
                )
            rec.state = 'supervisor'
            # create cativity to the assigned person
            # check if the activity already exists
            activity = self.env['mail.activity'].search([('res_id', '=', rec.id), ('activity_type_id', '=', 4)])

            # if the activity exists, update it
            if activity:
                activity.write({
                    'display_name': rec.note,
                    'summary': _('Request Approval for PR (%s)')% rec.note,
                    'date_deadline': fields.date.today(),
                    'user_id': rec.assigned_to.id,
                    'res_model':'kb_pr_level',
                })
            # if the activity does not exist, create it
            else:
                res_model_id = self.env['ir.model'].search([('model',"=",'kb_pr_level')])
                self.env['mail.activity'].create({
                    'display_name': rec.note,
                    'summary': _('Request Approval for PR (%s)')% rec.note,
                    'date_deadline':fields.date.today(),
                    'user_id': rec.assigned_to.id,
                    'res_id': rec.id,
                    'activity_type_id': 4,
                    'res_model_id':res_model_id.id,
                    'res_model':'kb_pr_level',
                })

    def kb_set_to_scm_state(self):
        for rec in self:
            rec.state = 'scm'

    def create_purchase_order(self):
        # kb_date_today = fields.Datetime(string="Date", default=datetime.today())

        purchase_id = self.env['purchase.order'].create({
            'partner_id': self.kb_vendor_id.id,
            # 'date_order': kb_date_today,
            'kb_requests_id': self.kb_pr_levels_ids,
        })
        vals = list()
        for rec in self.kb_product_line_ids:
            vals.append({
                'product_id': rec.kb_product_id.id,
                'name': rec.kb_product_name,
                'product_qty': rec.kb_product_qty,
                'price_unit': rec.kb_product_price,
                # 'taxes_id': rec.kb_tax_external,
                # 'price_subtotal': rec.kb_total_price_external,
                'analytic_distribution': {
                    rec.analytic_account_id.id: 100.0  # Assuming 100% allocation to this analytic account
                },
                'order_id': purchase_id.id,

            })
        purchase_line_id = self.env['purchase.order.line'].create(vals)

        self.purchase_hide_button = True
    purchase_count = fields.Integer(
        string="Purchases count", compute="_compute_purchase_count", readonly=True
    )
    @api.depends("kb_product_line_ids")
    def _compute_purchase_count(self):
        for rec in self:
            rec.purchase_count = len(rec.mapped("kb_product_line_ids.purchase_lines.order_id"))

    def action_view_purchase_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        lines = self.mapped("kb_product_line_ids.purchase_lines.order_id")
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [
                (self.env.ref("purchase.purchase_order_form").id, "form")
            ]
            action["res_id"] = lines.id
        return action
    def action_done(self):
        self.state = 'done'

    def action_reject(self):
        self.state = 'reject'

    def action_cancel(self):
        self.state = 'cancel'
    def scm_approve(self):
        self.state = 'approved'
    state = fields.Selection([
        ('new', 'Draft'),
        ('supervisor', 'Waiting Supervisor Approval'),
        ('scm', 'Waiting Supply Chain Manager Approval'),
        ('approved','Approved'), # must be readonly
        ('in_progress','In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ('reject', 'Reject'),
    ], readonly=True, default="new", help='Choose the state')

    kb_pr_levels_ids = fields.Char(string='Request ID', required=True, readonly=True, default=lambda self: _('New'),
                                   copy=False)
    note = fields.Char(string='')
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request")
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New'
        if vals.get('kb_pr_levels_ids', ('New')) == ('New'):
            vals['kb_pr_levels_ids'] = self.env['ir.sequence'].next_by_code('kb_seq_for_pr') or ('New')
        res = super(KbRrLevel, self).create(vals)        
        return res

    line_subtotal = fields.Monetary(string="Subtotal")

    @api.onchange('kb_product_line_ids')
    def calc_total_price(self):
        kb_subtotal = 0.0
        for lines in self.kb_product_line_ids:
            if lines.kb_subtotal:
                kb_subtotal += lines.kb_subtotal
            else:
                self.line_subtotal = 0.0
        self.line_subtotal = kb_subtotal


    order_count = fields.Integer(compute='requests_count', string='# Requests')
    deli_count = fields.Integer(compute='stock_count', string='# Delivery')


    def requests_count(self):
        for each in self:
            order_id = self.env['purchase.order'].search([('kb_requests_id', '=', self.kb_pr_levels_ids)])
            each.order_count = len(order_id)

    def requests_smart_button(self):
        self.ensure_one()
        domain = [('kb_requests_id', '=', self.kb_pr_levels_ids)]
        return {
            'name': _('Requests'),
            'domain': domain,
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': "{'default_kb_vendor_id': '%s'}" % self.id,
        }

    def stock_count(self):
        for each in self:
            stock_id = self.env['stock.picking'].search([('kb_requests_id', '=', self.kb_pr_levels_ids)])
            each.deli_count = len(stock_id)

    def stock_smart_button(self):
        self.ensure_one()
        domain = [('kb_requests_id', '=', self.kb_pr_levels_ids)]
        return {
            'name': _('Delivery'),
            'domain': domain,
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': "{'default_stock_picking_del': '%s'}" % self.id,
        }


    def create_delivery_order(self):
        warehouse_delivery_id = self.env['stock.picking.type'].search([('code', '=', 'outgoing'),
                                                                       ('default_location_src_id', '=', self.kb_location_id.id)], limit=1)

        if self.kb_location_id:
            delivery_ids = self.env['stock.picking'].create({
                'partner_id': self.kb_user_id.id,
                'picking_type_id': warehouse_delivery_id.id,
                'location_id': self.kb_location_id.id,
                'kb_requests_id': self.kb_pr_levels_ids,

            })
            for line in self.kb_product_line_ids:
                delivery_id_move = self.env['stock.move'].create({
                    'location_id': self.kb_location_id.id,
                    'location_dest_id': 5,
                    'name': "Purchase Request",
                    'product_id': line.kb_product_id.product_variant_id.id,
                    'product_uom_qty': line.issued_qty,
                    # 'quantity_done': line.kb_product_qty,
                    'picking_id': delivery_ids.id,
                    'analytic_distribution': {
                        line.analytic_account_id.id: 100.0  # Assuming 100% allocation to this analytic account
                    },
                })
            # delivery_ids.action_confirm()
            self.stock_hide_button = True,
        else:
            raise UserError(_('Must Select Source Location!'))


            # delivery_ids.button_validate(),


    internal_hide_button = fields.Boolean(string="Hide", default=False)


    # def create_internal_transfer(self):

    #     # warehouse_delivery_id = self.env['stock.picking.type'].search([('code', '=', 'outgoing'),
    #     #                                                                ('default_location_src_id', '=',
    #     #                                                                 self.kb_location_id.id)], limit=1)

    #     if self.kb_destination_id and self.kb_location_id:
    #         delivery_ids = self.env['stock.picking'].create({
    #             'partner_id': self.kb_user_id.id,
    #             'picking_type_id': 5,
    #             'location_id': self.kb_location_id.id,
    #             'location_dest_id': self.kb_destination_id.id,
    #             'kb_requests_id': self.kb_pr_levels_ids,

    #         })
    #         for line in self.kb_product_line_ids:
    #             delivery_id_move = self.env['stock.move'].create({
    #                 'location_id': self.kb_location_id.id,
    #                 'location_dest_id': self.kb_destination_id.id,
    #                 'name': "Purchase Request",
    #                 'product_id': line.kb_product_id.product_variant_id.id,
    #                 'product_uom_qty': line.kb_product_qty,
    #                 # 'quantity_done': line.kb_product_qty,
    #                 'picking_id': delivery_ids.id,
    #                 'analytic_distribution': {
    #                     line.analytic_account_id.id: 100.0  # Assuming 100% allocation to this analytic account
    #                 },
    #             })

    #         # delivery_ids.action_confirm()
    #         self.internal_hide_button = True,
    #     else:
    #         raise UserError(_('Must Select Source Location And Destination Location!'))


    def button_in_progress(self):
        lines = self.mapped("kb_product_line_ids.purchase_lines.order_id")
        for po in lines:
            if po.state == 'draft':
                po.write({
                    'origin':self.note,})
        return self.write({"state": "in_progress"})
    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({"state": "new", "note": self._get_default_name()})
        return super(KbRrLevel, self).copy(default)

    @api.model
    def _get_partner_id(self, request):
        user_id = request.assigned_to or self.env.user
        return user_id.partner_id.id



    def write(self, vals):
        res = super(KbRrLevel, self).write(vals)
        for request in self:
            if vals.get("assigned_to"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
        return res

    def _can_be_deleted(self):
        self.ensure_one()
        return self.state == "new"

    def unlink(self):
        for request in self:
            if not request._can_be_deleted():
                raise UserError(
                    _("You cannot delete a purchase request which is not draft.")
                )
        return super(KbRrLevel, self).unlink()

    def button_draft(self):
        self.write({"state": "new"})


class KbRequestForSalesLine(models.Model):
    _name = "kb_pr_level_line"

    kb_product_id = fields.Many2one('product.template', string="Product")
    product_uom_id = fields.Many2one(comodel_name="uom.uom",string="UoM",tracking=True,domain="[('category_id', '=', product_uom_category_id)]",)
    product_uom_category_id = fields.Many2one(related="kb_product_id.uom_id.category_id")
    kb_product_name = fields.Char(string='Name', related="kb_product_id.name", required=False)
    kb_product_qty = fields.Float(string='Requested Quantity', required=False, default=1)
    kb_product_qty_on_hand = fields.Float(string='Available Quantity', related="kb_product_id.qty_available", default=1)
    issued_qty = fields.Float('Issued Qty')
    kb_product_price = fields.Float(string='Estimated Cost', readonly=False)
    kb_product_tax = fields.Many2many('account.tax', 'product_cost_rel', string="Taxes")
    company_id = fields.Many2one(related="kb_product_line_ids.company_id",store=True)
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string="Analytic Account")
    move_dest_ids = fields.One2many(
            comodel_name="stock.move",
            inverse_name="created_purchase_request_line_id",
            string="Downstream Moves",
        )
    purchase_lines = fields.Many2many(
        comodel_name="purchase.order.line",
        relation="purchase_request_purchase_order_line_rel",
        column1="purchase_request_line_id",
        column2="purchase_order_line_id",
        string="Purchase Order Lines",
        readonly=True,
        copy=False,
    )
    purchase_state = fields.Selection(
        compute="_compute_purchase_state",
        string="Purchase Status",
        selection=lambda self: self.env["purchase.order"]._fields["state"].selection,
        store=True,
    )
    @api.depends("purchase_lines.state", "purchase_lines.order_id.state")
    def _compute_purchase_state(self):
        for rec in self:
            temp_purchase_state = False
            if rec.purchase_lines:
                if any(po_line.state == "done" for po_line in rec.purchase_lines):
                    temp_purchase_state = "done"
                elif all(po_line.state == "cancel" for po_line in rec.purchase_lines):
                    temp_purchase_state = "cancel"
                elif any(po_line.state == "purchase" for po_line in rec.purchase_lines):
                    temp_purchase_state = "purchase"
                elif any(
                    po_line.state == "to approve" for po_line in rec.purchase_lines
                ):
                    temp_purchase_state = "to approve"
                elif any(po_line.state == "sent" for po_line in rec.purchase_lines):
                    temp_purchase_state = "sent"
                elif all(
                    po_line.state in ("draft", "cancel")
                    for po_line in rec.purchase_lines
                ):
                    temp_purchase_state = "draft"
            rec.purchase_state = temp_purchase_state

    purchase_request_allocation_ids = fields.One2many(
        comodel_name="purchase.request.allocation",
        inverse_name="purchase_request_line_id",
        string="Purchase Request Allocation",
    )

    qty_in_progress = fields.Float(
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty",
        store=True,
        help="Quantity in progress.",
    )
    qty_done = fields.Float(
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty",
        store=True,
        help="Quantity completed",
    )
    qty_cancelled = fields.Float(
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty_cancelled",
        store=True,
        help="Quantity cancelled",
    )
    qty_to_buy = fields.Boolean(
        compute="_compute_qty_to_buy",
        string="There is some pending qty to buy",
        store=True,
    )
    pending_qty_to_receive = fields.Float(
        compute="_compute_qty_to_buy",
        digits="Product Unit of Measure",
        copy=False,
        string="Pending Qty to Receive",
        store=True,
    )
    kb_subtotal = fields.Float(string="Subtotal", compute='_compute_amount_subtotal')
    date_required = fields.Date(
        string="Request Date",
        required=True,
        tracking=True,
        default=fields.Date.context_today,
    )
    @api.depends('kb_product_id', 'kb_product_qty', 'kb_product_price', 'kb_product_tax')
    def _compute_amount_subtotal(self):
        for rec in self:
            kb_product_price = rec.kb_product_price
            amount = rec.kb_product_qty * kb_product_price
            new_subtotal = (rec.kb_product_tax.amount / 100) * amount
            rec.kb_subtotal = amount + new_subtotal

    kb_product_line_ids = fields.Many2one('kb_pr_level')
    @api.depends(
        "purchase_request_allocation_ids",
        "purchase_request_allocation_ids.stock_move_id.state",
        "purchase_request_allocation_ids.stock_move_id",
        "purchase_request_allocation_ids.purchase_line_id",
        "purchase_request_allocation_ids.purchase_line_id.state",
        "kb_product_line_ids.state",
        "kb_product_qty",
        "issued_qty",
    )
    def _compute_qty_to_buy(self):
        for pr in self:
            qty_to_buy = sum(pr.mapped("kb_product_qty")) - sum(pr.mapped("issued_qty")) - sum(pr.mapped("qty_done"))
            pr.qty_to_buy = qty_to_buy > 0.0
            pr.pending_qty_to_receive = qty_to_buy

    @api.depends(
        "purchase_request_allocation_ids",
        "purchase_request_allocation_ids.stock_move_id.state",
        "purchase_request_allocation_ids.stock_move_id",
        "purchase_request_allocation_ids.purchase_line_id.state",
        "purchase_request_allocation_ids.purchase_line_id",
    )
    def _compute_qty(self):
        for request in self:
            done_qty = sum(
                request.purchase_request_allocation_ids.mapped("allocated_product_qty")
            )
            open_qty = sum(
                request.purchase_request_allocation_ids.mapped("open_product_qty")
            )
            request.qty_done = done_qty
            request.qty_in_progress = open_qty

    @api.depends(
        "purchase_request_allocation_ids",
        "purchase_request_allocation_ids.stock_move_id.state",
        "purchase_request_allocation_ids.stock_move_id",
        "purchase_request_allocation_ids.purchase_line_id.order_id.state",
        "purchase_request_allocation_ids.purchase_line_id",
    )
    def _compute_qty_cancelled(self):
        for request in self:
            if request.kb_product_id.type != "service":
                qty_cancelled = sum(
                    request.mapped("purchase_request_allocation_ids.stock_move_id")
                    .filtered(lambda sm: sm.state == "cancel")
                    .mapped("product_qty")
                )
            else:
                qty_cancelled = sum(
                    request.mapped("purchase_request_allocation_ids.purchase_line_id")
                    .filtered(lambda sm: sm.state == "cancel")
                    .mapped("product_qty")
                )
                # done this way as i cannot track what was received before
                # cancelled the purchase order
                qty_cancelled -= request.qty_done
            if request.product_uom_id:
                request.qty_cancelled = (
                    max(
                        0,
                        request.kb_product_id.uom_id._compute_quantity(
                            qty_cancelled, request.product_uom_id
                        ),
                    )
                    if request.purchase_request_allocation_ids
                    else 0
                )
            else:
                request.qty_cancelled = qty_cancelled

    # @api.model
    # def _calc_new_qty(self, request_line, po_line=None, new_pr_line=False):
    #     purchase_uom = po_line.product_uom or request_line.product_id.uom_po_id
    #     # TODO: Not implemented yet.
    #     #  Make sure we use the minimum quantity of the partner corresponding
    #     #  to the PO. This does not apply in case of dropshipping
    #     supplierinfo_min_qty = 0.0
    #     if not po_line.order_id.dest_address_id:
    #         supplierinfo_min_qty = self._get_supplier_min_qty(
    #             po_line.product_id, po_line.order_id.partner_id
    #         )

    #     rl_qty = 0.0
    #     # Recompute quantity by adding existing running procurements.
    #     if new_pr_line:
    #         rl_qty = po_line.product_uom_qty
    #     else:
    #         for prl in po_line.purchase_request_lines:
    #             for alloc in prl.purchase_request_allocation_ids:
    #                 rl_qty += alloc.product_uom_id._compute_quantity(
    #                     alloc.requested_product_uom_qty, purchase_uom
    #                 )
    #     qty = max(rl_qty, supplierinfo_min_qty)
    #     return qty

    purchased_qty = fields.Float(
        string="RFQ/PO Qty",
        digits="Product Unit of Measure",
        compute="_compute_purchased_qty",
    )
    def _compute_purchased_qty(self):
        for rec in self:
            rec.purchased_qty = 0.0
            for line in rec.purchase_lines.filtered(lambda x: x.state != "cancel"):
                if rec.product_uom_id and line.product_uom != rec.product_uom_id:
                    rec.purchased_qty += line.product_uom._compute_quantity(
                        line.product_qty, rec.product_uom_id
                    )
                else:
                    rec.purchased_qty += line.product_qty