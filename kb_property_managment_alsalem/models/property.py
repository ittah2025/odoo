from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError


class property(models.Model):
    _name = "property"
    _rec_name = 'name'
    
    name = fields.Char(string="name")
    apartment_no = fields.One2many('apartments', 'property_id', string='apartments lines')