# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date, datetime
import requests
import json
from odoo.exceptions import ValidationError

from odoo.exceptions import UserError


class payment_line(models.Model):
    _inherit = "account.payment"

    # contract_number = fields.Many2one('contract.details', string="Contract Number", readonly= True)



