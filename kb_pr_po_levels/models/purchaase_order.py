from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('scm', 'Waiting Supply Chain Manager'),
        ('dir_m', 'Approved by SCM'),
        ('ceo', 'Waiting CEO'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    kb_requests_id = fields.Char(string="Request id")


    def action_scm_approval(self):
        self.write({'state': 'scm'})

    def action_dir_m_approval(self):
        self.write({'state': 'dir_m'})

    def action_ceo_approval(self):
        self.write({'state': 'ceo'})

    kb_amount_check = fields.Boolean(string="amount")

    @api.onchange('order_line')
    def action_calculate_total_approval(self):
        total_approved = self.company_id.po_double_validation_amount
        if self.amount_total >= total_approved:
            self.kb_amount_check = True
        else:
            self.kb_amount_check = False



    def button_confirm(self):
        '''  override button_confirm method in purchase.order '''
        self._purchase_request_line_check()
        res = super(PurchaseOrder, self).button_confirm()
        self._purchase_request_confirm_message()
        for order in self:
            if order.state not in ['draft', 'sent', 'dir_m', 'ceo']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True



    def _purchase_request_confirm_message_content(self, request, request_dict=None):
        self.ensure_one()
        if not request_dict:
            request_dict = {}
        title = _("Order confirmation %(po_name)s for your Request %(pr_name)s") % {
            "po_name": self.name,
            "pr_name": request.note,
        }
        message = "<h3>%s</h3><ul>" % title
        message += _(
            "The following requested items from Purchase Request %(pr_name)s "
            "have now been confirmed in Purchase Order %(po_name)s:"
        ) % {
            "po_name": self.name,
            "pr_name": request.note,
        }

        for line in request_dict.values():
            message += _(
                "<li><b>%(prl_name)s</b>: Ordered quantity %(prl_qty)s %(prl_uom)s, "
                "Planned date %(prl_date_planned)s</li>"
            ) % {
                "prl_name": line["name"],
                "prl_qty": line["product_qty"],
                "prl_uom": line["product_uom"],
                "prl_date_planned": line["date_planned"],
            }
        message += "</ul>"
        return message
    origin = fields.Char(string="Invoice NO")
    def _purchase_request_confirm_message(self):
        request_obj = self.env["kb_pr_level"]
        for po in self:
            requests_dict = {}
            for line in po.order_line:
                for request_line in line.sudo().purchase_request_lines:
                    request_id = request_line.kb_product_line_ids.id
                    if request_id not in requests_dict:
                        requests_dict[request_id] = {}
                    date_planned = "%s" % line.date_planned
                    data = {
                        "name": request_line.kb_product_id.name,
                        "product_qty": line.product_qty,
                        "product_uom": line.product_uom.name,
                        "date_planned": date_planned,
                    }
                    requests_dict[request_id][request_line.id] = data
            for request_id in requests_dict:
                request = request_obj.sudo().browse(request_id)
                message = po._purchase_request_confirm_message_content(
                    request, requests_dict[request_id]
                )
                request.message_post(
                    body=message, subtype_id=self.env.ref("mail.mt_comment").id
                )
        return True

    def _purchase_request_line_check(self):
        for po in self:
            for line in po.order_line:
                for request_line in line.purchase_request_lines:
                    if request_line.sudo().purchase_state == "done":
                        raise exceptions.UserError(
                            _("Purchase Request %s has already been completed")
                            % (request_line.kb_product_line_ids.name)
                        )
        return True


    def unlink(self):
        alloc_to_unlink = self.env["purchase.request.allocation"]
        for rec in self:
            for alloc in (
                rec.order_line.mapped("purchase_request_lines")
                .mapped("purchase_request_allocation_ids")
                .filtered(
                    lambda alloc, rec=rec: alloc.purchase_line_id.order_id.id == rec.id
                )
            ):
                alloc_to_unlink += alloc
        res = super().unlink()
        alloc_to_unlink.unlink()
        return res

    project_id = fields.Many2one('project.project')
    assigned_to = fields.Many2one(
        comodel_name="res.users",
        string="Approver",
        tracking=True,
        index=True,related="create_uid.employee_id.parent_id.user_id",
    )
    final_user = fields.Many2one(
        comodel_name="res.users",
        string="Final Approver",
        tracking=True,
        index=True,
    )
    payment_ids = fields.One2many('account.payment', 'purchase_order', string='Advance Payment', copy=False, store=True)

    payment_count = fields.Integer("Payemnt Requests count", compute='_compute_payment_count')
    @api.depends('payment_ids')
    def _compute_payment_count(self):
        for order in self:
            order.payment_count = len(order.payment_ids)

    def action_view_payments(self):
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id('account.action_account_payments_payable')
        result['context'] = {'default_partner_id': self.partner_id.id, 'default_purchase_order': self.id}
        if not self.payment_ids or len(self.payment_ids) > 1:
            result['domain'] = [('id', 'in', self.payment_ids.ids)]
        elif len(self.payment_ids) == 1:
            res = self.env.ref('account.view_account_payment_form', False)
            form_view = [(res and res.id or False, 'form')]
            result['views'] = form_view + [(state, view) for state, view in result.get('views', []) if view != 'form']
            result['res_id'] = self.payment_ids.id
        return result

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_request_lines = fields.Many2many(
        comodel_name="kb_pr_level_line",
        relation="purchase_request_purchase_order_line_rel",
        column1="purchase_order_line_id",
        column2="purchase_request_line_id",
        readonly=True,
        copy=False,
    )

    purchase_request_allocation_ids = fields.One2many(
        comodel_name="purchase.request.allocation",
        inverse_name="purchase_line_id",
        string="Purchase Request Allocation",
        copy=False,
    )

    def action_open_request_line_tree_view(self):
        """
        :return dict: dictionary value for created view
        """
        request_line_ids = []
        for line in self:
            request_line_ids += line.purchase_request_lines.ids

        domain = [("id", "in", request_line_ids)]

        return {
            "name": _("Purchase Request Lines"),
            "type": "ir.actions.act_window",
            "res_model": "kb_pr_level_line",
            "view_mode": "tree,form",
            "domain": domain,
        }

    def _prepare_stock_moves(self, picking):
        self.ensure_one()
        val = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        all_list = []
        for v in val:
            all_ids = self.env["purchase.request.allocation"].search(
                [("purchase_line_id", "=", v["purchase_line_id"])]
            )
            for all_id in all_ids:
                all_list.append((4, all_id.id))
            v["purchase_request_allocation_ids"] = all_list
        return val

    def update_service_allocations(self, prev_qty_received):
        for rec in self:
            allocation = self.env["purchase.request.allocation"].search(
                [
                    ("purchase_line_id", "=", rec.id),
                    ("purchase_line_id.product_id.type", "=", "service"),
                ]
            )
            if not allocation:
                return
            qty_left = rec.qty_received - prev_qty_received
            for alloc in allocation:
                allocated_product_qty = alloc.allocated_product_qty
                if not qty_left:
                    alloc.purchase_request_line_id._compute_qty()
                    break
                if alloc.open_product_qty <= qty_left:
                    allocated_product_qty += alloc.open_product_qty
                    qty_left -= alloc.open_product_qty
                    alloc._notify_allocation(alloc.open_product_qty)
                else:
                    allocated_product_qty += qty_left
                    alloc._notify_allocation(qty_left)
                    qty_left = 0
                alloc.write({"allocated_product_qty": allocated_product_qty})

                message_data = self._prepare_request_message_data(
                    alloc, alloc.purchase_request_line_id, allocated_product_qty
                )
                message = self._purchase_request_confirm_done_message_content(
                    message_data
                )
                if message:
                    alloc.purchase_request_line_id.request_id.message_post(
                        body=message, subtype_id=self.env.ref("mail.mt_comment").id
                    )

                alloc.purchase_request_line_id._compute_qty()
        return True

    @api.model
    def _purchase_request_confirm_done_message_content(self, message_data):
        title = _("Service confirmation for Request %s") % (
            message_data["request_name"]
        )
        message = "<h3>%s</h3>" % title
        message += _(
            "The following requested services from Purchase"
            " Request %(request_name)s requested by %(requestor)s "
            "have now been received:"
        ) % {
            "request_name": message_data["request_name"],
            "requestor": message_data["requestor"],
        }
        message += "<ul>"
        message += _(
            "<li><b>%(product_name)s</b>: "
            "Received quantity %(product_qty)s %(product_uom)s</li>"
        ) % {
            "product_name": message_data["product_name"],
            "product_qty": message_data["product_qty"],
            "product_uom": message_data["product_uom"],
        }
        message += "</ul>"
        return message

    def _prepare_request_message_data(self, alloc, request_line, allocated_qty):
        return {
            "request_name": request_line.request_id.name,
            "product_name": request_line.product_id.name_get()[0][1],
            "product_qty": allocated_qty,
            "product_uom": alloc.product_uom_id.name,
            "requestor": request_line.request_id.requested_by.partner_id.name,
        }

    def write(self, vals):
        #  As services do not generate stock move this tweak is required
        #  to allocate them.
        prev_qty_received = {}
        if vals.get("qty_received", False):
            service_lines = self.filtered(lambda l: l.product_id.type == "service")
            for line in service_lines:
                prev_qty_received[line.id] = line.qty_received
        res = super(PurchaseOrderLine, self).write(vals)
        if prev_qty_received:
            for line in service_lines:
                line.update_service_allocations(prev_qty_received[line.id])
        return res
    