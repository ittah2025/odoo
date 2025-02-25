from odoo import api, fields, models, _
from calendar import month
from email.policy import default
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)


class tires_table(models.Model):
    _name = "tires_table"


    tires_table_id = fields.Many2one('orders')

    tireMeasure = fields.Char('Tire Tread Depth', groups='base.group_user')
    tireSerialNumber = fields.Char('Tire Serial Number', groups='base.group_user')

    tireItem = fields.Selection([
        ('fr', 'FR'),
        ('fl', 'FL'),
        ('RR0', 'RR0'),
        ('RR1', 'RR1'),
        ('RL0', 'RL0'),
        ('RL1', 'RL1'),
        ('LL', 'LR'),

    ], string="Side")

    tireInstallDate = fields.Date("Install Date", groups='base.group_user')
    tireKm = fields.Char("Install Km", groups='base.group_user')


