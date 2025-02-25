from odoo import api, fields, models, _
from calendar import month
from email.policy import default
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)


class battery_table(models.Model):
    _name = "battery_table"


    battery_table_id = fields.Many2one('orders')

    batteryItem = fields.Selection([
        ('battery1', 'Battery 1'),
        ('battery2', 'Battery 2'),

    ], string="Battery")

    company_name = fields.Char('Company Name', groups='base.group_user')
    batterySerialNumber = fields.Char('Battery Serial Number', groups='base.group_user')
    batteryAmps = fields.Char('Amps', groups='base.group_user')
    batteryvolts = fields.Char('Battery Voltage', groups='base.group_user')


    batteryinstallDate = fields.Date("Install Date", groups='base.group_user')
    batterychangeDate = fields.Date("Expiration Date", groups='base.group_user')
    batterytotal_days_count = fields.Char(string="Total Time")


    @api.onchange('batteryinstallDate', 'batterychangeDate', 'batterytotal_days_count')
    def calculate_date(self):
        if self.batteryinstallDate and self.batterychangeDate:
            d1 = datetime.strptime(str(self.batteryinstallDate), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.batterychangeDate), '%Y-%m-%d')
            self.batterytotal_days_count = d2 - d1

    batteryWarranty = fields.Char(string="Battery Warranty")