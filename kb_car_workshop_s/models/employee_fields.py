from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)


class employee_fields(models.Model):
    _inherit = "hr.employee"


    carshop_employee = fields.Boolean("Car Workshop Employee")
