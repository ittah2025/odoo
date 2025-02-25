from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)


class EndofContractView(models.Model):
    _inherit = "hr.employee"

    
    end_date = fields.Date(string="Contract End Date", related='contract_id.date_end')