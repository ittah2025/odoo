from odoo import api, fields, models
from datetime import date, datetime
from odoo.exceptions import UserError
from odoo import _

# class InheritResPartner(models.Model):
#     _inherit = 'orders'

 
#     def _order_state(self):
#         for each in self:
#             order_state_id = self.env['orders'].search([('state', '=', 'order_parts')])
#             each.order_state = len(order_state_id)

#     def return_action_to_open_orders(self):
#         self.ensure_one()
#         domain = [
#             ('orders', '=', self.id)]
#         return {
#             'name': _('orders'),
#             'domain': domain,
#             'res_model': 'orders',
#             'type': 'ir.actions.act_window',
#             'view_id': False,
#             'view_mode': 'tree,form',
#             'view_type': 'form',
#             'help': _('''<p class="oe_view_nocontent_create">
#                            Click to Create for New service
#                         </p>'''),
#             'limit': 80,
#             'context': "{'default_partner_id': '%s'}" % self.id,
#         }
#     order_state = fields.Integer(compute='_order_state', string='# Orders')