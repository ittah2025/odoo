from odoo import api, fields, models
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)


class CreateAppointment(models.TransientModel):
    _name = 'wizard'
    _description = ' Wizard'

    cancelReason = fields.Text(string="Reason", required=True)

    # def print_report(self):
    #     data = {
    #         'model': 'wizard',
    #         'form': self.read()[0]
    #     }
    #
    #     return self.env.ref('kb_car_workshop_s.action_print_document').report_action(self, data=data)

    def update_order_status(self):
        self.env['orders'].browse(self.env.context.get('active_ids')).update({'cancelReason': self.cancelReason})
        return True







