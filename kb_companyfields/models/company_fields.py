
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class companyFields(models.Model):
    
    _inherit = "res.company"

    companyNameEN = fields.Char('Company Name English')
    registerNumber = fields.Char('License Number')