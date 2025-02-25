from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


# class InheritResPartner(models.Model):
     # _inherit = 'orders'

    # def _order_count(self):
    #     for each in self:
    #         order_id = self.env['orders'].search([('vehicleOperatingCodeNumber', '=', each.id)])
    #         each.order_count = len(order_id)
    #
    # def return_action_to_open_odometers(self):
    #     self.ensure_one()
    #     domain = [
    #         ('vehicleOperatingCodeNumber', '=', self.id)]
    #     return {
    #         'name': _('orders'),
    #         'domain': domain,
    #         'res_model': 'orders',
    #         'type': 'ir.actions.act_window',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'view_type': 'form',
    #         'help': _('''<p class="oe_view_nocontent_create">
    #                        Click to Create for New service
    #                     </p>'''),
    #         'limit': 80,
    #         'context': "{'default_vehicleOperatingCodeNumber': '%s'}" % self.id,
    #     }
    #
    # order_count = fields.Integer(compute='_order_count', string='# Orders')