from calendar import month
from email.policy import default
from odoo import api, fields, models, _
from datetime import date
from datetime import datetime
import re
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)


class maintenanceItems(models.Model):
    _name = "maintenanceItems"
    _table = "maintenanceItems"
    _description = "maintenanceItems"

    maintenanceItems_id = fields.Char(string='Maintenance Items', required=True,
                                              copy=False, readonly=True, default=lambda self: ('New'))

    name = fields.Char(string='Name', required=True, translate=True)

    note = fields.Text(string="Description")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'Maintenance Items'
        if vals.get('maintenanceItems_id', ('New')) == ('New'):
            vals['maintenanceItems_id'] = self.env['ir.sequence'].next_by_code(
                'maintenanceItems') or ('New')
        res = super(maintenanceItems, self).create(vals)
        return res


