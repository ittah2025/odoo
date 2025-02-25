# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.osv import expression
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError

class MaterialRequest(models.Model):
    _name = "material.request"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Material Request"
    _order = "date"


    name = fields.Char(string="Referance",
        required=True, copy=False, readonly=True,
        index='trigram',
        default=lambda self: _('New'))
    project_id = fields.Many2one('project.project')
    part = fields.Char('Part')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('to_stock','To Delivery'),
        ('done','Done'),
        ('reject','Rejected'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    date = fields.Datetime(default=fields.Datetime.now,string="Date",readonly=True)
    company_id = fields.Many2one(comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company,readonly=True)
    user_id = fields.Many2one(comodel_name='res.users',
        string="User",
        readonly=True, index=True,
        tracking=2,
        default=lambda self: self.env.user)
    manager_id = fields.Many2one('res.users',related="user_id.employee_id.parent_id.user_id",store=True)
    notes = fields.Html('Notes')
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'material.request', sequence_date=date) or _("New")
        return super().create(vals_list)
    material_line = fields.One2many('material.request.line','material_id')
    def unlink(self):
        for record in self:
            if record.state == 'approved':
                raise UserError("You cannot remove an approved requests!")
            if record.state == 'cancel':
                raise UserError("You cannot remove an cancelled requests!")
            if record.state == 'reject':
                raise UserError("You cannot remove an rejected requests!")
        super(MaterialRequest, self).unlink()

    def action_waiting_approve(self):
        for line in self:
            line.state = "waiting"
    def action_approve(self):
        for line in self:
            line.state = "approved"
    def action_reject(self):
        for line in self:
            line.state = "reject"
    def action_draft(self):
        for line in self:
            line.state = "draft"
    picking_ids = fields.One2many('stock.picking', 'material_id', string='Transfers')
    delivery_count = fields.Integer(string='Issue Orders', compute='_compute_picking_ids')

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)
    def action_view_delivery(self):
        return self._get_action_view_picking(self.picking_ids)

    def _get_action_view_picking(self, pickings):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.user_id.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    stock_hide_button = fields.Boolean()
    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "outgoing"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "outgoing"), ("warehouse_id", "=", False)]
            )
        return types[:1]
    picking_type_id = fields.Many2one(comodel_name="stock.picking.type",string="Picking Type",required=True,default=_default_picking_type,)

    def action_process_req(self):

            for line in self.material_line:
                    delivery_ids = self.env['stock.picking'].create({
                            'partner_id': self.user_id.partner_id.id,
                            'picking_type_id': self.picking_type_id.id,
                            'location_id': line.location.id,
                            'origin':self.name,
                            'material_id':self.id,

                    })
                    delivery_id_move = self.env['stock.move'].create({
                            'location_id': line.location.id,
                            'location_dest_id': 5,
                            'name': "Issue Request",
                            'product_id': line.product_id.product_variant_id.id,
                            'product_uom_qty': line.requested_qty,
                            'picking_id': delivery_ids.id,
                            
                        })
            self.stock_hide_button = True
            self.state = "to_stock"

    def action_cancel(self):
        for line in self:
            line.state = "cancel"      
    def action_done(self):
        for line in self.picking_ids:
            if line.state not in ['done','cancel']:
                raise UserError(_('The Delivery is not done yet'))
        self.state = "done"      
class MaterialRequestLine(models.Model):
    _name = "material.request.line"
    _description = "Material Request Line"
    @api.onchange('location')
    def _compute_available_qty(self):
        for line in self:
            available_qty = self.env['stock.quant'].search([('product_id','=',line.product_id.id),('location_id','=',line.location.id)]).quantity
            line.available_qty = available_qty


    material_id = fields.Many2one('material.request')
    name = fields.Char('Item Description')
    product_id = fields.Many2one('product.product',string="Item Code")
    requested_qty = fields.Integer('Qty')
    product_uom = fields.Many2one(related="product_id.uom_id",string="UOM")
    location = fields.Many2one('stock.location',domain="[('usage','=','internal')]")
    available_qty = fields.Integer('Available Qty',compute='_compute_available_qty')
    note = fields.Text('Remarks')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_id = fields.Many2one('stock.picking', string="Material Request", store=True, readonly=False, index='btree_not_null')