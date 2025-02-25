from odoo import api, fields, models, _


class KbMany2oneField(models.Model):
    _name = 'customer_m2n'

    name = fields.Char(string="Customer Name")
