from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)


class products_new_fields(models.Model):
    _inherit = "product.template"

    Vehicle_type_prod = fields.Char("Vehicle Type", translate=True)

    products_workshop = fields.Boolean("Product For WorkShop")
