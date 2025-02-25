from odoo import api, fields, models
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)

class CompleteAction(models.TransientModel):
    _name = 'wizards_complete'
    _description = ' Wizard'

    employeeComplete = fields.Many2one('hr.employee', string="Employee name", required=True)

    def update_orders_status_to_complete(self):
        self.env['orders'].browse(self.env.context.get('active_ids')).update({'employeeComplete': self.employeeComplete})
        return True
