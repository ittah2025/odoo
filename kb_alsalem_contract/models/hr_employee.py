# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import date


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    placeOfIssue = fields.Char(string='Place Of Issue')
    dateOf = fields.Date(string='Date')
    postalCode = fields.Integer(string='Postal code')