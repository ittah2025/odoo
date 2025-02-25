from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)

class TimeOffType(models.Model):
    _inherit = 'hr.leave.type'


    kb_time_of_type = fields.Boolean(string="Paid Time Off")


