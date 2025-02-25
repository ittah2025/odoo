from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)


class Dashboard(models.Model):
    _inherit = 'orders'

    @api.model
    def get_data(self):
            # default_date = datetime.today().date()
            # domain = [('date_order', '>=', default_date)]
        allcarsCount = self.env['orders'].search([])
        orderComplete = self.env['orders'].search([('state', '=', 'complete')])
        orderParts = self.env['orders'].search([('state', '=', 'order_parts')])
        ordersHold = self.env['orders'].search([('state', '=', 'on_hold')])
        ordersInprogress = self.env['orders'].search([('state', '=', 'in_progress')])
        allOrders =  self.env['orders'].search([])
        return {
                'total_cars': len(allcarsCount),
                'total_order_complete': len(orderComplete),
                'total_order_parts': len(orderParts),
                'total_order_onHold': len(ordersHold),
                'total_order_inProgres': len(ordersInprogress),
                'total_orders': len(allOrders)
            }
        

